#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path
BASE='4f322d44fb38747659451db3d7f1dac7ff8ff21f';TMP=Path('/tmp/vp8l-color-delta');VS=('base','i16u32','u8packed','u8array')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
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
 p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text()
 if v=='i16u32':
  old='''fn color_transform_delta(t: i8, c: i8) -> u32 {\n    (i32::from(t) * i32::from(c)) as u32 >> 5\n}'''
  new='''fn color_transform_delta(t: i8, c: i8) -> u32 {\n    u32::from(((i16::from(t) * i16::from(c)) as u16) >> 5)\n}''';assert old in s;s=s.replace(old,new,1)
 else:
  marker='''#[inline(always)]\nfn inverse_color_pixel_packed('''
  helper='''#[inline(always)]\nfn color_transform_delta_u8(t: i8, c: i8) -> u8 {\n    ((i16::from(t) * i16::from(c)) >> 5) as u8\n}\n\n'''
  assert marker in s;s=s.replace(marker,helper+marker,1)
  a=s.index('#[inline(always)]\nfn inverse_color_pixel_packed(');b=s.index('\n}\n\npub(crate) fn apply_color_transform(',a)+2
  if v=='u8packed':
   repl='''#[inline(always)]\nfn inverse_color_pixel_packed(\n    pixel: &mut [u8],\n    red_to_blue: u8,\n    green_to_blue: u8,\n    green_to_red: u8,\n) {\n    let argb = u32::from_le_bytes(pixel[..4].try_into().unwrap());\n    let green = ((argb >> 8) & 0xff) as u8;\n    let mut red = (argb & 0xff) as u8;\n    let mut blue = ((argb >> 16) & 0xff) as u8;\n    red = red.wrapping_add(color_transform_delta_u8(green_to_red as i8, green as i8));\n    blue = blue.wrapping_add(color_transform_delta_u8(green_to_blue as i8, green as i8));\n    blue = blue.wrapping_add(color_transform_delta_u8(red_to_blue as i8, red as i8));\n    let out = (argb & 0xff00_ff00) | u32::from(red) | (u32::from(blue) << 16);\n    pixel[..4].copy_from_slice(&out.to_le_bytes());\n}'''
  else:
   repl='''#[inline(always)]\nfn inverse_color_pixel_packed(\n    pixel: &mut [u8],\n    red_to_blue: u8,\n    green_to_blue: u8,\n    green_to_red: u8,\n) {\n    let mut rgba: [u8; 4] = pixel[..4].try_into().unwrap();\n    let green = rgba[1] as i8;\n    rgba[0] = rgba[0].wrapping_add(color_transform_delta_u8(green_to_red as i8, green));\n    rgba[2] = rgba[2].wrapping_add(color_transform_delta_u8(green_to_blue as i8, green));\n    rgba[2] = rgba[2].wrapping_add(color_transform_delta_u8(red_to_blue as i8, rgba[0] as i8));\n    pixel[..4].copy_from_slice(&rgba);\n}'''
  s=s[:a]+repl+s[b:]
 p.write_text(s)
def inv(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for v in VS:
  r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
  if v!='base':
   patch(r,v);run(['cargo','fmt'],cwd=r)
   for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
  (r/'examples').mkdir(exist_ok=True);(r/'examples/cdelta.rs').write_text(BENCH);run(['cargo','build','--release','--example','cdelta','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/cdelta'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
 corpus={v:[roots[v]/x for x in rels]for v in VS};hotrel=Path('tests/images/gallery2/3_webp_ll.webp');hot={v:[roots[v]/hotrel]for v in VS}
 bh=inv(exes['base'],'h',1,corpus['base'])
 for v in VS[1:]:assert bh==inv(exes[v],'h',1,corpus[v])
 results={}
 for name,files,it in [('corpus',corpus,70),('colorhot',hot,45)]:
  rows=[]
  for n in range(17):
   order=VS if n%2==0 else tuple(reversed(VS));z={}
   for v in order:z[v]=float(inv(exes[v],'t',it,files[v]))
   rows.append(z)
  results[name]=rows
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L color-delta current-tree matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- tests narrower signed multiply and byte-domain channel accumulation; hashes + full verification passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for name,rows in results.items():
  for v in VS[1:]:q=[z['base']/z[v]for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-color-delta-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
