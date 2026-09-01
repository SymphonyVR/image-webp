#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='4cd194935d100a09acf24eb24d8c1343c7844844';MAIN='f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f';TMP=Path('/tmp/vp8l-v3-regression')
VS=['root10','pred1_main','root10_pred1']
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+n+(n&1)
 return o
def replace_fn(dst,src,name,next_name):
 a=dst.index(f'pub fn {name}(');b=dst.index(f'pub fn {next_name}(',a);c=src.index(f'pub fn {name}(');d=src.index(f'pub fn {next_name}(',c);return dst[:a]+src[c:d]+dst[b:]
def patch(name,root):
 if 'root10' in name:
  p=root/'src/lossless/decoder/huffman.rs';s=p.read_text();old='const MAX_TABLE_BITS: u8 = 9;';assert old in s;p.write_text(s.replace(old,'const MAX_TABLE_BITS: u8 = 10;',1))
 if 'pred1' in name:
  p=root/'src/lossless/decoder/reverse_transform.rs';s=p.read_text();main=run(['git','show',f'{MAIN}:src/lossless/decoder/reverse_transform.rs'],cwd=root,cap=True);p.write_text(replace_fn(s,main,'apply_predictor_transform_1','apply_predictor_transform_2'))
def prep(name):
 r=TMP/name;run(['git','worktree','add','--detach',str(r),BASE])
 if name!='base':patch(name,r);run(['cargo','fmt'],cwd=r);run(['cargo','test','-q'],cwd=r);run(['cargo','doc','-q'],cwd=r);run(['cargo','clippy','--all-features','--','-D','warnings'],cwd=r);run(['cargo','fmt','--','--check'],cwd=r);run(['cargo','+1.80.1','build','-q'],cwd=r)
 return r
def make(path,w,h,kind):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    if kind=='structured':r=(x*3+y*5+((x>>5)^(y>>4))*17)&255;g=(x*2+y*7+((x*y)>>10))&255;b=(x*11+y*3+((x+y)>>3)*9)&255
    elif kind=='color':g=(x*9+y*13+((x>>3)^(y>>4))*21)&255;r=(g+((x*5-y*3)&255))&255;b=(g+((y*7-x*2)&255))&255
    elif kind=='corr':g=(x*7+y*11+((x>>4)^(y>>5))*19)&255;r=(g+((x+y)&31)-16)&255;b=(g+((x*3-y)&31)-16)&255
    elif kind=='stripes':q=((x>>4)^(y>>5))&7;r=q*31;g=(q*47)&255;b=(q*83)&255
    elif kind=='tiles':q=((x>>5)+3*(y>>5))&15;r=q*17;g=(q*53)&255;b=(q*91)&255
    elif kind=='gradient':r=(x*255//max(1,w-1));g=(y*255//max(1,h-1));b=((x+y)*255//max(1,w+h-2))
    else:z=(x*1103515245+y*12345+((x*y)*2654435761))&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
    i=x*3;row[i:i+3]=bytes((r,g,b))
   f.write(row)
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def build(r):
 (r/'examples').mkdir(exist_ok=True);(r/'examples/regfam.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','regfam','-q'],cwd=r,env=e);return r/'target/release/examples/regfam'
def inv(b,m,n,ps):return run(['taskset','-c','0',str(b),m,str(n),*[str(p)for p in ps]],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={n:prep(n)for n in ['base',*VS]};rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p.read_bytes())and b'ANIM'not in chunks(p.read_bytes())];bins={n:build(r)for n,r in roots.items()}
 fx={}
 for k in ('structured','color','corr','stripes','tiles','gradient','noise'):
  ppm=TMP/f'{k}.ppm';webp=TMP/f'{k}.webp';make(ppm,1536,1152,k);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);fx[k]=webp
 for n in VS:
  if inv(bins['base'],'h',1,[roots['base']/r for r in rels]+list(fx.values()))!=inv(bins[n],'h',1,[roots[n]/r for r in rels]+list(fx.values())):raise SystemExit(f'hash mismatch {n}')
 workloads={'corpus':([roots['base']/r for r in rels],70),'gen_z9':(list(fx.values()),12),'large':([fx['structured']],8)}
 rows=[]
 for rnd in range(1,18):
  order=['base',*VS] if rnd%2 else list(reversed(['base',*VS]))
  for w,(baseps,iters) in workloads.items():
   for n in order:
    ps=[roots[n]/p.relative_to(roots['base']) for p in baseps] if w=='corpus' else baseps
    rows.append((w,rnd,n,float(inv(bins[n],'t',iters,ps))))
 vals={};pairs={}
 for w,r,n,x in rows:vals.setdefault((w,n),[]).append(x);pairs.setdefault((w,r),{})[n]=x
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L v3 regression-family isolation','',f'- baseline: `{BASE}`',f'- main reference: `{MAIN}`',f'- CPU: `{cpu}`','- 17 paired rounds; candidate hashes/tests/docs/Clippy/fmt/MSRV passed','','| workload | candidate | base median | candidate median | paired speedup | positive | range |','|---|---|---:|---:|---:|---:|---:|']
 for w in workloads:
  for n in VS:
   q=[z['base']/z[n]for(ww,_),z in sorted(pairs.items())if ww==w];L.append(f'| {w} | {n} | {statistics.median(vals[w,"base"]):.3f} us | {statistics.median(vals[w,n]):.3f} us | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-v3-regression-families.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
