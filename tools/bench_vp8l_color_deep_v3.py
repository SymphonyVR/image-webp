#!/usr/bin/env python3
import math, os, shutil, statistics, subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44'; TMP=Path('/tmp/vp8l-color-deep-v3')
VS=['packed_outer','packed_current','packed_inc','scalar_inc']
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def replace_color(s,body,helper=''):
 a=s.index('pub(crate) fn apply_color_transform(');b=s.index('pub(crate) fn apply_subtract_green_transform(',a);return s[:a]+helper+body+s[b:]
HELPER=r'''#[inline(always)]
fn inverse_color_pixel_packed(pixel: &mut [u8], rb: u8, gb: u8, gr: u8) {
    let argb=u32::from_le_bytes(pixel[..4].try_into().unwrap());
    let green=((argb>>8)&255) as u8; let mut red=argb&255; let mut blue=(argb>>16)&255;
    red+=color_transform_delta(gr as i8,green as i8); blue+=color_transform_delta(gb as i8,green as i8);
    red&=255; blue+=color_transform_delta(rb as i8,red as u8 as i8); blue&=255;
    let out=(argb&0xff00_ff00)|red|(blue<<16); pixel[..4].copy_from_slice(&out.to_le_bytes());
}

'''
OUTER=r'''pub(crate) fn apply_color_transform(image_data:&mut [u8],width:u16,size_bits:u8,transform_data:&[u8]){
 let bx=usize::from(subsample_size(width,size_bits));let w=usize::from(width);
 for (y,row) in image_data.chunks_exact_mut(w*4).enumerate(){let tf=&transform_data[(y>>size_bits)*bx*4..];
  for (block,t) in row.chunks_mut(4<<size_bits).zip(tf.chunks_exact(4)){let rb=t[0];let gb=t[1];let gr=t[2];for p in block.chunks_exact_mut(4){inverse_color_pixel_packed(p,rb,gb,gr);}}
 }
}

'''
CURRENT=r'''pub(crate) fn apply_color_transform(image_data:&mut [u8],width:u16,size_bits:u8,transform_data:&[u8]){
 let bx=usize::from(subsample_size(width,size_bits));let w=usize::from(width);let tile=1usize<<size_bits;let safe=w&!(tile-1);
 for (y,row) in image_data.chunks_exact_mut(w*4).enumerate(){let tf=&transform_data[(y>>size_bits)*bx*4..];let(full,tail)=row.split_at_mut(safe*4);
  for(block,t) in full.chunks_exact_mut(tile*4).zip(tf.chunks_exact(4)){let rb=t[0];let gb=t[1];let gr=t[2];for p in block.chunks_exact_mut(4){inverse_color_pixel_packed(p,rb,gb,gr);}}
  if !tail.is_empty(){let t=&tf[(safe/tile)*4..][..4];for p in tail.chunks_exact_mut(4){inverse_color_pixel_packed(p,t[0],t[1],t[2]);}}
 }
}

'''
PINC=r'''pub(crate) fn apply_color_transform(image_data:&mut [u8],width:u16,size_bits:u8,transform_data:&[u8]){
 let bx=usize::from(subsample_size(width,size_bits));let w=usize::from(width);let bb=4usize<<size_bits;let mask=(1usize<<size_bits)-1;let mut off=0usize;
 for(y,row) in image_data.chunks_exact_mut(w*4).enumerate(){let tf=&transform_data[off..];for(block,t) in row.chunks_mut(bb).zip(tf.chunks_exact(4)){let rb=t[0];let gb=t[1];let gr=t[2];for p in block.chunks_exact_mut(4){inverse_color_pixel_packed(p,rb,gb,gr);}}if((y+1)&mask)==0{off+=bx*4;}}
}

'''
SINC=r'''pub(crate) fn apply_color_transform(image_data:&mut [u8],width:u16,size_bits:u8,transform_data:&[u8]){
 let bx=usize::from(subsample_size(width,size_bits));let w=usize::from(width);let bb=4usize<<size_bits;let mask=(1usize<<size_bits)-1;let mut off=0usize;
 for(y,row) in image_data.chunks_exact_mut(w*4).enumerate(){let tf=&transform_data[off..];for(block,t) in row.chunks_mut(bb).zip(tf.chunks_exact(4)){let rb=t[0]as i8;let gb=t[1]as i8;let gr=t[2]as i8;for p in block.chunks_exact_mut(4){let g=p[1]as i8;let mut r=u32::from(p[0]);let mut b=u32::from(p[2]);r+=color_transform_delta(gr,g);b+=color_transform_delta(gb,g);b+=color_transform_delta(rb,r as u8 as i8);p[0]=(r&255)as u8;p[2]=(b&255)as u8;}}if((y+1)&mask)==0{off+=bx*4;}}
}

'''
def patch(n,r):
 p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text();body={'packed_outer':OUTER,'packed_current':CURRENT,'packed_inc':PINC,'scalar_inc':SINC}[n];p.write_text(replace_color(s,body,'' if n=='scalar_inc' else HELPER))
def prep(n):
 r=TMP/n;run(['git','worktree','add','--detach',str(r),BASE]);
 if n!='base':patch(n,r);run(['cargo','fmt'],cwd=r);run(['cargo','test','-q'],cwd=r);run(['cargo','+1.80.1','build','-q'],cwd=r)
 return r
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+n+(n&1)
 return o
def ppm(path,w,h,kind):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    if kind=='structured':r=(x*3+y*5+((x>>5)^(y>>4))*17)&255;g=(x*2+y*7+((x*y)>>10))&255;b=(x*11+y*3+((x+y)>>3)*9)&255
    elif kind=='color':g=(x*5+y*9+((x*y)>>9))&255;r=(g*3+(x>>2))&255;b=(255-g+(y>>1))&255
    elif kind=='gradient':r=x*255//max(1,w-1);g=y*255//max(1,h-1);b=(x+y)*255//max(1,w+h-2)
    elif kind=='corr':g=(x*7+y*11)&255;r=(g+((x>>3)&15))&255;b=(g-((y>>3)&15))&255
    elif kind=='anticorr':g=(x*5+y*3)&255;r=(255-g+((x>>4)&7))&255;b=g^255
    elif kind=='tiles':q=((x>>5)+3*(y>>5))&15;r=q*17;g=(q*53+(x&31)*3)&255;b=(q*91+(y&31)*5)&255
    elif kind=='noise':z=(x*1103515245+y*12345+(x*y)*2654435761)&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
    else:r=(x*13+y*7+((x*y)>>8))&255;g=(x*2+y*17+((x+y)>>2)*11)&255;b=(x*5+y*3+((x>>4)^(y>>3))*29)&255
    i=x*3;row[i:i+3]=bytes((r,g,b))
   f.write(row)
def fixtures():
 out=[];spec=[('structured',1536,1536),('color',1536,1536),('gradient',1536,1024),('corr',1536,1536),('anticorr',1536,1536),('tiles',1536,1536),('noise',1024,1024),('photoish',1536,1536)]
 for k,w,h in spec:
  p=TMP/(k+'.ppm');ppm(p,w,h,k)
  for z in ([0,3,6,9] if k in('structured','color','corr')else[9]):
   q=TMP/f'{k}-z{z}.webp';run(['cwebp','-quiet','-lossless','-z',str(z),str(p),'-o',str(q)]);out.append(q)
 return out
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let a:Vec<_>=std::env::args().skip(1).collect();let m=&a[0];let n:usize=a[1].parse().unwrap();let x=std::fs::read(&a[2]).unwrap();if m=="h"{println!("{:x}",h(&x));return}for _ in 0..2{black_box(d(&x));}let t=Instant::now();for _ in 0..n{black_box(d(&x));}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/n as f64)}'''
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={n:prep(n)for n in['base',*VS]};files=[]
 for p in sorted((roots['base']/'tests/images').rglob('*.webp')):
  c=chunks(p.read_bytes())
  if b'VP8L'in c and b'ANIM'not in c:files.append(('corpus/'+str(p.relative_to(roots['base'])),p))
 files += [('gen/'+p.name,p) for p in fixtures()];bins={}
 for n,r in roots.items():
  (r/'examples').mkdir(exist_ok=True);(r/'examples/color_deep.rs').write_text(BENCH);env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','color_deep','-q'],cwd=r,env=env);bins[n]=r/'target/release/examples/color_deep'
 for label,p in files:
  bh=run([str(bins['base']),'h','1',str(p)],cap=True)
  for n in VS:
   cp=roots[n]/p.relative_to(roots['base']) if str(p).startswith(str(roots['base'])) else p
   if run([str(bins[n]),'h','1',str(cp)],cap=True)!=bh:raise SystemExit(f'hash mismatch {label} {n}')
 rows=[]
 for label,p in files:
  t=float(run([str(bins['base']),'t','1',str(p)],cap=True));it=max(2,min(400,math.ceil(35000/max(t,1.0))))
  for cand in VS:
   cp=roots[cand]/p.relative_to(roots['base']) if str(p).startswith(str(roots['base'])) else p;rr=[];bs=[];cs=[]
   for rnd in range(13):
    vals={};order=['base',cand]if rnd%2==0 else[cand,'base']
    for v in order:vals[v]=float(run([str(bins[v]),'t',str(it),str(p if v=='base' else cp)],cap=True))
    bs.append(vals['base']);cs.append(vals[cand]);rr.append(vals['base']/vals[cand])
   rows.append((label,cand,statistics.median(bs),statistics.median(cs),statistics.median(rr),sum(x>1 for x in rr),min(rr),max(rr)))
 L=['# VP8L deep color-transform matrix','',f'- baseline: `{BASE}`','- all decoded hashes match; candidates pass tests + Rust 1.80.1','- 13 alternating paired rounds per file; adaptive iterations target ~35 ms/sample','','| file | candidate | base us | cand us | median | positive | range |','|---|---|---:|---:|---:|---:|---:|']
 for r in rows:L.append(f'| {r[0]} | {r[1]} | {r[2]:.3f} | {r[3]:.3f} | {r[4]:.4f}x | {r[5]}/13 | {r[6]:.4f}–{r[7]:.4f}x |')
 L+=['','## Aggregate medians','','| set | candidate | median file ratio | files >1 |','|---|---|---:|---:|']
 for g,prefix in [('corpus','corpus/'),('generated','gen/'),('all','')]:
  for c in VS:
   q=[r[4]for r in rows if r[1]==c and(not prefix or r[0].startswith(prefix))];L.append(f'| {g} | {c} | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} |')
 Path('benchmark-vp8l-color-deep-v3.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
