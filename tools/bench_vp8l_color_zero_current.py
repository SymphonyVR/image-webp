#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='4f322d44fb38747659451db3d7f1dac7ff8ff21f';TMP=Path('/tmp/vp8l-color-zero-current');VS=('base','zero','mask')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
ZERO=r'''pub(crate) fn apply_color_transform(
    image_data: &mut [u8],
    width: u16,
    size_bits: u8,
    transform_data: &[u8],
) {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);
    for (y, row) in image_data.chunks_exact_mut(width * 4).enumerate() {
        let row_transform_data_start = (y >> size_bits) * block_xsize * 4;
        let row_tf_data = &transform_data[row_transform_data_start..];
        for (block, transform) in row.chunks_mut(4 << size_bits).zip(row_tf_data.chunks_exact(4)) {
            let red_to_blue = transform[0];
            let green_to_blue = transform[1];
            let green_to_red = transform[2];
            if red_to_blue == 0 && green_to_blue == 0 && green_to_red == 0 { continue; }
            for pixel in block.chunks_exact_mut(4) {
                inverse_color_pixel_packed(pixel, red_to_blue, green_to_blue, green_to_red);
            }
        }
    }
}

'''
HELP=r'''#[inline(always)]
fn color_block_rb(block: &mut [u8], rb: u8) { for p in block.chunks_exact_mut(4) { let v=u32::from_le_bytes(p.try_into().unwrap()); let r=(v&0xff) as u8; let b=((v>>16)&0xff).wrapping_add(color_transform_delta(rb as i8,r as i8) as u8); let out=(v&0xff00_ffff)|(u32::from(b)<<16); p.copy_from_slice(&out.to_le_bytes()); } }
#[inline(always)]
fn color_block_gb(block: &mut [u8], gb: u8) { for p in block.chunks_exact_mut(4) { let v=u32::from_le_bytes(p.try_into().unwrap()); let g=((v>>8)&0xff) as u8; let b=((v>>16)&0xff).wrapping_add(color_transform_delta(gb as i8,g as i8) as u8); let out=(v&0xff00_ffff)|(u32::from(b)<<16); p.copy_from_slice(&out.to_le_bytes()); } }
#[inline(always)]
fn color_block_gr(block: &mut [u8], gr: u8) { for p in block.chunks_exact_mut(4) { let v=u32::from_le_bytes(p.try_into().unwrap()); let g=((v>>8)&0xff) as u8; let r=(v&0xff).wrapping_add(color_transform_delta(gr as i8,g as i8) as u8); let out=(v&0xffff_ff00)|u32::from(r); p.copy_from_slice(&out.to_le_bytes()); } }
#[inline(always)]
fn color_block_rb_gb(block: &mut [u8], rb:u8, gb:u8) { for p in block.chunks_exact_mut(4) { let v=u32::from_le_bytes(p.try_into().unwrap()); let g=((v>>8)&0xff) as u8; let r=(v&0xff) as u8; let mut b=((v>>16)&0xff) as u8; b=b.wrapping_add(color_transform_delta(gb as i8,g as i8) as u8); b=b.wrapping_add(color_transform_delta(rb as i8,r as i8) as u8); let out=(v&0xff00_ffff)|(u32::from(b)<<16); p.copy_from_slice(&out.to_le_bytes()); } }
#[inline(always)]
fn color_block_rb_gr(block: &mut [u8], rb:u8, gr:u8) { for p in block.chunks_exact_mut(4) { let v=u32::from_le_bytes(p.try_into().unwrap()); let g=((v>>8)&0xff) as u8; let r=(v&0xff).wrapping_add(color_transform_delta(gr as i8,g as i8) as u8); let b=((v>>16)&0xff).wrapping_add(color_transform_delta(rb as i8,r as i8) as u8); let out=(v&0xff00_ff00)|u32::from(r)|(u32::from(b)<<16); p.copy_from_slice(&out.to_le_bytes()); } }
#[inline(always)]
fn color_block_gb_gr(block: &mut [u8], gb:u8, gr:u8) { for p in block.chunks_exact_mut(4) { let v=u32::from_le_bytes(p.try_into().unwrap()); let g=((v>>8)&0xff) as u8; let r=(v&0xff).wrapping_add(color_transform_delta(gr as i8,g as i8) as u8); let b=((v>>16)&0xff).wrapping_add(color_transform_delta(gb as i8,g as i8) as u8); let out=(v&0xff00_ff00)|u32::from(r)|(u32::from(b)<<16); p.copy_from_slice(&out.to_le_bytes()); } }
'''
MASK=r'''pub(crate) fn apply_color_transform(
    image_data: &mut [u8],
    width: u16,
    size_bits: u8,
    transform_data: &[u8],
) {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);
    for (y, row) in image_data.chunks_exact_mut(width * 4).enumerate() {
        let row_transform_data_start = (y >> size_bits) * block_xsize * 4;
        let row_tf_data = &transform_data[row_transform_data_start..];
        for (block, transform) in row.chunks_mut(4 << size_bits).zip(row_tf_data.chunks_exact(4)) {
            let rb=transform[0];let gb=transform[1];let gr=transform[2];
            let mask=u8::from(rb!=0)|(u8::from(gb!=0)<<1)|(u8::from(gr!=0)<<2);
            match mask {
                0=>{},1=>color_block_rb(block,rb),2=>color_block_gb(block,gb),3=>color_block_rb_gb(block,rb,gb),
                4=>color_block_gr(block,gr),5=>color_block_rb_gr(block,rb,gr),6=>color_block_gb_gr(block,gb,gr),
                _=>for pixel in block.chunks_exact_mut(4){inverse_color_pixel_packed(pixel,rb,gb,gr);},
            }
        }
    }
}

'''
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
 p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text();a=s.index('pub(crate) fn apply_color_transform(');b=s.index('pub(crate) fn apply_subtract_green_transform(',a)
 if v=='zero':s=s[:a]+ZERO+s[b:]
 else:s=s[:a]+HELP+MASK+s[b:]
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
  (r/'examples').mkdir(exist_ok=True);(r/'examples/czero.rs').write_text(BENCH);run(['cargo','build','--release','--example','czero','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/czero'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
 corpus={v:[roots[v]/x for x in rels]for v in VS};hot_rel=Path('tests/images/gallery2/3_webp_ll.webp');hot={v:[roots[v]/hot_rel]for v in VS};bh=inv(exes['base'],'h',1,corpus['base'])
 for v in VS[1:]:assert bh==inv(exes[v],'h',1,corpus[v])
 results={}
 for name,files,it in [('corpus',corpus,70),('colorhot',hot,30)]:
  rows=[]
  for n in range(17):
   order=VS if n%2==0 else tuple(reversed(VS));z={}
   for v in order:z[v]=float(inv(exes[v],'t',it,files[v]))
   rows.append(z)
  results[name]=rows
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L color zero-coefficient current-tree matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- branches once per color-transform block; hashes + full verification passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for name,rows in results.items():
  for v in VS[1:]:q=[z['base']/z[v]for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-color-zero-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
