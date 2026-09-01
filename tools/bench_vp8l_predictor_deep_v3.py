#!/usr/bin/env python3
import importlib.util, math, os, shutil, statistics
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('pc',HERE/'bench_vp8l_predictor_closure.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.TMP=Path('/tmp/vp8l-predictor-deep-v3');m.VS=['direct','avg','packed']
TMP=m.TMP;VS=m.VS
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let a:Vec<_>=std::env::args().skip(1).collect();let mode=&a[0];let n:usize=a[1].parse().unwrap();let x=std::fs::read(&a[2]).unwrap();if mode=="h"{println!("{:x}",h(&x));return}for _ in 0..2{black_box(d(&x));}let t=Instant::now();for _ in 0..n{black_box(d(&x));}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/n as f64)}'''
def ppm(path,w,h,k):
 with path.open('wb') as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    if k=='gradient':r=x*255//max(1,w-1);g=y*255//max(1,h-1);b=(x+y)*255//max(1,w+h-2)
    elif k=='corr':g=(x*7+y*11+((x*y)>>7))&255;r=(g+((x>>3)&15))&255;b=(g-((y>>3)&15))&255
    elif k=='stripes':r=(x*13)&255;g=((x//4)*47+y)&255;b=((x//11)*91+y*3)&255
    elif k=='tiles':q=((x>>5)+3*(y>>5))&15;r=q*17;g=(q*53+(x&31)*3)&255;b=(q*91+(y&31)*5)&255
    elif k=='smooth':r=(x//4+y//8)&255;g=(x//6+y//5)&255;b=(x//9+y//3)&255
    else:z=(x*1103515245+y*12345+(x*y)*2654435761)&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
    i=x*3;row[i:i+3]=bytes((r,g,b))
   f.write(row)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={n:m.prep(n)for n in['base',*VS]};files=[]
 for p in sorted((roots['base']/'tests/images').rglob('*.webp')):
  c=m.chunks(p.read_bytes())
  if b'VP8L'in c and b'ANIM'not in c:files.append(('corpus/'+p.name,p))
 for k in('gradient','corr','stripes','tiles','smooth','noise'):
  p=TMP/(k+'.ppm');ppm(p,1536,1024,k)
  for z in (0,3,6,9):
   q=TMP/f'{k}-z{z}.webp';m.run(['cwebp','-quiet','-lossless','-z',str(z),str(p),'-o',str(q)]);files.append((f'gen/{k}-z{z}',q))
 bins={}
 for n,r in roots.items():
  (r/'examples').mkdir(exist_ok=True);(r/'examples/pred_deep.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';m.run(['cargo','build','--release','--example','pred_deep','-q'],cwd=r,env=e);bins[n]=r/'target/release/examples/pred_deep'
 for label,p in files:
  bh=m.run([str(bins['base']),'h','1',str(p)],cap=True)
  for n in VS:
   cp=roots[n]/p.relative_to(roots['base']) if str(p).startswith(str(roots['base'])) else p
   if m.run([str(bins[n]),'h','1',str(cp)],cap=True)!=bh:raise SystemExit(f'hash mismatch {label} {n}')
 rows=[]
 for label,p in files:
  t=float(m.run([str(bins['base']),'t','1',str(p)],cap=True));it=max(2,min(500,math.ceil(45000/max(1,t))))
  for cand in VS:
   cp=roots[cand]/p.relative_to(roots['base']) if str(p).startswith(str(roots['base'])) else p;rr=[]
   for rnd in range(13):
    vals={};order=['base',cand]if rnd%2==0 else[cand,'base']
    for v in order:vals[v]=float(m.run([str(bins[v]),'t',str(it),str(p if v=='base' else cp)],cap=True))
    rr.append(vals['base']/vals[cand])
   rows.append((label,cand,statistics.median(rr),sum(x>1 for x in rr),min(rr),max(rr)))
 L=['# VP8L deep predictor matrix','',f'- baseline: `{m.BASE}`','- candidates: direct packed modes 2–4; average packed modes 5–10; combined packed modes 2–10','- hashes + tests + Rust 1.80.1 pass','- 13 alternating paired rounds/file; ~45 ms/sample','','| file | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for r in rows:L.append(f'| {r[0]} | {r[1]} | {r[2]:.4f}x | {r[3]}/13 | {r[4]:.4f}–{r[5]:.4f}x |')
 L+=['','## Aggregate','','| set | candidate | median file ratio | files >1 |','|---|---|---:|---:|']
 for g,prefix in [('corpus','corpus/'),('generated','gen/'),('all','')]:
  for c in VS:
   q=[r[2]for r in rows if r[1]==c and(not prefix or r[0].startswith(prefix))];L.append(f'| {g} | {c} | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} |')
 Path('benchmark-vp8l-predictor-deep-v3.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
