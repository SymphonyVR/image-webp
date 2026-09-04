#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='4f322d44fb38747659451db3d7f1dac7ff8ff21f';TMP=Path('/tmp/vp8l-color-delta-lut-current');VS=('base','lut','lutzero')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
TABLE=r'''const fn build_color_delta_lut() -> [u8; 65536] {
    let mut table = [0u8; 65536];
    let mut t = 0usize;
    while t < 256 {
        let coeff = (t as u8) as i8 as i32;
        let mut c = 0usize;
        while c < 256 {
            let color = (c as u8) as i8 as i32;
            table[(t << 8) | c] = ((coeff * color) as u32 >> 5) as u8;
            c += 1;
        }
        t += 1;
    }
    table
}
static COLOR_DELTA_LUT: [u8; 65536] = build_color_delta_lut();
#[inline(always)]
fn color_transform_delta_lut(t: u8, c: u8) -> u32 {
    u32::from(COLOR_DELTA_LUT[(usize::from(t) << 8) | usize::from(c)])
}

'''
HELP=r'''#[inline(always)]
fn inverse_color_pixel_lut(pixel: &mut [u8], red_to_blue: u8, green_to_blue: u8, green_to_red: u8) {
    let argb = u32::from_le_bytes(pixel[..4].try_into().unwrap());
    let green = ((argb >> 8) & 0xff) as u8;
    let mut red = argb & 0xff;
    let mut blue = (argb >> 16) & 0xff;
    red += color_transform_delta_lut(green_to_red, green);
    blue += color_transform_delta_lut(green_to_blue, green);
    red &= 0xff;
    blue += color_transform_delta_lut(red_to_blue, red as u8);
    blue &= 0xff;
    let out = (argb & 0xff00_ff00) | red | (blue << 16);
    pixel[..4].copy_from_slice(&out.to_le_bytes());
}

'''
FUNC=r'''pub(crate) fn apply_color_transform(
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
            SKIP
            for pixel in block.chunks_exact_mut(4) { inverse_color_pixel_lut(pixel,rb,gb,gr); }
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
 p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text();insert=s.index('fn color_transform_delta(');s=s[:insert]+TABLE+s[insert:];a=s.index('pub(crate) fn apply_color_transform(');b=s.index('pub(crate) fn apply_subtract_green_transform(',a);fn=FUNC.replace('SKIP','if rb == 0 && gb == 0 && gr == 0 { continue; }' if v=='lutzero' else '');s=s[:a]+HELP+fn+s[b:];p.write_text(s)
def inv(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for v in VS:
  r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
  if v!='base':
   patch(r,v);run(['cargo','fmt'],cwd=r)
   for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
  (r/'examples').mkdir(exist_ok=True);(r/'examples/cdlut.rs').write_text(BENCH);run(['cargo','build','--release','--example','cdlut','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/cdlut'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)];corpus={v:[roots[v]/x for x in rels]for v in VS};hot_rel=Path('tests/images/gallery2/3_webp_ll.webp');hot={v:[roots[v]/hot_rel]for v in VS};bh=inv(exes['base'],'h',1,corpus['base'])
 for v in VS[1:]:assert bh==inv(exes[v],'h',1,corpus[v])
 results={}
 for name,files,it in [('corpus',corpus,70),('colorhot',hot,30)]:
  rows=[]
  for n in range(17):
   order=VS if n%2==0 else tuple(reversed(VS));z={}
   for v in order:z[v]=float(inv(exes[v],'t',it,files[v]))
   rows.append(z)
  results[name]=rows
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L color-delta LUT current-tree matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- 64 KiB exact modulo-256 delta table; hashes + full verification passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for name,rows in results.items():
  for v in VS[1:]:q=[z['base']/z[v]for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-color-delta-lut-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
