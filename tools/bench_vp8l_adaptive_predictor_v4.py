#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='58dba70a93fef7883c934e28465e04534278fb80';TMP=Path('/tmp/vp8l-adaptive-pred');TS=[4,8,16,32,64,128]
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip() if cap else subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+n+(n&1)
 return o
def packed_fn(mode,t):
 off={2:'- width * 4',3:'- width * 4 + 4',4:'- width * 4 - 4'}[mode]
 return f'''pub fn apply_predictor_transform_{mode}(image_data: &mut [u8], range: Range<usize>, width: usize) {{
    assert!(range.end <= image_data.len());
    if (range.end - range.start) / 4 < {t} {{
        let mut i = range.start;
        while i < range.end {{ image_data[i] = image_data[i].wrapping_add(image_data[(i as isize {off.replace('width','width as isize')}) as usize]); i += 1; }}
        return;
    }}
    let (old,current)=image_data[..range.end].split_at_mut(range.start);
    let pred=&old[(range.start as isize {off.replace('width','width as isize')}) as usize..];
    for (p,q) in current.chunks_exact_mut(4).zip(pred.chunks_exact(4)) {{
        let a=u32::from_le_bytes(p.try_into().unwrap()); let b=u32::from_le_bytes(q.try_into().unwrap());
        let lo=(a&0x00ff00ff).wrapping_add(b&0x00ff00ff)&0x00ff00ff;
        let hi=(((a>>8)&0x00ff00ff).wrapping_add((b>>8)&0x00ff00ff)&0x00ff00ff)<<8;
        p.copy_from_slice(&(lo|hi).to_le_bytes());
    }}
}}
'''
def replace_fn(s,name,new):
 a=s.index(f'pub fn {name}(');num=int(name.rsplit('_',1)[1]);b=s.index(f'pub fn apply_predictor_transform_{num+1}(',a);return s[:a]+new+s[b:]
def prep(n):
 r=TMP/n;run(['git','worktree','add','--detach',str(r),BASE])
 if n!='base':
  t=int(n[1:]);p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text()
  for m in(2,3,4):s=replace_fn(s,f'apply_predictor_transform_{m}',packed_fn(m,t))
  p.write_text(s);run(['cargo','fmt'],cwd=r);run(['cargo','test','-q'],cwd=r);run(['cargo','+1.80.1','build','-q'],cwd=r)
 return r
def make(p,w,h,k):
 with p.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    if k=='stripes':q=((x>>4)^(y>>5))&7;a=q*31;b=(q*47)&255;c=(q*83)&255
    elif k=='tiles':q=((x>>5)+3*(y>>5))&15;a=q*17;b=(q*53)&255;c=(q*91)&255
    elif k=='noise':z=(x*1103515245+y*12345+((x*y)*2654435761))&0xffffffff;a=(z>>8)&255;b=(z>>16)&255;c=(z>>24)&255
    else:b=(x*7+y*11+((x>>4)^(y>>5))*19)&255;a=(b+((x+y)&31)-16)&255;c=(b+((x*3-y)&31)-16)&255
    i=x*3;row[i:i+3]=bytes((a,b,c))
   f.write(row)
B=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def build(r):
 (r/'examples').mkdir(exist_ok=True);(r/'examples/ap.rs').write_text(B);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','ap','-q'],cwd=r,env=e);return r/'target/release/examples/ap'
def inv(b,m,n,ps):return run(['taskset','-c','0',str(b),m,str(n),*[str(x)for x in ps]],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();names=['base']+[f't{x}'for x in TS];roots={n:prep(n)for n in names};bins={n:build(r)for n,r in roots.items()};rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p.read_bytes())and b'ANIM'not in chunks(p.read_bytes())];fx={}
 for k in('stripes','tiles','noise','corr'):
  ppm=TMP/f'{k}.ppm';w=TMP/f'{k}.webp';make(ppm,1536,1152,k);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(w)]);fx[k]=w
 h0=inv(bins['base'],'h',1,[roots['base']/r for r in rels]+list(fx.values()))
 for n in names[1:]:
  if inv(bins[n],'h',1,[roots[n]/r for r in rels]+list(fx.values()))!=h0:raise SystemExit('hash mismatch '+n)
 wl={'corpus':(rels,65),'generated':(list(fx.values()),12),'stripes':([fx['stripes']],10),'noise':([fx['noise']],4)};rows=[]
 for rnd in range(1,14):
  order=names if rnd%2 else list(reversed(names))
  for w,(items,iters) in wl.items():
   for n in order:rows.append((w,rnd,n,float(inv(bins[n],'t',iters,[roots[n]/r for r in items]if w=='corpus'else items))))
 vals={};pairs={}
 for w,r,n,x in rows:vals.setdefault((w,n),[]).append(x);pairs.setdefault((w,r),{})[n]=x
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L adaptive packed-predictor v4 matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- modes 2–4 packed only when span >= threshold pixels; 13 alternating rounds','- decoded hashes/tests/MSRV passed','','| workload | threshold | speedup | positive |','|---|---:|---:|---:|']
 for w in wl:
  for t in TS:
   n=f't{t}';q=[z['base']/z[n]for(ww,_),z in sorted(pairs.items())if ww==w];L.append(f'| {w} | {t} | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} |')
 Path('benchmark-vp8l-adaptive-predictor-v4.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
