#!/usr/bin/env python3
import math, os, shutil, statistics, subprocess
from pathlib import Path

BASE='4cd194935d100a09acf24eb24d8c1343c7844844'
TMP=Path('/tmp/vp8l-group-root-selectors')
HERE=Path(__file__).resolve().parent
ROUNDS=11
VARIANTS=('base','never','q16','q8','q4')
MATS=(HERE/'materialize_vp8l_group_huffman.py',HERE/'materialize_vp8l_group_parse.py',HERE/'materialize_vp8l_group_decode.py')
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
    if k=='structured':q=((x>>5)+3*(y>>5))&15;r=q*17;g=(q*53+(x&31)*3)&255;b=(q*91+(y&31)*5)&255
    elif k=='corr':g=(x*7+y*11+((x*y)>>7))&255;r=(g+((x>>3)&15))&255;b=(g-((y>>3)&15))&255
    elif k=='noise':z=(x*1103515245+y*12345+(x*y)*2654435761+0x9e3779b9)&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
    elif k=='gradient':r=x*255//max(1,w-1);g=y*255//max(1,h-1);b=(x+y)*255//max(1,w+h-2)
    else:r=(x*11+y*3)&255;g=(x*5+y*13)&255;b=(r+g*3)&255
    row+=bytes((r,g,b))
   f.write(row)
def inv(exe,mode,n,ps):return run(['taskset','-c','0',str(exe),mode,str(n),*[str(x)for x in ps]],cap=True)
def prep(name):
 root=TMP/name;run(['git','worktree','add','--detach',str(root),BASE])
 if name!='base':
  for m in MATS:run(['python3',str(m)],cwd=root)
  p=root/'src/lossless/decoder/mod.rs';s=p.read_text()
  if name=='never':s=s.replace('let use_wide_root = specs.iter().any(HuffmanCodeSpec::prefers_wide_root);','let use_wide_root = false;')
  elif name!='q8':s=s.replace('long_symbols * 8 >= symbols',f'long_symbols * {name[1:]} >= symbols')
  p.write_text(s);run(['cargo','fmt'],cwd=root);run(['git','diff','--check'],cwd=root)
 (root/'examples').mkdir(exist_ok=True);(root/'examples/group_selector.rs').write_text(BENCH)
 env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','group_selector','-q'],cwd=root,env=env)
 return root,root/'target/release/examples/group_selector'
def paired(exes,files,it):
 vals={v:[] for v in VARIANTS};ratios={v:[] for v in VARIANTS if v!='base'}
 for r in range(ROUNDS):
  order=VARIANTS if r%2==0 else tuple(reversed(VARIANTS));z={}
  for v in order:z[v]=float(inv(exes[v],'t',it,files[v]));vals[v].append(z[v])
  for v in ratios:ratios[v].append(z['base']/z[v])
 return vals,ratios
def iters(exe,ps,target=150000,cap=80):
 probe=float(inv(exe,'t',1,ps));return max(1,min(cap,math.ceil(target/max(probe*len(ps),1))))
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={}
 for v in VARIANTS:roots[v],exes[v]=prep(v)
 gen={}
 for k in ('structured','gradient','corr','color','noise'):
  src=TMP/f'{k}.ppm';ppm(src,1536,1536,k)
  for z in(0,9):w=TMP/f'{k}-z{z}.webp';run(['cwebp','-quiet','-lossless','-z',str(z),str(src),'-o',str(w)]);gen[f'{k}-z{z}']=w
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
 files_repo={v:[roots[v]/r for r in rels] for v in VARIANTS}
 ref=inv(exes['base'],'h',1,files_repo['base'])
 for v in VARIANTS[1:]:
  if inv(exes[v],'h',1,files_repo[v])!=ref:raise SystemExit(f'{v} repo hash mismatch')
 gpaths=list(gen.values());gh=inv(exes['base'],'h',1,gpaths)
 for v in VARIANTS[1:]:
  if inv(exes[v],'h',1,gpaths)!=gh:raise SystemExit(f'{v} generated hash mismatch')
 workloads=[('repo-vp8l-corpus',files_repo,iters(exes['base'],files_repo['base'],180000,100))]
 for label in ('structured-z9','corr-z9','noise-z9'):
  p=gen[label];workloads.append((label,{v:[p] for v in VARIANTS},iters(exes['base'],[p],160000,20)))
 for z in(0,9):
  ps=[gen[f'{k}-z{z}']for k in('structured','gradient','corr','color','noise')];workloads.append((f'generated-z{z}-aggregate',{v:ps for v in VARIANTS},iters(exes['base'],ps,180000,12)))
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
 L=['# VP8L group-static root selector matrix','',f'- base: `{BASE}`',f'- CPU: `{cpu}`',f'- {ROUNDS} alternating/reversed rounds; hashes equal base','- `never`: group-static architecture but never selects 11-bit root','- `q16/q8/q4`: require >=256 non-zero symbols and at least 1/16, 1/8, or 1/4 of them longer than 9 bits','', '| workload | variant | median us | speedup vs base | positive rounds |','|---|---|---:|---:|---:|']
 for label,files,it in workloads:
  vals,ratios=paired(exes,files,it);L.append(f"| {label} | base | {statistics.median(vals['base']):.3f} | 1.0000x | 0/{ROUNDS} |")
  for v in VARIANTS[1:]:L.append(f"| {label} | {v} | {statistics.median(vals[v]):.3f} | **{statistics.median(ratios[v]):.4f}x** | {sum(x>1 for x in ratios[v])}/{ROUNDS} |")
 out='\n'.join(L)+'\n';Path('benchmark-vp8l-group-root-selectors.md').write_text(out);print(out)
if __name__=='__main__':main()
