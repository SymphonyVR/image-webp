#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='4f322d44fb38747659451db3d7f1dac7ff8ff21f';TMP=Path('/tmp/vp8l-color-paired-mul');VS=('base','pair','pair_byte')
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
 p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text();a=s.index('#[inline(always)]\nfn inverse_color_pixel_packed(');b=s.index('\n}\n\npub(crate) fn apply_color_transform(',a)+2
 third='''color_transform_delta(red_to_blue as i8, red as i8) as u8'''
 if v=='pair_byte':
  helper='''#[inline(always)]\nfn color_delta_byte(t: i8, c: i8) -> u8 { ((i16::from(t) * i16::from(c)) >> 5) as u8 }\n\n'''
  s=s[:a]+helper+s[a:];a+=len(helper);b+=len(helper);third='color_delta_byte(red_to_blue as i8, red as i8)'
 repl=f'''#[inline(always)]\nfn inverse_color_pixel_paired(\n    pixel: &mut [u8], red_to_blue: u8, green_pair: u32, green_red_base: i32, green_blue_base: i32,\n) {{\n    let argb = u32::from_le_bytes(pixel[..4].try_into().unwrap());\n    let green = ((argb >> 8) & 0xff) as u8;\n    let c = u32::from(green.wrapping_add(128));\n    let products = green_pair * c;\n    let correction = (c as i32) << 7;\n    let red_delta = (((products & 0xffff) as i32 + green_red_base - correction) >> 5) as u8;\n    let blue_delta = (((products >> 16) as i32 + green_blue_base - correction) >> 5) as u8;\n    let mut red = (argb & 0xff) as u8;\n    let mut blue = ((argb >> 16) & 0xff) as u8;\n    red = red.wrapping_add(red_delta);\n    blue = blue.wrapping_add(blue_delta);\n    blue = blue.wrapping_add({third});\n    let out = (argb & 0xff00_ff00) | u32::from(red) | (u32::from(blue) << 16);\n    pixel[..4].copy_from_slice(&out.to_le_bytes());\n}}'''
 s=s[:a]+repl+s[b:]
 old='''            let red_to_blue = transform[0];\n            let green_to_blue = transform[1];\n            let green_to_red = transform[2];\n\n            for pixel in block.chunks_exact_mut(4) {\n                inverse_color_pixel_packed(pixel, red_to_blue, green_to_blue, green_to_red);\n            }'''
 new='''            let red_to_blue = transform[0];\n            let green_to_blue = u32::from(transform[1].wrapping_add(128));\n            let green_to_red = u32::from(transform[2].wrapping_add(128));\n            let green_pair = green_to_red | (green_to_blue << 16);\n            let green_red_base = 16384 - ((green_to_red as i32) << 7);\n            let green_blue_base = 16384 - ((green_to_blue as i32) << 7);\n\n            for pixel in block.chunks_exact_mut(4) {\n                inverse_color_pixel_paired(\n                    pixel, red_to_blue, green_pair, green_red_base, green_blue_base,\n                );\n            }'''
 assert old in s;p.write_text(s.replace(old,new,1))
def inv(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for v in VS:
  r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
  if v!='base':
   patch(r,v);run(['cargo','fmt'],cwd=r)
   for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
  (r/'examples').mkdir(exist_ok=True);(r/'examples/cpair.rs').write_text(BENCH);run(['cargo','build','--release','--example','cpair','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/cpair'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)];corpus={v:[roots[v]/x for x in rels]for v in VS};hotrel=Path('tests/images/gallery2/3_webp_ll.webp');hot={v:[roots[v]/hotrel]for v in VS}
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
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L paired green-color multiply current-tree matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- independently packs green→red and green→blue coefficient products into one u32 multiply; pair_byte also uses byte-domain red→blue delta; hashes + full verification passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for name,rows in results.items():
  for v in VS[1:]:q=[z['base']/z[v]for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-color-paired-mul-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
