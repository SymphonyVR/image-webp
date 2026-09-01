#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path
BASE='0881ec1a66f09e11b766c309cf6e651077775bd9';TMP=Path('/tmp/vp8l-secondary-current-final');VS=('base','green','stack','green-stack','all')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
GREEN=r'''pub(crate) fn apply_subtract_green_transform(image_data: &mut [u8]) {
    for pixel in image_data.chunks_exact_mut(4) {
        let value = u32::from_le_bytes(pixel.try_into().unwrap());
        let green = (value >> 8) & 0xff;
        let red_blue = ((value & 0x00ff_00ff).wrapping_add(green | (green << 16))) & 0x00ff_00ff;
        pixel.copy_from_slice(&((value & 0xff00_ff00) | red_blue).to_le_bytes());
    }
}
'''
STACK_OLD=r'''    let expanded_lookup_table_storage: Vec<[u8; EXP_ENTRY_SIZE]> = (0..256u16)
        .map(|packed_byte_value_u16| {
            let mut entry_pixels_array = [0u8; EXP_ENTRY_SIZE]; // Uses const generic
            let packed_byte_value = packed_byte_value_u16 as u8;

            // Loop bound is effectively constant for each instantiation.
            for pixel_sub_index in 0..pixels_per_packed_byte_usize {
                let shift_amount = (pixel_sub_index as u8) * bits_per_entry_u8;
                let k = (packed_byte_value >> shift_amount) & mask_u8;

                let color_source_array: [u8; 4] = if k < table_size {
                    let color_data_offset = usize::from(k) * 4;
                    table_data[color_data_offset..color_data_offset + 4]
                        .try_into()
                        .unwrap()
                } else {
                    [0u8; 4] // WebP spec: out-of-bounds indices are [0,0,0,0]
                };

                let array_fill_offset = pixel_sub_index * 4;
                entry_pixels_array[array_fill_offset..array_fill_offset + 4]
                    .copy_from_slice(&color_source_array);
            }
            entry_pixels_array
        })
        .collect();

    let expanded_lookup_table_array: &[[u8; EXP_ENTRY_SIZE]; 256] =
        expanded_lookup_table_storage.as_slice().try_into().unwrap();
'''
STACK_NEW=r'''    let mut expanded_lookup_table_array = [[0u8; EXP_ENTRY_SIZE]; 256];
    for (packed_byte_value, entry_pixels_array) in expanded_lookup_table_array.iter_mut().enumerate() {
        let packed_byte_value = packed_byte_value as u8;
        for pixel_sub_index in 0..pixels_per_packed_byte_usize {
            let shift_amount = (pixel_sub_index as u8) * bits_per_entry_u8;
            let k = (packed_byte_value >> shift_amount) & mask_u8;
            let color_source_array: [u8; 4] = if k < table_size {
                let color_data_offset = usize::from(k) * 4;
                table_data[color_data_offset..color_data_offset + 4].try_into().unwrap()
            } else { [0u8; 4] };
            let array_fill_offset = pixel_sub_index * 4;
            entry_pixels_array[array_fill_offset..array_fill_offset + 4].copy_from_slice(&color_source_array);
        }
    }
'''
NOSCRATCH=r'''    for y_rev_idx in 0..height as usize {
        let y = height as usize - 1 - y_rev_idx;
        let packed_row_input_global_offset = y * input_stride_bytes_packed;
        let output_row_global_offset = y * output_stride_bytes_expanded;
        for block_index in (0..packed_image_width_in_blocks).rev() {
            let packed_index = image_data[packed_row_input_global_offset + block_index * 4 + 1];
            let output_offset = output_row_global_offset + block_index * EXP_ENTRY_SIZE;
            let copy_len = if block_index + 1 == packed_image_width_in_blocks { final_block_expanded_size_bytes } else { EXP_ENTRY_SIZE };
            image_data[output_offset..output_offset + copy_len].copy_from_slice(&expanded_lookup_table_array[packed_index as usize][..copy_len]);
        }
    }
'''
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(p):
 d=p.read_bytes();o=[];q=12
 if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP':return o
 while q+8<=len(d):t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
 return o
def patch(root,v):
 p=root/'src/lossless/decoder/reverse_transform.rs';s=p.read_text()
 if v in ('green','green-stack','all'):
  a=s.index('pub(crate) fn apply_subtract_green_transform(');b=s.index('\npub(crate) fn apply_color_indexing_transform(',a);s=s[:a]+GREEN+s[b:]
 if v in ('stack','green-stack','all'):
  assert STACK_OLD in s;s=s.replace(STACK_OLD,STACK_NEW,1)
 if v=='all':
  a=s.index('    let mut packed_indices_for_row: Vec<u8> = vec![0; packed_image_width_in_blocks];');b=s.index('\n}\n\n//predictor functions',a);s=s[:a]+NOSCRATCH+s[b:]
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
  (r/'examples').mkdir(exist_ok=True);(r/'examples/sec.rs').write_text(BENCH);run(['cargo','build','--release','--example','sec','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/sec'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
 w=h=2048;colors=[(10,20,30),(230,40,80),(20,220,60),(80,90,240),(240,210,20),(160,30,200),(30,200,210),(245,245,245)]
 for kind in ('palette','green'):
  ppm=TMP/f'{kind}.ppm'
  with ppm.open('wb')as f:
   f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
   for y in range(h):
    for x in range(w):
     if kind=='palette':c=colors[((x>>5)+(y>>5)*3)&7]
     else:g=(x*3+y*5+((x>>4)^(y>>4))*7)&255;c=(g,g,g)
     i=x*3;row[i:i+3]=bytes(c)
    f.write(row)
  run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(TMP/f'{kind}.webp')])
 corpus={v:[roots[v]/x for x in rels]for v in VS};extras=[TMP/'palette.webp',TMP/'green.webp'];bh=inv(exes['base'],'h',1,corpus['base']+extras)
 for v in VS[1:]:assert bh==inv(exes[v],'h',1,corpus[v]+extras)
 workloads={'corpus':(corpus,50),'palette':({v:[TMP/'palette.webp']for v in VS},3),'green':({v:[TMP/'green.webp']for v in VS},3)};res={}
 for label,(files,it)in workloads.items():
  rows=[]
  for n in range(13):
   order=VS if n%2==0 else tuple(reversed(VS));z={}
   for v in order:z[v]=float(inv(exes[v],'t',it,files[v]))
   rows.append(z)
  res[label]=rows
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L secondary transforms current-final matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for label,rows in res.items():
  for v in VS[1:]:q=[z['base']/z[v]for z in rows];L.append(f'| {label} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-secondary-current-final.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
