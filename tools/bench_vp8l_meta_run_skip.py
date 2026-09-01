#!/usr/bin/env python3
import math,os,shutil,statistics,subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44';TMP=Path('/tmp/vp8l-meta-run-skip');VS=['scan','pre','pre_const']
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+n+(n&1)
 return o
OLD_ELSE='''                } else {\n                    let x = index % usize::from(width);\n                    let y = index / usize::from(width);\n                    next_block_start = (x | usize::from(huffman_info.mask))\n                        .min(usize::from(width - 1))\n                        + y * usize::from(width)\n                        + 1;\n                    huffman_info.get_huff_index(x as u16, y as u16)\n                };\n'''
SCAN_ELSE='''                } else {\n                    let width_usize = usize::from(width);\n                    let y = index / width_usize;\n                    let x = index - y * width_usize;\n                    let meta_width = usize::from(huffman_info.xsize);\n                    let meta_x = x >> huffman_info.bits;\n                    let meta_y = y >> huffman_info.bits;\n                    let pos = meta_y * meta_width + meta_x;\n                    let huff_index = usize::from(huffman_info.image[pos]);\n                    let row_end = (meta_y + 1) * meta_width;\n                    let mut end_pos = pos + 1;\n                    while end_pos < row_end && usize::from(huffman_info.image[end_pos]) == huff_index {\n                        end_pos += 1;\n                    }\n                    let run_end_meta = end_pos - meta_y * meta_width;\n                    let run_end_x = (run_end_meta << huffman_info.bits).min(width_usize);\n                    next_block_start = y * width_usize + run_end_x;\n                    huff_index\n                };\n'''
PRE_ELSE='''                } else {\n                    let width_usize = usize::from(width);\n                    let y = index / width_usize;\n                    let x = index - y * width_usize;\n                    let meta_width = usize::from(huffman_info.xsize);\n                    let pos = (y >> huffman_info.bits) * meta_width + (x >> huffman_info.bits);\n                    let huff_index = usize::from(huffman_info.image[pos]);\n                    let run_end_x = (usize::from(huffman_info.run_ends[pos]) << huffman_info.bits).min(width_usize);\n                    next_block_start = y * width_usize + run_end_x;\n                    huff_index\n                };\n'''
def add_precompute(s):
 marker='''        let huffman_mask = if huffman_bits == 0 {\n'''
 add='''        let mut run_ends = vec![0u16; entropy_image.len()];\n        if huffman_bits != 0 {\n            let w = usize::from(huffman_xsize);\n            for (row_idx, row) in entropy_image.chunks_exact(w).enumerate() {\n                let mut end = w as u16;\n                for x in (0..w).rev() {\n                    if x + 1 == w || row[x] != row[x + 1] { end = (x + 1) as u16; }\n                    run_ends[row_idx * w + x] = end;\n                }\n            }\n        }\n\n'''
 if marker not in s:raise SystemExit('mask marker');s=s.replace(marker,add+marker,1)
 s=s.replace('''            huffman_code_groups: hufftree_groups,\n        };\n''','''            huffman_code_groups: hufftree_groups,\n            run_ends,\n        };\n''',1)
 s=s.replace('''    huffman_code_groups: Vec<HuffmanCodeGroup>,\n}\n''','''    huffman_code_groups: Vec<HuffmanCodeGroup>,\n    run_ends: Vec<u16>,\n}\n''',1)
 return s
def add_const(s,root):
 hp=root/'src/lossless/decoder/huffman.rs';h=hp.read_text();m='''    pub(crate) const fn is_single_node(&self) -> bool {\n        matches!(self.0, HuffmanTreeInner::Single(_))\n    }\n''';a='''    pub(crate) const fn single_symbol(&self) -> Option<u16> {\n        match self.0 { HuffmanTreeInner::Single(symbol) => Some(symbol), HuffmanTreeInner::Tree { .. } => None }\n    }\n\n'''
 if m not in h:raise SystemExit('single marker');hp.write_text(h.replace(m,a+m,1))
 s=s.replace('''        let mut hufftree_groups = Vec::new();\n\n        for _i in 0..num_huff_groups {\n''','''        let mut hufftree_groups = Vec::new();\n        let mut single_pixels = Vec::new();\n\n        for _i in 0..num_huff_groups {\n''',1)
 old='''            hufftree_groups.push(group);\n        }\n\n'''
 new='''            let single_pixel = match (group[RED].single_symbol(), group[GREEN].single_symbol(), group[BLUE].single_symbol(), group[ALPHA].single_symbol()) {\n                (Some(r), Some(g), Some(b), Some(a)) if r < 256 && g < 256 && b < 256 && a < 256 => Some([r as u8, g as u8, b as u8, a as u8]),\n                _ => None,\n            };\n            single_pixels.push(single_pixel);\n            hufftree_groups.push(group);\n        }\n\n'''
 if old not in s:raise SystemExit('group end');s=s.replace(old,new,1)
 s=s.replace('''            huffman_code_groups: hufftree_groups,\n            run_ends,\n''','''            huffman_code_groups: hufftree_groups,\n            run_ends,\n            single_pixels,\n''',1)
 s=s.replace('''    run_ends: Vec<u16>,\n}\n''','''    run_ends: Vec<u16>,\n    single_pixels: Vec<Option<[u8; 4]>>,\n}\n''',1)
 oldfast='''                if tree[..4].iter().all(|t| t.is_single_node()) {\n                    let code = tree[GREEN].read_symbol(&mut self.bit_reader)?;\n                    if code < 256 {\n                        let n = if huffman_info.bits == 0 {\n                            num_values\n                        } else {\n                            next_block_start - index\n                        };\n\n                        let red = tree[RED].read_symbol(&mut self.bit_reader)?;\n                        let blue = tree[BLUE].read_symbol(&mut self.bit_reader)?;\n                        let alpha = tree[ALPHA].read_symbol(&mut self.bit_reader)?;\n                        let value = [red as u8, code as u8, blue as u8, alpha as u8];\n\n                        for i in 0..n {\n                            data[index * 4 + i * 4..][..4].copy_from_slice(&value);\n                        }\n\n                        if let Some(color_cache) = huffman_info.color_cache.as_mut() {\n                            color_cache.insert(value);\n                        }\n\n                        index += n;\n                        continue;\n                    }\n                }\n'''
 newfast='''                if let Some(value) = huffman_info.single_pixels[huff_index] {\n                    let n = if huffman_info.bits == 0 { num_values } else { next_block_start - index };\n                    for i in 0..n { data[index * 4 + i * 4..][..4].copy_from_slice(&value); }\n                    if let Some(color_cache) = huffman_info.color_cache.as_mut() { color_cache.insert(value); }\n                    index += n;\n                    continue;\n                }\n'''
 if oldfast not in s:raise SystemExit('fast marker');return s.replace(oldfast,newfast,1)
def patch(n,r):
 p=r/'src/lossless/decoder/mod.rs';s=p.read_text()
 if n=='scan':
  if OLD_ELSE not in s:raise SystemExit('else marker');s=s.replace(OLD_ELSE,SCAN_ELSE,1)
 else:
  s=add_precompute(s)
  if OLD_ELSE not in s:raise SystemExit('else marker');s=s.replace(OLD_ELSE,PRE_ELSE,1)
  if n=='pre_const':s=add_const(s,r)
 p.write_text(s)
def prep(n):
 r=TMP/n;run(['git','worktree','add','--detach',str(r),BASE])
 if n!='base':patch(n,r);run(['cargo','fmt'],cwd=r);run(['cargo','test','-q'],cwd=r);run(['cargo','+1.80.1','build','-q'],cwd=r)
 return r
def make(path,w,h,k):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    if k=='tiles':q=((x>>5)+3*(y>>5))&15;r=q*17;g=(q*53+(x&31)*3)&255;b=(q*91+(y&31)*5)&255
    elif k=='noise':z=(x*1103515245+y*12345+(x*y)*2654435761)&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
    else:r=(x*3+y*5+((x>>5)^(y>>4))*17)&255;g=(x*2+y*7+((x*y)>>10))&255;b=(x*11+y*3+((x+y)>>3)*9)&255
    i=x*3;row[i:i+3]=bytes((r,g,b))
   f.write(row)
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let a:Vec<_>=std::env::args().skip(1).collect();let m=&a[0];let n:usize=a[1].parse().unwrap();let x=std::fs::read(&a[2]).unwrap();if m=="h"{println!("{:x}",h(&x));return}for _ in 0..2{black_box(d(&x));}let t=Instant::now();for _ in 0..n{black_box(d(&x));}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/n as f64)}'''
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={n:prep(n)for n in['base',*VS]};files=[]
 for p in sorted((roots['base']/'tests/images').rglob('*.webp')):
  c=chunks(p.read_bytes())
  if b'VP8L'in c and b'ANIM'not in c:files.append(('corpus/'+p.name,p))
 for k in('structured','tiles','noise'):
  ppm=TMP/(k+'.ppm');webp=TMP/(k+'.webp');make(ppm,2048,1536,k);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);files.append(('gen/'+k,webp))
 bins={}
 for n,r in roots.items():
  (r/'examples').mkdir(exist_ok=True);(r/'examples/meta_skip.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','meta_skip','-q'],cwd=r,env=e);bins[n]=r/'target/release/examples/meta_skip'
 for label,p in files:
  bh=run([str(bins['base']),'h','1',str(p)],cap=True)
  for n in VS:
   cp=roots[n]/p.relative_to(roots['base']) if str(p).startswith(str(roots['base'])) else p
   if run([str(bins[n]),'h','1',str(cp)],cap=True)!=bh:raise SystemExit(f'hash mismatch {label} {n}')
 rows=[]
 for label,p in files:
  t=float(run([str(bins['base']),'t','1',str(p)],cap=True));it=max(2,min(500,math.ceil(50000/max(t,1.0))))
  for cand in VS:
   cp=roots[cand]/p.relative_to(roots['base']) if str(p).startswith(str(roots['base'])) else p;rr=[]
   for rnd in range(17):
    vals={};order=['base',cand]if rnd%2==0 else[cand,'base']
    for v in order:vals[v]=float(run([str(bins[v]),'t',str(it),str(p if v=='base' else cp)],cap=True))
    rr.append(vals['base']/vals[cand])
   rows.append((label,cand,statistics.median(rr),sum(x>1 for x in rr),min(rr),max(rr)))
 L=['# VP8L meta-Huffman run-skip matrix','',f'- baseline: `{BASE}`','- hashes + tests + Rust 1.80.1 pass','- 17 alternating paired rounds/file; ~50 ms target/sample','','| file | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for r in rows:L.append(f'| {r[0]} | {r[1]} | {r[2]:.4f}x | {r[3]}/17 | {r[4]:.4f}–{r[5]:.4f}x |')
 L+=['','## Aggregate','','| set | candidate | median file ratio | files >1 |','|---|---|---:|---:|']
 for g,prefix in [('corpus','corpus/'),('generated','gen/'),('all','')]:
  for c in VS:
   q=[r[2]for r in rows if r[1]==c and(not prefix or r[0].startswith(prefix))];L.append(f'| {g} | {c} | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} |')
 Path('benchmark-vp8l-meta-run-skip.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
