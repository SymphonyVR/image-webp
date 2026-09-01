#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44';TMP=Path('/tmp/vp8l-huff-scratch');VS=['reuse','sorted','reuse_sorted','all']
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def patch(n,r):
 hp=r/'src/lossless/decoder/huffman.rs';mp=r/'src/lossless/decoder/mod.rs';h=hp.read_text();m=mp.read_text()
 def slice_build():
  nonlocal h
  old='pub(crate) fn build_implicit(code_lengths: Vec<u16>) -> Result<Self, DecodingError> {';new='pub(crate) fn build_implicit(code_lengths: &[u16]) -> Result<Self, DecodingError> {'
  if old not in h:raise SystemExit('slice marker');h=h.replace(old,new,1)
 def reuse():
  nonlocal h,m
  slice_build();m=m.replace('let mut hufftree_groups = Vec::new();','let mut hufftree_groups = Vec::new();\n        let mut code_lengths_scratch = Vec::new();',1);m=m.replace('let tree = self.read_huffman_code(alphabet_size)?;','let tree = self.read_huffman_code(alphabet_size, &mut code_lengths_scratch)?;',1);m=m.replace('fn read_huffman_code(&mut self, alphabet_size: u16) -> Result<HuffmanTree, DecodingError> {','fn read_huffman_code(&mut self, alphabet_size: u16, code_lengths_scratch: &mut Vec<u16>) -> Result<HuffmanTree, DecodingError> {',1);m=m.replace('let mut code_length_code_lengths = vec![0; CODE_LENGTH_CODES];','let mut code_length_code_lengths = [0u16; CODE_LENGTH_CODES];',1)
  old='''            let new_code_lengths =\n                self.read_huffman_code_lengths(code_length_code_lengths, alphabet_size)?;\n\n            HuffmanTree::build_implicit(new_code_lengths)\n''';new='''            self.read_huffman_code_lengths(&code_length_code_lengths, alphabet_size, code_lengths_scratch)?;\n            HuffmanTree::build_implicit(code_lengths_scratch.as_slice())\n'''
  if old not in m:raise SystemExit('read marker');m=m.replace(old,new,1)
  old='''        code_length_code_lengths: Vec<u16>,\n        num_symbols: u16,\n    ) -> Result<Vec<u16>, DecodingError> {\n        let table = HuffmanTree::build_implicit(code_length_code_lengths)?;''';new='''        code_length_code_lengths: &[u16],\n        num_symbols: u16,\n        code_lengths: &mut Vec<u16>,\n    ) -> Result<(), DecodingError> {\n        let table = HuffmanTree::build_implicit(code_length_code_lengths)?;'''
  if old not in m:raise SystemExit('sig marker');m=m.replace(old,new,1)
  m=m.replace('''        let mut code_lengths = vec![0; usize::from(num_symbols)];\n        let mut prev_code_len = 8; //default code length\n''','''        code_lengths.clear();\n        code_lengths.resize(usize::from(num_symbols), 0);\n        let mut prev_code_len = 8; //default code length\n''',1);m=m.replace('''        Ok(code_lengths)\n    }\n\n    /// Decodes the image data''','''        Ok(())\n    }\n\n    /// Decodes the image data''',1)
 def sorted_stack():
  nonlocal h
  old='''        let mut next_index = offsets;\n        let mut sorted_symbols = vec![0u16; code_lengths.len()];\n        for symbol in 0..code_lengths.len() {\n''';new='''        let mut next_index = offsets;\n        let mut sorted_stack = [0u16; 512];\n        let mut sorted_heap = Vec::new();\n        let sorted_symbols: &mut [u16] = if code_lengths.len() <= sorted_stack.len() {\n            &mut sorted_stack[..code_lengths.len()]\n        } else {\n            sorted_heap.resize(code_lengths.len(), 0);\n            sorted_heap.as_mut_slice()\n        };\n        for symbol in 0..code_lengths.len() {\n'''
  if old not in h:raise SystemExit('sorted marker');h=h.replace(old,new,1)
 if n in ('reuse','reuse_sorted','all'):reuse()
 if n in ('sorted','reuse_sorted','all'):
  if n=='sorted':slice_build()
  sorted_stack()
  if n=='sorted':
   m=m.replace('HuffmanTree::build_implicit(code_length_code_lengths)?','HuffmanTree::build_implicit(&code_length_code_lengths)?',1);m=m.replace('HuffmanTree::build_implicit(new_code_lengths)','HuffmanTree::build_implicit(&new_code_lengths)',1)
 if n=='all':m=m.replace('let mut hufftree_groups = Vec::new();','let mut hufftree_groups = Vec::with_capacity(num_huff_groups as usize);',1)
 hp.write_text(h);mp.write_text(m)
def prep(n):
 r=TMP/n;run(['git','worktree','add','--detach',str(r),BASE]);
 if n!='base':patch(n,r);run(['cargo','fmt'],cwd=r);run(['cargo','test','-q'],cwd=r);run(['cargo','+1.80.1','build','-q'],cwd=r)
 return r
def ch(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];z=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+z+(z&1)
 return o
def corp(r):return[p.relative_to(r)for p in sorted((r/'tests/images').rglob('*.webp'))if b'VP8L'in ch(p.read_bytes())and b'ANIM'not in ch(p.read_bytes())]
BENCH='''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def build(r):
 (r/'examples').mkdir(exist_ok=True);(r/'examples/hs2.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','hs2','-q'],cwd=r,env=e);return r/'target/release/examples/hs2'
def inv(b,m,n,ps):return run(['taskset','-c','0',str(b),m,str(n),*[str(x)for x in ps]],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={n:prep(n)for n in ['base',*VS]};rels=corp(roots['base']);ppm=TMP/'large.ppm';w=h=1536
 with ppm.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):i=x*3;row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
   f.write(row)
 webp=TMP/'large.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);bins={n:build(r)for n,r in roots.items()};bh=inv(bins['base'],'h',1,[*[roots['base']/r for r in rels],webp])
 for n in VS:
  if inv(bins[n],'h',1,[*[roots[n]/r for r in rels],webp])!=bh:raise SystemExit('hash '+n)
 rows=[]
 for rnd in range(1,12):
  order=['base',*VS]if rnd%2 else[*reversed(VS),'base']
  for n in order:rows.append(('corpus',rnd,n,float(inv(bins[n],'bench',50,[roots[n]/r for r in rels]))));rows.append(('large',rnd,n,float(inv(bins[n],'bench',3,[webp]))))
 rr={}
 for w,r,n,x in rows:rr.setdefault((w,r),{})[n]=x
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L Huffman scratch closure','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + MSRV passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for w in('corpus','large'):
  for n in VS:q=[z['base']/z[n]for(ww,_),z in sorted(rr.items())if ww==w];L.append(f'| {w} | {n} | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-huffman-scratch-v2.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
