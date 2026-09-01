#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='58dba70a93fef7883c934e28465e04534278fb80';MAIN='f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f';TMP=Path('/tmp/vp8l-mod-lineage')
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip() if cap else subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+n+(n&1)
 return o
def prep(n):
 r=TMP/n;run(['git','worktree','add','--detach',str(r),BASE])
 if n!='current':(r/'src/lossless/decoder/mod.rs').write_text(run(['git','show',f'{MAIN}:src/lossless/decoder/mod.rs'],cwd=r,cap=True));run(['cargo','fmt'],cwd=r);run(['cargo','test','-q'],cwd=r);run(['cargo','+1.80.1','build','-q'],cwd=r)
 return r
def make(p,w,h,k):
 with p.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    if k=='structured':a=(x*3+y*5+((x>>5)^(y>>4))*17)&255;b=(x*2+y*7+((x*y)>>10))&255;c=(x*11+y*3+((x+y)>>3)*9)&255
    elif k=='tiles':q=((x>>5)+3*(y>>5))&15;a=q*17;b=(q*53)&255;c=(q*91)&255
    else:z=(x*1103515245+y*12345+((x*y)*2654435761))&0xffffffff;a=(z>>8)&255;b=(z>>16)&255;c=(z>>24)&255
    i=x*3;row[i:i+3]=bytes((a,b,c))
   f.write(row)
B=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def build(r):
 (r/'examples').mkdir(exist_ok=True);(r/'examples/ml.rs').write_text(B);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','ml','-q'],cwd=r,env=e);return r/'target/release/examples/ml'
def inv(b,m,n,ps):return run(['taskset','-c','0',str(b),m,str(n),*[str(x)for x in ps]],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={n:prep(n)for n in('current','mainmod')};bins={n:build(r)for n,r in roots.items()};rels=[p.relative_to(roots['current'])for p in sorted((roots['current']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p.read_bytes())and b'ANIM'not in chunks(p.read_bytes())];fx=[]
 for k in('structured','tiles','noise'):
  ppm=TMP/f'{k}.ppm';w=TMP/f'{k}.webp';make(ppm,1536,1152,k);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(w)]);fx.append(w)
 assert inv(bins['current'],'h',1,[roots['current']/r for r in rels]+fx)==inv(bins['mainmod'],'h',1,[roots['mainmod']/r for r in rels]+fx)
 wl={'corpus':(rels,80),'gen_z9':(fx,15),'structured':([fx[0]],8)};rows=[]
 for rnd in range(1,18):
  order=('current','mainmod')if rnd%2 else('mainmod','current')
  for w,(items,iters) in wl.items():
   for n in order:rows.append((w,rnd,n,float(inv(bins[n],'t',iters,[roots[n]/r for r in items]if w=='corpus'else items))))
 vals={};pairs={}
 for w,r,n,x in rows:vals.setdefault((w,n),[]).append(x);pairs.setdefault((w,r),{})[n]=x
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L decoder-stream lineage v4','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- mainmod restores upstream main `mod.rs` while retaining packed-color + 9-bit Huffman root','- 17 paired rounds; hashes/tests/MSRV passed','','| workload | current | mainmod | current/mainmod | mainmod wins |','|---|---:|---:|---:|---:|']
 for w in wl:
  q=[z['current']/z['mainmod']for(ww,_),z in sorted(pairs.items())if ww==w];L.append(f'| {w} | {statistics.median(vals[w,"current"]):.3f} us | {statistics.median(vals[w,"mainmod"]):.3f} us | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} |')
 Path('benchmark-vp8l-mod-lineage-v4.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
