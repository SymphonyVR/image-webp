#!/usr/bin/env python3
import math,os,shutil,statistics,subprocess
from pathlib import Path
MAIN='f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f';BASE='4cd194935d100a09acf24eb24d8c1343c7844844';CAND='87f1f0c625b5169bd9162aaa02d1c97e68a20cf4';TMP=Path('/tmp/confirm-vp8l-wide-root-final')
V=[('main',MAIN),('base',BASE),('candidate',CAND)]
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn one(d:&[u8])->u64{let mut q=WebPDecoder::new(Cursor::new(d)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();let mut h=0xcbf29ce484222325u64;for &z in&b{h=(h^z as u64).wrapping_mul(1099511628211)}black_box(h)}fn main(){let a:Vec<_>=std::env::args().skip(1).collect();let m=&a[0];let n:usize=a[1].parse().unwrap();let ds:Vec<Vec<u8>>=a[2..].iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for d in&ds{println!("{:016x}",one(d))}return}for d in&ds{black_box(one(d));}let t=Instant::now();for _ in 0..n{for d in&ds{black_box(one(d));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(p):
 d=p.read_bytes();o=[];q=12
 if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP':return o
 while q+8<=len(d):t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
 return o
def ppm(path,w,h,k):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode())
  for y in range(h):
   row=bytearray()
   for x in range(w):
    if k=='gradient':r=x*255//(w-1);g=y*255//(h-1);b=(x+y)*255//(w+h-2)
    elif k=='corr':g=(x*7+y*11+((x*y)>>7))&255;r=(g+((x>>3)&15))&255;b=(g-((y>>3)&15))&255
    elif k=='color':r=(x*11+y*3)&255;g=(x*5+y*13)&255;b=(r+g*3)&255
    elif k=='structured':q=((x>>5)+3*(y>>5))&15;r=q*17;g=(q*53+(x&31)*3)&255;b=(q*91+(y&31)*5)&255
    else:z=(x*1103515245+y*12345+(x*y)*2654435761+0x9e3779b9)&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
    row+=bytes((r,g,b))
   f.write(row)
def inv(exe,mode,n,ps):return run(['taskset','-c','0',str(exe),mode,str(n),*[str(x)for x in ps]],cap=True)
def paired(exes,files,iters,rounds=17):
 samples={n:[]for n,_ in V};pairs={}
 names=[n for n,_ in V]
 for r in range(rounds):
  order=names if r%2==0 else list(reversed(names));z={}
  for n in order:z[n]=float(inv(exes[n],'t',iters,files[n]))
  for n in names:samples[n].append(z[n]);pairs[r]=z
 return {n:statistics.median(x)for n,x in samples.items()},pairs
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for n,sha in V:
  r=TMP/n;roots[n]=r;run(['git','worktree','add','--detach',str(r),sha]);(r/'examples').mkdir(exist_ok=True);(r/'examples/wide_confirm.rs').write_text(BENCH);run(['cargo','build','--release','--example','wide_confirm','-q'],cwd=r,env=env);exes[n]=r/'target/release/examples/wide_confirm'
 generated={}
 for k in ('structured','gradient','corr','color','noise'):
  src=TMP/f'{k}.ppm';ppm(src,2048,2048,k)
  for z in(0,9):w=TMP/f'{k}-z{z}.webp';run(['cwebp','-quiet','-lossless','-z',str(z),str(src),'-o',str(w)]);generated[f'{k}-z{z}']=w
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
 # Candidate must be byte-identical to the already validated composed base on all benchmark streams.
 base_ps=[roots['base']/r for r in rels];cand_ps=[roots['candidate']/r for r in rels]
 assert inv(exes['base'],'h',1,base_ps)==inv(exes['candidate'],'h',1,cand_ps)
 assert inv(exes['base'],'h',1,list(generated.values()))==inv(exes['candidate'],'h',1,list(generated.values()))
 workloads=[]
 for label,p in generated.items():
  probe=float(inv(exes['base'],'t',1,[p]));it=max(1,min(20,math.ceil(120000/max(probe,1))));files={n:[p]for n,_ in V};med,pairs=paired(exes,files,it);workloads.append((label,med,pairs))
 for z in(0,9):
  ps=[generated[f'{k}-z{z}']for k in ('structured','gradient','corr','color','noise')];probe=float(inv(exes['base'],'t',1,ps));it=max(1,min(12,math.ceil(150000/max(probe*len(ps),1))));files={n:ps for n,_ in V};med,pairs=paired(exes,files,it);workloads.append((f'generated-z{z}-aggregate',med,pairs))
 files={n:[roots[n]/r for r in rels]for n,_ in V};probe=float(inv(exes['base'],'t',1,files['base']));it=max(1,min(100,math.ceil(180000/max(probe*len(rels),1))));med,pairs=paired(exes,files,it);workloads.append(('repo-vp8l-corpus',med,pairs))
 run(['curl','-L','--fail','--retry','3','-o',str(TMP/'sample.zip'),'https://github.com/user-attachments/files/17482915/sample.zip']);(TMP/'issue').mkdir();run(['unzip','-q',str(TMP/'sample.zip'),'-d',str(TMP/'issue')]);issue=next((TMP/'issue').rglob('*.webp'));files={n:[issue]for n,_ in V};probe=float(inv(exes['base'],'t',1,[issue]));it=max(1,min(10,math.ceil(180000/max(probe,1))));med,pairs=paired(exes,files,it);workloads.append(('issue119',med,pairs))
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
 L=['# Final VP8L wide-root confirmation','',f'- main: `{MAIN}`',f'- composed base: `{BASE}`',f'- candidate: `{CAND}`',f'- CPU: `{cpu}`','- release native, CPU 0 pinned, 17 alternating/reversed 3-way rounds','- candidate hashes == validated composed-base hashes on repository VP8L corpus and every generated stream','', '| workload | main us | base us | candidate us | candidate/main | candidate/base | cand>main | cand>base |','|---|---:|---:|---:|---:|---:|---:|---:|']
 for label,med,pairs in workloads:
  qm=[z['main']/z['candidate']for _,z in sorted(pairs.items())];qb=[z['base']/z['candidate']for _,z in sorted(pairs.items())];L.append(f"| {label} | {med['main']:.3f} | {med['base']:.3f} | {med['candidate']:.3f} | **{statistics.median(qm):.4f}x** | **{statistics.median(qb):.4f}x** | {sum(x>1 for x in qm)}/17 | {sum(x>1 for x in qb)}/17 |")
 Path('benchmark-vp8l-wide-root-confirm-final.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
