#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='0881ec1a66f09e11b766c309cf6e651077775bd9';TMP=Path('/tmp/vp8l-cache-current-final');VS=('base','hash','packed','both')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let p:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=p.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(p):
 d=p.read_bytes();o=[];q=12
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return o
 while q+8<=len(d):t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
 return o
def patch(r,v):
 p=r/'src/lossless/decoder/mod.rs';s=p.read_text()
 if v in('hash','both'):
  old='''        let [r, g, b, a] = color;\n        let color_u32 =\n            (u32::from(r) << 16) | (u32::from(g) << 8) | (u32::from(b)) | (u32::from(a) << 24);\n''';new='''        let [r, g, b, a] = color;\n        let color_u32 = u32::from_be_bytes([a, r, g, b]);\n''';assert old in s;s=s.replace(old,new,1)
 if v in('packed','both'):
  s=s.replace('color_cache: vec![[0; 4]; 1 << bits],','color_cache: vec![0; 1 << bits],',1).replace('color_cache: Vec<[u8; 4]>,','color_cache: Vec<u32>,',1)
  old='''        self.color_cache[index as usize] = color;\n    }\n\n    #[inline(always)]\n    fn lookup(&self, index: usize) -> [u8; 4] {\n        self.color_cache[index]\n''';new='''        self.color_cache[index as usize] = u32::from_le_bytes(color);\n    }\n\n    #[inline(always)]\n    fn lookup(&self, index: usize) -> [u8; 4] {\n        self.color_cache[index].to_le_bytes()\n''';assert old in s;s=s.replace(old,new,1)
 p.write_text(s)
def inv(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for v in VS:
  r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
  if v!='base':
   patch(r,v);run(['cargo','fmt'],cwd=r)
   for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q']):run(c,cwd=r)
  (r/'examples').mkdir(exist_ok=True);(r/'examples/cachec.rs').write_text(BENCH);run(['cargo','build','--release','--example','cachec','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/cachec'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
 ppm=TMP/'large.ppm';w=h=2048
 with ppm.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):i=x*3;row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
   f.write(row)
 large=TMP/'large.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(large)])
 corpus={v:[roots[v]/x for x in rels]for v in VS};bh=inv(exes['base'],'h',1,corpus['base']+[large])
 for v in VS[1:]:assert bh==inv(exes[v],'h',1,corpus[v]+[large])
 workloads={'corpus':(corpus,70),'large':({v:[large]for v in VS},4)};res={}
 for name,(files,it)in workloads.items():
  rows=[]
  for n in range(17):
   order=VS if n%2==0 else tuple(reversed(VS));z={}
   for v in order:z[v]=float(inv(exes[v],'t',it,files[v]))
   rows.append(z)
  res[name]=rows
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L cache representation current-final matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for name,rows in res.items():
  for v in VS[1:]:q=[z['base']/z[v]for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-cache-current-final.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
