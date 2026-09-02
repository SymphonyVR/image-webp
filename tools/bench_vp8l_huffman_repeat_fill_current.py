#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='84d8d20753fce0a9972e8a244fdf929b5a55671c';TMP=Path('/tmp/vp8l-huffman-repeat-fill');VS=('base','fill')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(p):
 d=p.read_bytes();o=[];q=12
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return o
 while q+8<=len(d):t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
 return o
def patch(r):
 p=r/'src/lossless/decoder/mod.rs';s=p.read_text();old='''                let mut repeat = self.bit_reader.read_bits::<u16>(extra_bits)? + repeat_offset;\n\n                if symbol + repeat > num_symbols {\n                    return Err(DecodingError::BitStreamError);\n                }\n\n                let length = if use_prev { prev_code_len } else { 0 };\n                while repeat > 0 {\n                    repeat -= 1;\n                    code_lengths[usize::from(symbol)] = length;\n                    symbol += 1;\n                }\n''';new='''                let repeat = self.bit_reader.read_bits::<u16>(extra_bits)? + repeat_offset;\n                let end = symbol\n                    .checked_add(repeat)\n                    .ok_or(DecodingError::BitStreamError)?;\n                if end > num_symbols {\n                    return Err(DecodingError::BitStreamError);\n                }\n\n                let length = if use_prev { prev_code_len } else { 0 };\n                code_lengths[usize::from(symbol)..usize::from(end)].fill(length);\n                symbol = end;\n''';assert old in s;p.write_text(s.replace(old,new,1))
def inv(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for v in VS:
  r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
  if v!='base':
   patch(r);run(['cargo','fmt'],cwd=r)
   for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
  (r/'examples').mkdir(exist_ok=True);(r/'examples/hrep.rs').write_text(BENCH);run(['cargo','build','--release','--example','hrep','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/hrep'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
 ppm=TMP/'large.ppm';w=h=2048
 with ppm.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):i=x*3;row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
   f.write(row)
 large=TMP/'large.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(large)])
 corpus={v:[roots[v]/x for x in rels]for v in VS};assert inv(exes['base'],'h',1,corpus['base']+[large])==inv(exes['fill'],'h',1,corpus['fill']+[large])
 results={}
 for name,files,it in [('corpus',corpus,80),('large',{v:[large]for v in VS},4)]:
  q=[]
  for n in range(17):
   order=VS if n%2==0 else tuple(reversed(VS));z={v:float(inv(exes[v],'t',it,files[v])) for v in order};q.append(z['base']/z['fill'])
  results[name]=q
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L Huffman repeat-fill current-tree benchmark','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- replaces scalar repeat-code writes with slice fill; full verification passed','','| workload | paired median | positive | range |','|---|---:|---:|---:|']
 for name,q in results.items():L.append(f'| {name} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-huffman-repeat-fill-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
