#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44'; TMP=Path('/tmp/vp8l-packed-huffman-v2')
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def rep(s,o,n,l):
 if o not in s:raise SystemExit('missing '+l)
 return s.replace(o,n,1)
def patch(root):
 hp=root/'src/lossless/decoder/huffman.rs';h=hp.read_text();marker='''    pub(crate) const fn is_single_node(&self) -> bool {\n        matches!(self.0, HuffmanTreeInner::Single(_))\n    }\n''';add='''    pub(crate) fn max_code_bits(&self) -> u8 {\n        match &self.0 {\n            HuffmanTreeInner::Single(_) => 0,\n            HuffmanTreeInner::Tree { primary_table, .. } => primary_table.iter().map(|entry| (entry >> 12) as u8).max().unwrap_or(0),\n        }\n    }\n\n    pub(crate) fn packed_lookup(&self, bits: u16) -> (u8, u16) {\n        match &self.0 {\n            HuffmanTreeInner::Single(symbol) => (0, *symbol),\n            HuffmanTreeInner::Tree { primary_table, table_mask, .. } => {\n                let entry = primary_table[usize::from(bits & *table_mask)];\n                let n = (entry >> 12) as u8;\n                debug_assert!(n <= MAX_TABLE_BITS);\n                (n, entry & 0xfff)\n            }\n        }\n    }\n\n''';h=rep(h,marker,add+marker,'huffman helpers');hp.write_text(h)
 mp=root/'src/lossless/decoder/mod.rs';m=mp.read_text();typ='type HuffmanCodeGroup = [HuffmanTree; HUFFMAN_CODES_PER_META_CODE];\n';m=rep(m,typ,typ+'''\n#[derive(Clone, Copy, Debug, Default)]\nstruct PackedHuffmanEntry { bits: u8, code: u16, rgba: u32 }\n\n''','packed type')
 m=rep(m,'        let mut hufftree_groups = Vec::new();\n\n        for _i in 0..num_huff_groups {\n','        let mut hufftree_groups = Vec::new();\n        let mut packed_offsets = Vec::with_capacity(num_huff_groups as usize);\n        let mut packed_entries = Vec::new();\n\n        for _i in 0..num_huff_groups {\n','vectors')
 old='''            hufftree_groups.push(group);\n        }\n\n        let huffman_mask = if huffman_bits == 0 {\n''';new='''            let max_literal_bits: u16 = group[..4].iter().map(|tree| u16::from(tree.max_code_bits())).sum();\n            let all_single = group[..4].iter().all(|tree| tree.is_single_node());\n            let packed_offset = if !all_single && max_literal_bits < 6 {\n                let offset = packed_entries.len();\n                for raw in 0u16..64 {\n                    let mut bits = raw;\n                    let (green_bits, green) = group[GREEN].packed_lookup(bits); bits >>= green_bits;\n                    if green >= 256 { packed_entries.push(PackedHuffmanEntry { bits: green_bits, code: green, rgba: 0 }); continue; }\n                    let (red_bits, red) = group[RED].packed_lookup(bits); bits >>= red_bits;\n                    let (blue_bits, blue) = group[BLUE].packed_lookup(bits); bits >>= blue_bits;\n                    let (alpha_bits, alpha) = group[ALPHA].packed_lookup(bits);\n                    debug_assert!(red < 256 && blue < 256 && alpha < 256);\n                    packed_entries.push(PackedHuffmanEntry {\n                        bits: green_bits + red_bits + blue_bits + alpha_bits, code: green,\n                        rgba: u32::from_le_bytes([red as u8, green as u8, blue as u8, alpha as u8]),\n                    });\n                }\n                Some(offset)\n            } else { None };\n            packed_offsets.push(packed_offset);\n            hufftree_groups.push(group);\n        }\n\n        let huffman_mask = if huffman_bits == 0 {\n''';m=rep(m,old,new,'group build')
 m=rep(m,'            huffman_code_groups: hufftree_groups,\n        };\n','            huffman_code_groups: hufftree_groups,\n            packed_offsets,\n            packed_entries,\n        };\n','info build')
 m=rep(m,'        let mut tree = &huffman_info.huffman_code_groups[huff_index];\n        let mut index = 0;\n','        let mut tree = &huffman_info.huffman_code_groups[huff_index];\n        let mut packed_offset = huffman_info.packed_offsets[huff_index];\n        let mut index = 0;\n','decode init')
 m=rep(m,'                tree = &huffman_info.huffman_code_groups[huff_index];\n\n                // Fast path','                tree = &huffman_info.huffman_code_groups[huff_index];\n                packed_offset = huffman_info.packed_offsets[huff_index];\n\n                // Fast path','group change')
 old='''            let code = tree[GREEN].read_symbol(&mut self.bit_reader)?;\n\n            //check code\n            if code < 256 {\n''';new='''            let code = if let Some(offset) = packed_offset {\n                let entry = huffman_info.packed_entries[offset + (self.bit_reader.peek_full() as usize & 63)];\n                self.bit_reader.consume(entry.bits)?;\n                if entry.code < 256 {\n                    let value = entry.rgba.to_le_bytes();\n                    data[index * 4..][..4].copy_from_slice(&value);\n                    if let Some(color_cache) = huffman_info.color_cache.as_mut() { color_cache.insert(value); }\n                    index += 1; continue;\n                }\n                entry.code\n            } else { tree[GREEN].read_symbol(&mut self.bit_reader)? };\n\n            //check code\n            if code < 256 {\n''';m=rep(m,old,new,'decode packed')
 m=rep(m,'    huffman_code_groups: Vec<HuffmanCodeGroup>,\n}\n','    huffman_code_groups: Vec<HuffmanCodeGroup>,\n    packed_offsets: Vec<Option<usize>>,\n    packed_entries: Vec<PackedHuffmanEntry>,\n}\n','info fields');mp.write_text(m)
def ch(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];z=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+z+(z&1)
 return o
BENCH='''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def runbench():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();base=TMP/'base';cand=TMP/'cand';run(['git','worktree','add','--detach',str(base),BASE]);run(['git','worktree','add','--detach',str(cand),BASE]);patch(cand);run(['cargo','fmt'],cwd=cand);run(['cargo','test','-q'],cwd=cand);run(['cargo','doc','-q'],cwd=cand);run(['cargo','clippy','--all-features','--','-D','warnings'],cwd=cand);run(['cargo','fmt','--','--check'],cwd=cand);run(['cargo','+1.80.1','build','-q'],cwd=cand)
 rels=[p.relative_to(base)for p in sorted((base/'tests/images').rglob('*.webp'))if b'VP8L'in ch(p.read_bytes())and b'ANIM'not in ch(p.read_bytes())];ppm=TMP/'large.ppm';w=h=1536
 with ppm.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):i=x*3;row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
   f.write(row)
 webp=TMP/'large.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)])
 bins={}
 for n,r in [('base',base),('cand',cand)]:
  (r/'examples').mkdir(exist_ok=True);(r/'examples/ph2.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','ph2','-q'],cwd=r,env=e);bins[n]=r/'target/release/examples/ph2'
 def inv(n,m,it,ps):return run(['taskset','-c','0',str(bins[n]),m,str(it),*[str(x)for x in ps]],cap=True)
 if inv('base','h',1,[*[base/r for r in rels],webp])!=inv('cand','h',1,[*[cand/r for r in rels],webp]):raise SystemExit('hash mismatch')
 rows=[]
 for rnd in range(1,14):
  order=['base','cand']if rnd%2 else['cand','base']
  for n in order:rows.append(('corpus',rnd,n,float(inv(n,'t',55,[(base if n=='base' else cand)/r for r in rels]))));rows.append(('large',rnd,n,float(inv(n,'t',3,[webp]))))
 rr={};vals={}
 for w,r,n,x in rows:rr.setdefault((w,r),{})[n]=x;vals.setdefault((w,n),[]).append(x)
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L packed Huffman v2','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- contiguous packed tables; hashes + tests/docs/Clippy/fmt/MSRV passed','','| workload | baseline | candidate | paired median | positive | range |','|---|---:|---:|---:|---:|---:|']
 for w in('corpus','large'):
  q=[z['base']/z['cand']for(ww,_),z in sorted(rr.items())if ww==w];L.append(f'| {w} | {statistics.median(vals[w,"base"]):.3f} us | {statistics.median(vals[w,"cand"]):.3f} us | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-packed-huffman-v2.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':runbench()
