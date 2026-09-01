#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='0881ec1a66f09e11b766c309cf6e651077775bd9';TMP=Path('/tmp/vp8l-packed-predictors-current');VS=('base','direct','avg','both')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let p:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=p.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
HELPERS=r'''
#[inline(always)] fn load_pixel_u32(pixel:&[u8])->u32{u32::from_le_bytes(pixel[..4].try_into().unwrap())}
#[inline(always)] fn average2_u32(a:u32,b:u32)->u32{(((a^b)&0xfefe_fefe)>>1)+(a&b)}
#[inline(always)] fn add_pixels_u32(a:u32,b:u32)->u32{let hi=(a&0xff00_ff00).wrapping_add(b&0xff00_ff00);let lo=(a&0x00ff_00ff).wrapping_add(b&0x00ff_00ff);(hi&0xff00_ff00)|(lo&0x00ff_00ff)}
#[inline(always)] fn store_pixel_u32(pixel:&mut[u8],value:u32){pixel[..4].copy_from_slice(&value.to_le_bytes());}
'''
BODIES={
2:r'''pub fn apply_predictor_transform_2(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,current)=image_data[..range.end].split_at_mut(range.start);let top=&old[range.start-width*4..];for(pixel,t)in current.chunks_exact_mut(4).zip(top.chunks_exact(4)){let out=add_pixels_u32(load_pixel_u32(pixel),load_pixel_u32(t));store_pixel_u32(pixel,out);}}
''',
3:r'''pub fn apply_predictor_transform_3(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,current)=image_data[..range.end].split_at_mut(range.start);let tr=&old[range.start-width*4+4..];for(pixel,t)in current.chunks_exact_mut(4).zip(tr.chunks_exact(4)){let out=add_pixels_u32(load_pixel_u32(pixel),load_pixel_u32(t));store_pixel_u32(pixel,out);}}
''',
4:r'''pub fn apply_predictor_transform_4(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,current)=image_data[..range.end].split_at_mut(range.start);let tl=&old[range.start-width*4-4..];for(pixel,t)in current.chunks_exact_mut(4).zip(tl.chunks_exact(4)){let out=add_pixels_u32(load_pixel_u32(pixel),load_pixel_u32(t));store_pixel_u32(pixel,out);}}
''',
5:r'''pub fn apply_predictor_transform_5(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,current)=image_data[..range.end].split_at_mut(range.start);let mut left=load_pixel_u32(&old[range.start-4..]);let tr=&old[range.start-width*4+4..];let top=&old[range.start-width*4..];for((pixel,tr),t)in current.chunks_exact_mut(4).zip(tr.chunks_exact(4)).zip(top.chunks_exact(4)){let pred=average2_u32(average2_u32(left,load_pixel_u32(tr)),load_pixel_u32(t));left=add_pixels_u32(load_pixel_u32(pixel),pred);store_pixel_u32(pixel,left);}}
''',
6:r'''pub fn apply_predictor_transform_6(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,current)=image_data[..range.end].split_at_mut(range.start);let mut left=load_pixel_u32(&old[range.start-4..]);let tl=&old[range.start-width*4-4..];for(pixel,tl)in current.chunks_exact_mut(4).zip(tl.chunks_exact(4)){let pred=average2_u32(left,load_pixel_u32(tl));left=add_pixels_u32(load_pixel_u32(pixel),pred);store_pixel_u32(pixel,left);}}
''',
7:r'''pub fn apply_predictor_transform_7(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,current)=image_data[..range.end].split_at_mut(range.start);let mut left=load_pixel_u32(&old[range.start-4..]);let top=&old[range.start-width*4..];for(pixel,t)in current.chunks_exact_mut(4).zip(top.chunks_exact(4)){let pred=average2_u32(left,load_pixel_u32(t));left=add_pixels_u32(load_pixel_u32(pixel),pred);store_pixel_u32(pixel,left);}}
''',
8:r'''pub fn apply_predictor_transform_8(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,current)=image_data[..range.end].split_at_mut(range.start);let tl=&old[range.start-width*4-4..];let top=&old[range.start-width*4..];for((pixel,tl),t)in current.chunks_exact_mut(4).zip(tl.chunks_exact(4)).zip(top.chunks_exact(4)){let pred=average2_u32(load_pixel_u32(tl),load_pixel_u32(t));let out=add_pixels_u32(load_pixel_u32(pixel),pred);store_pixel_u32(pixel,out);}}
''',
9:r'''pub fn apply_predictor_transform_9(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,current)=image_data[..range.end].split_at_mut(range.start);let top=&old[range.start-width*4..];let tr=&old[range.start-width*4+4..];for((pixel,t),tr)in current.chunks_exact_mut(4).zip(top.chunks_exact(4)).zip(tr.chunks_exact(4)){let pred=average2_u32(load_pixel_u32(t),load_pixel_u32(tr));let out=add_pixels_u32(load_pixel_u32(pixel),pred);store_pixel_u32(pixel,out);}}
''',
10:r'''pub fn apply_predictor_transform_10(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,current)=image_data[..range.end].split_at_mut(range.start);let mut left=load_pixel_u32(&old[range.start-4..]);let tl=&old[range.start-width*4-4..];let top=&old[range.start-width*4..];let tr=&old[range.start-width*4+4..];for(((pixel,tl),t),tr)in current.chunks_exact_mut(4).zip(tl.chunks_exact(4)).zip(top.chunks_exact(4)).zip(tr.chunks_exact(4)){let pred=average2_u32(average2_u32(left,load_pixel_u32(tl)),average2_u32(load_pixel_u32(t),load_pixel_u32(tr)));left=add_pixels_u32(load_pixel_u32(pixel),pred);store_pixel_u32(pixel,left);}}
'''}
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
 p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text();marker='''fn average2_autovec(a: u8, b: u8) -> u8 {\n    (a & b) + ((a ^ b) >> 1)\n}\n''';assert marker in s;s=s.replace(marker,marker+HELPERS,1)
 nums=[]
 if v in('direct','both'):nums += [2,3,4]
 if v in('avg','both'):nums += [5,6,7,8,9,10]
 for n in nums:
  a=s.index(f'pub fn apply_predictor_transform_{n}(');b=s.index(f'pub fn apply_predictor_transform_{n+1}(',a);s=s[:a]+BODIES[n]+s[b:]
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
  (r/'examples').mkdir(exist_ok=True);(r/'examples/ppc.rs').write_text(BENCH);run(['cargo','build','--release','--example','ppc','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/ppc'
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
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# Packed VP8L predictors current-final matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for name,rows in res.items():
  for v in VS[1:]:q=[z['base']/z[v]for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-packed-predictors-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
