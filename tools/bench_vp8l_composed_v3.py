#!/usr/bin/env python3
import math, os, shutil, statistics, subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44'
CAND='4cd194935d100a09acf24eb24d8c1343c7844844'
TMP=Path('/tmp/vp8l-composed-v3')
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+n+(n&1)
 return o
def ppm(path,w,h,k):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    if k=='structured':r=(x*3+y*5+((x>>5)^(y>>4))*17)&255;g=(x*2+y*7+((x*y)>>10))&255;b=(x*11+y*3+((x+y)>>3)*9)&255
    elif k=='color':g=(x*5+y*9+((x*y)>>9))&255;r=(g*3+(x>>2))&255;b=(255-g+(y>>1))&255
    elif k=='corr':g=(x*7+y*11+((x*y)>>7))&255;r=(g+((x>>3)&15))&255;b=(g-((y>>3)&15))&255
    elif k=='stripes':r=(x*13)&255;g=((x//4)*47+y)&255;b=((x//11)*91+y*3)&255
    elif k=='tiles':q=((x>>5)+3*(y>>5))&15;r=q*17;g=(q*53+(x&31)*3)&255;b=(q*91+(y&31)*5)&255
    elif k=='gradient':r=x*255//max(1,w-1);g=y*255//max(1,h-1);b=(x+y)*255//max(1,w+h-2)
    else:z=(x*1103515245+y*12345+(x*y)*2654435761)&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
    i=x*3;row[i:i+3]=bytes((r,g,b))
   f.write(row)
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def paired(b,c,bf,cf,iters,rounds):
 ratios=[];bs=[];cs=[]
 for r in range(rounds):
  vals={};order=('base','cand') if r%2==0 else ('cand','base')
  for v in order:
   x=b if v=='base' else c; fs=bf if v=='base' else cf
   vals[v]=float(run(['taskset','-c','0',str(x),'t',str(iters),*[str(p)for p in fs]],cap=True))
  bs.append(vals['base']);cs.append(vals['cand']);ratios.append(vals['base']/vals['cand'])
 return statistics.median(bs),statistics.median(cs),statistics.median(ratios),sum(x>1 for x in ratios),min(ratios),max(ratios)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();base=TMP/'base';cand=TMP/'cand';run(['git','worktree','add','--detach',str(base),BASE]);run(['git','worktree','add','--detach',str(cand),CAND])
 run(['cargo','test','-q'],cwd=cand);run(['cargo','doc','--no-deps','-q'],cwd=cand);run(['cargo','clippy','--','-D','warnings'],cwd=cand);run(['cargo','fmt','--','--check'],cwd=cand);run(['cargo','+1.80.1','build','-q'],cwd=cand)
 repo=[]
 for p in sorted((base/'tests/images').rglob('*.webp')):
  c=chunks(p.read_bytes())
  if b'VP8L'in c and b'ANIM'not in c:repo.append(p)
 generated=[]
 specs=[('structured',2048,2048,[0,9]),('color',1536,1536,[0,9]),('corr',1536,1536,[0,9]),('stripes',1536,1024,[9]),('tiles',1536,1024,[9]),('gradient',1536,1024,[9]),('noise',1024,1024,[9])]
 for k,w,h,zs in specs:
  src=TMP/f'{k}.ppm';ppm(src,w,h,k)
  for z in zs:
   q=TMP/f'{k}-z{z}.webp';run(['cwebp','-quiet','-lossless','-z',str(z),str(src),'-o',str(q)]);generated.append((f'{k}-z{z}',q))
 for r in (base,cand):
  (r/'examples').mkdir(exist_ok=True);(r/'examples/composed_bench.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','composed_bench','-q'],cwd=r,env=e)
 b=base/'target/release/examples/composed_bench';c=cand/'target/release/examples/composed_bench';crepo=[cand/p.relative_to(base) for p in repo]
 if run([str(b),'h','1',*[str(p)for p in repo]],cap=True)!=run([str(c),'h','1',*[str(p)for p in crepo]],cap=True):raise SystemExit('repo hash mismatch')
 for _,p in generated:
  if run([str(b),'h','1',str(p)],cap=True)!=run([str(c),'h','1',str(p)],cap=True):raise SystemExit('generated hash mismatch '+p.name)
 agg=[]
 agg.append(('repo-corpus',*paired(b,c,repo,crepo,80,25)))
 large=[p for n,p in generated if n=='structured-z9'];agg.append(('large-structured-z9',*paired(b,c,large,large,5,25)))
 normal=[p for n,p in generated if n.endswith('z9')];agg.append(('generated-z9',*paired(b,c,normal,normal,4,25)))
 controls=[p for n,p in generated if n.endswith('z0')];agg.append(('generated-z0-controls',*paired(b,c,controls,controls,4,25)))
 rows=[]
 for p,cp in zip(repo,crepo):
  t=float(run([str(b),'t','1',str(p)],cap=True));it=max(2,min(500,math.ceil(50000/max(t,1))));rows.append(('repo/'+p.name,*paired(b,c,[p],[cp],it,13)))
 for n,p in generated:
  t=float(run([str(b),'t','1',str(p)],cap=True));it=max(2,min(500,math.ceil(50000/max(t,1))));rows.append(('gen/'+n,*paired(b,c,[p],[p],it,13)))
 cpu=run(['bash','-lc',"lscpu | sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
 L=['# Clean VP8L composed v3 benchmark','',f'- baseline: `{BASE}`',f'- candidate: `{CAND}`',f'- CPU: `{cpu}`','- candidate tree differs from baseline in production `mod.rs` + `reverse_transform.rs` only','- hashes match; tests/docs/Clippy/fmt/MSRV build pass','- aggregate workloads: 25 alternating paired rounds; per-file: 13 rounds','','## Aggregate','','| workload | base us | candidate us | paired median | positive | range |','|---|---:|---:|---:|---:|---:|']
 for x in agg:L.append(f'| {x[0]} | {x[1]:.3f} | {x[2]:.3f} | {x[3]:.4f}x | {x[4]}/25 | {x[5]:.4f}–{x[6]:.4f}x |')
 L+=['','## Per-file','','| file | base us | candidate us | paired median | positive | range |','|---|---:|---:|---:|---:|---:|']
 for x in rows:L.append(f'| {x[0]} | {x[1]:.3f} | {x[2]:.3f} | {x[3]:.4f}x | {x[4]}/13 | {x[5]:.4f}–{x[6]:.4f}x |')
 ratios=[x[3] for x in rows];L+=['','## Breadth','',f'- per-file median ratio: **{statistics.median(ratios):.4f}x**',f'- files positive: **{sum(x>1 for x in ratios)}/{len(ratios)}**']
 Path('benchmark-vp8l-composed-v3.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
