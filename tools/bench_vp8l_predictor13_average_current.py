#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='4f322d44fb38747659451db3d7f1dac7ff8ff21f';TMP=Path('/tmp/vp8l-p13-average');VS=('base','avg','autovec')
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
def patch(r,v):
 p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text()
 fn='average2' if v=='avg' else 'average2_autovec'
 for i in range(4):
  old=f'(i16::from(prev[{i}]) + i16::from(t[{i}])) / 2'
  new=f'i16::from({fn}(prev[{i}], t[{i}]))'
  assert old in s;s=s.replace(old,new,1)
 p.write_text(s)
def inv(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for v in VS:
  r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
  if v!='base':
   patch(r,v);run(['cargo','fmt'],cwd=r)
   for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
  (r/'examples').mkdir(exist_ok=True);(r/'examples/p13.rs').write_text(BENCH);run(['cargo','build','--release','--example','p13','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/p13'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)];corpus={v:[roots[v]/x for x in rels]for v in VS};hotrels=[Path('tests/images/gallery2/1_webp_ll.webp'),Path('tests/images/gallery2/3_webp_ll.webp')];hot={v:[roots[v]/x for x in hotrels]for v in VS}
 bh=inv(exes['base'],'h',1,corpus['base'])
 for v in VS[1:]:assert bh==inv(exes[v],'h',1,corpus[v])
 results={}
 for name,files,it in [('corpus',corpus,70),('p13hot',hot,40)]:
  rows=[]
  for n in range(17):
   order=VS if n%2==0 else tuple(reversed(VS));z={}
   for v in order:z[v]=float(inv(exes[v],'t',it,files[v]))
   rows.append(z)
  results[name]=rows
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L predictor13 average current-tree matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- replaces predictor13 i16 add/divide average with equivalent byte average; hashes + full verification passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for name,rows in results.items():
  for v in VS[1:]:q=[z['base']/z[v]for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-predictor13-average-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
