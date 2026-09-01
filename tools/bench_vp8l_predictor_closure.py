#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path
BASE="509d11c2bf102929ded4be05d3c54b06032fdc44"; TMP=Path('/tmp/vp8l-predictor-closure')
VS=['index','fuse','traverse','direct','avg','packed','p11','all']
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def replace_fn(s,n,nextn,body):
 a=s.index(f'pub fn apply_predictor_transform_{n}('); b=s.index(f'pub fn apply_predictor_transform_{nextn}(',a); return s[:a]+body+s[b:]
DISPATCH='''            match predictor {\n                0=>apply_predictor_transform_0(image_data,start_index..end_index,width),1=>apply_predictor_transform_1(image_data,start_index..end_index,width),\n                2=>apply_predictor_transform_2(image_data,start_index..end_index,width),3=>apply_predictor_transform_3(image_data,start_index..end_index,width),\n                4=>apply_predictor_transform_4(image_data,start_index..end_index,width),5=>apply_predictor_transform_5(image_data,start_index..end_index,width),\n                6=>apply_predictor_transform_6(image_data,start_index..end_index,width),7=>apply_predictor_transform_7(image_data,start_index..end_index,width),\n                8=>apply_predictor_transform_8(image_data,start_index..end_index,width),9=>apply_predictor_transform_9(image_data,start_index..end_index,width),\n                10=>apply_predictor_transform_10(image_data,start_index..end_index,width),11=>apply_predictor_transform_11(image_data,start_index..end_index,width),\n                12=>apply_predictor_transform_12(image_data,start_index..end_index,width),13=>apply_predictor_transform_13(image_data,start_index..end_index,width),_=>{}\n            }\n'''
def traversal(s,kind):
 a=s.index('pub(crate) fn apply_predictor_transform('); b=s.index('pub fn apply_predictor_transform_0(',a)
 pre='''pub(crate) fn apply_predictor_transform(image_data:&mut [u8],width:u16,height:u16,size_bits:u8,predictor_data:&[u8])->Result<(),DecodingError>{\n let block_xsize=usize::from(subsample_size(width,size_bits));let width=usize::from(width);let height=usize::from(height);\n image_data[3]=image_data[3].wrapping_add(255);apply_predictor_transform_1(image_data,4..width*4,width);\n'''
 idx=kind in ('index','traverse'); fuse=kind in ('fuse','traverse')
 body=''
 if not fuse: body+=''' for y in 1..height{for i in 0..4{image_data[y*width*4+i]=image_data[y*width*4+i].wrapping_add(image_data[(y-1)*width*4+i]);}}\n'''
 if idx: body+=''' let tile=1usize<<size_bits;let mut pred_row=0usize;\n'''
 body+=''' for y in 1..height{\n'''
 if fuse: body+='''  for i in 0..4{image_data[y*width*4+i]=image_data[y*width*4+i].wrapping_add(image_data[(y-1)*width*4+i]);}\n'''
 body+='''  for block_x in 0..block_xsize{\n'''
 if idx: body+='''   let predictor=predictor_data[(pred_row+block_x)*4+1];\n'''
 else: body+='''   let predictor=predictor_data[((y>>size_bits)*block_xsize+block_x)*4+1];\n'''
 body+='''   let start_index=(y*width+(block_x<<size_bits).max(1))*4;let end_index=(y*width+((block_x+1)<<size_bits).min(width))*4;\n'''+DISPATCH+'''  }\n'''
 if idx: body+='''  if (y+1)%tile==0{pred_row+=block_xsize;}\n'''
 body+=''' } Ok(())}\n'''
 return s[:a]+pre+body+s[b:]
HELP='''#[inline(always)] fn load_u32(p:&[u8])->u32{u32::from_le_bytes(p[..4].try_into().unwrap())}\n#[inline(always)] fn store_u32(p:&mut[u8],v:u32){p[..4].copy_from_slice(&v.to_le_bytes())}\n#[inline(always)] fn add_u32(a:u32,b:u32)->u32{let hi=(a&0xff00ff00).wrapping_add(b&0xff00ff00);let lo=(a&0x00ff00ff).wrapping_add(b&0x00ff00ff);(hi&0xff00ff00)|(lo&0x00ff00ff)}\n#[inline(always)] fn avg_u32(a:u32,b:u32)->u32{(((a^b)&0xfefefefe)>>1)+(a&b)}\n'''
DIRECT={
2:'''pub fn apply_predictor_transform_2(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,cur)=image_data[..range.end].split_at_mut(range.start);let top=&old[range.start-width*4..];for(p,t)in cur.chunks_exact_mut(4).zip(top.chunks_exact(4)){store_u32(p,add_u32(load_u32(p),load_u32(t)));}}\n''',
3:'''pub fn apply_predictor_transform_3(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,cur)=image_data[..range.end].split_at_mut(range.start);let top=&old[range.start-width*4+4..];for(p,t)in cur.chunks_exact_mut(4).zip(top.chunks_exact(4)){store_u32(p,add_u32(load_u32(p),load_u32(t)));}}\n''',
4:'''pub fn apply_predictor_transform_4(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,cur)=image_data[..range.end].split_at_mut(range.start);let top=&old[range.start-width*4-4..];for(p,t)in cur.chunks_exact_mut(4).zip(top.chunks_exact(4)){store_u32(p,add_u32(load_u32(p),load_u32(t)));}}\n'''}
AVG={
5:'''pub fn apply_predictor_transform_5(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,cur)=image_data[..range.end].split_at_mut(range.start);let mut l=load_u32(&old[range.start-4..]);let tr=&old[range.start-width*4+4..];let t=&old[range.start-width*4..];for((p,r),q)in cur.chunks_exact_mut(4).zip(tr.chunks_exact(4)).zip(t.chunks_exact(4)){l=add_u32(load_u32(p),avg_u32(avg_u32(l,load_u32(r)),load_u32(q)));store_u32(p,l);}}\n''',
6:'''pub fn apply_predictor_transform_6(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,cur)=image_data[..range.end].split_at_mut(range.start);let mut l=load_u32(&old[range.start-4..]);let tl=&old[range.start-width*4-4..];for(p,q)in cur.chunks_exact_mut(4).zip(tl.chunks_exact(4)){l=add_u32(load_u32(p),avg_u32(l,load_u32(q)));store_u32(p,l);}}\n''',
7:'''pub fn apply_predictor_transform_7(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,cur)=image_data[..range.end].split_at_mut(range.start);let mut l=load_u32(&old[range.start-4..]);let t=&old[range.start-width*4..];for(p,q)in cur.chunks_exact_mut(4).zip(t.chunks_exact(4)){l=add_u32(load_u32(p),avg_u32(l,load_u32(q)));store_u32(p,l);}}\n''',
8:'''pub fn apply_predictor_transform_8(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,cur)=image_data[..range.end].split_at_mut(range.start);let tl=&old[range.start-width*4-4..];let t=&old[range.start-width*4..];for((p,a),b)in cur.chunks_exact_mut(4).zip(tl.chunks_exact(4)).zip(t.chunks_exact(4)){store_u32(p,add_u32(load_u32(p),avg_u32(load_u32(a),load_u32(b))));}}\n''',
9:'''pub fn apply_predictor_transform_9(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,cur)=image_data[..range.end].split_at_mut(range.start);let t=&old[range.start-width*4..];let tr=&old[range.start-width*4+4..];for((p,a),b)in cur.chunks_exact_mut(4).zip(t.chunks_exact(4)).zip(tr.chunks_exact(4)){store_u32(p,add_u32(load_u32(p),avg_u32(load_u32(a),load_u32(b))));}}\n''',
10:'''pub fn apply_predictor_transform_10(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,cur)=image_data[..range.end].split_at_mut(range.start);let mut l=load_u32(&old[range.start-4..]);let tl=&old[range.start-width*4-4..];let t=&old[range.start-width*4..];let tr=&old[range.start-width*4+4..];for(((p,a),b),c)in cur.chunks_exact_mut(4).zip(tl.chunks_exact(4)).zip(t.chunks_exact(4)).zip(tr.chunks_exact(4)){l=add_u32(load_u32(p),avg_u32(avg_u32(l,load_u32(a)),avg_u32(load_u32(b),load_u32(c))));store_u32(p,l);}}\n'''}
P11='''#[inline(always)] fn sad4(a:[u8;4],b:[u8;4])->u16{u16::from(a[0].abs_diff(b[0]))+u16::from(a[1].abs_diff(b[1]))+u16::from(a[2].abs_diff(b[2]))+u16::from(a[3].abs_diff(b[3]))}\npub fn apply_predictor_transform_11(image_data:&mut[u8],range:Range<usize>,width:usize){let(old,cur)=image_data[..range.end].split_at_mut(range.start);let top=&old[range.start-width*4..];let mut l:[u8;4]=old[range.start-4..range.start].try_into().unwrap();let mut tl:[u8;4]=old[range.start-width*4-4..range.start-width*4].try_into().unwrap();for(p,t)in cur.chunks_exact_mut(4).zip(top.chunks_exact(4)){let t:[u8;4]=t.try_into().unwrap();let pred=if sad4(t,tl)<sad4(l,tl){l}else{t};l=[p[0].wrapping_add(pred[0]),p[1].wrapping_add(pred[1]),p[2].wrapping_add(pred[2]),p[3].wrapping_add(pred[3])];p.copy_from_slice(&l);tl=t;}}\n'''
def patch(n,r):
 p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text()
 if n in ('index','fuse','traverse','all'):s=traversal(s,'traverse' if n=='all' else n)
 if n in ('direct','packed','all'):
  m='fn average2_autovec(a: u8, b: u8) -> u8 {\n    (a & b) + ((a ^ b) >> 1)\n}\n';s=s.replace(m,m+HELP,1)
  for k,v in DIRECT.items():s=replace_fn(s,k,k+1,v)
 elif n in ('avg',):
  m='fn average2_autovec(a: u8, b: u8) -> u8 {\n    (a & b) + ((a ^ b) >> 1)\n}\n';s=s.replace(m,m+HELP,1)
 if n in ('avg','packed','all'):
  if n=='packed' and HELP not in s:
   m='fn average2_autovec(a: u8, b: u8) -> u8 {\n    (a & b) + ((a ^ b) >> 1)\n}\n';s=s.replace(m,m+HELP,1)
  for k,v in AVG.items():s=replace_fn(s,k,k+1,v)
 if n in ('p11','all'):s=replace_fn(s,11,12,P11)
 p.write_text(s)
def prep(n):
 r=TMP/n;run(['git','worktree','add','--detach',str(r),BASE]);
 if n!='base':patch(n,r);run(['cargo','fmt'],cwd=r);run(['cargo','test','-q'],cwd=r);run(['cargo','+1.80.1','build','-q'],cwd=r)
 return r
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];z=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+z+(z&1)
 return o
def corpus(r):return[p.relative_to(r) for p in sorted((r/'tests/images').rglob('*.webp')) if b'VP8L'in chunks(p.read_bytes()) and b'ANIM'not in chunks(p.read_bytes())]
BENCH='''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def build(r):
 (r/'examples').mkdir(exist_ok=True);(r/'examples/pc.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','pc','-q'],cwd=r,env=e);return r/'target/release/examples/pc'
def invoke(b,m,n,ps):return run(['taskset','-c','0',str(b),m,str(n),*[str(x)for x in ps]],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={n:prep(n)for n in ['base',*VS]};rels=corpus(roots['base']);ppm=TMP/'large.ppm';w=h=1536
 with ppm.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):i=x*3;row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
   f.write(row)
 webp=TMP/'large.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);bins={n:build(r)for n,r in roots.items()};bh=invoke(bins['base'],'h',1,[*[roots['base']/r for r in rels],webp])
 for n in VS:
  if invoke(bins[n],'h',1,[*[roots[n]/r for r in rels],webp])!=bh:raise SystemExit('hash '+n)
 rows=[]
 for rnd in range(1,12):
  order=['base',*VS]if rnd%2 else[*reversed(VS),'base']
  for n in order:rows.append(('corpus',rnd,n,float(invoke(bins[n],'bench',45,[roots[n]/r for r in rels]))));rows.append(('large',rnd,n,float(invoke(bins[n],'bench',3,[webp]))))
 rr={}
 for w,r,n,x in rows:rr.setdefault((w,r),{})[n]=x
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L predictor closure matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + MSRV passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for w in ('corpus','large'):
  for n in VS:
   q=[z['base']/z[n]for(ww,_),z in sorted(rr.items())if ww==w];L.append(f'| {w} | {n} | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-predictor-closure-v2.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
