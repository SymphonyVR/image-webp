#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='84d8d20753fce0a9972e8a244fdf929b5a55671c';TMP=Path('/tmp/vp8l-palette-layout');VS=('base','stack','reverse','both')
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
def patch_stack(s):
 old='''    let expanded_lookup_table_storage: Vec<[u8; EXP_ENTRY_SIZE]> = (0..256u16)\n        .map(|packed_byte_value_u16| {\n            let mut entry_pixels_array = [0u8; EXP_ENTRY_SIZE]; // Uses const generic\n            let packed_byte_value = packed_byte_value_u16 as u8;\n\n            // Loop bound is effectively constant for each instantiation.\n            for pixel_sub_index in 0..pixels_per_packed_byte_usize {\n                let shift_amount = (pixel_sub_index as u8) * bits_per_entry_u8;\n                let k = (packed_byte_value >> shift_amount) & mask_u8;\n\n                let color_source_array: [u8; 4] = if k < table_size {\n                    let color_data_offset = usize::from(k) * 4;\n                    table_data[color_data_offset..color_data_offset + 4]\n                        .try_into()\n                        .unwrap()\n                } else {\n                    [0u8; 4] // WebP spec: out-of-bounds indices are [0,0,0,0]\n                };\n\n                let array_fill_offset = pixel_sub_index * 4;\n                entry_pixels_array[array_fill_offset..array_fill_offset + 4]\n                    .copy_from_slice(&color_source_array);\n            }\n            entry_pixels_array\n        })\n        .collect();\n\n    let expanded_lookup_table_array: &[[u8; EXP_ENTRY_SIZE]; 256] =\n        expanded_lookup_table_storage.as_slice().try_into().unwrap();\n'''
 new='''    let expanded_lookup_table_array: [[u8; EXP_ENTRY_SIZE]; 256] =\n        std::array::from_fn(|packed_byte_value_usize| {\n            let mut entry_pixels_array = [0u8; EXP_ENTRY_SIZE];\n            let packed_byte_value = packed_byte_value_usize as u8;\n\n            for pixel_sub_index in 0..pixels_per_packed_byte_usize {\n                let shift_amount = (pixel_sub_index as u8) * bits_per_entry_u8;\n                let k = (packed_byte_value >> shift_amount) & mask_u8;\n\n                let color_source_array: [u8; 4] = if k < table_size {\n                    let color_data_offset = usize::from(k) * 4;\n                    table_data[color_data_offset..color_data_offset + 4]\n                        .try_into()\n                        .unwrap()\n                } else {\n                    [0u8; 4]\n                };\n\n                let array_fill_offset = pixel_sub_index * 4;\n                entry_pixels_array[array_fill_offset..array_fill_offset + 4]\n                    .copy_from_slice(&color_source_array);\n            }\n            entry_pixels_array\n        });\n'''
 assert old in s;return s.replace(old,new,1)
def patch_reverse(s):
 a=s.index('    let mut packed_indices_for_row: Vec<u8> = vec![0; packed_image_width_in_blocks];')
 b=s.index('\n}\n\n//predictor functions',a)
 new='''    for y_rev_idx in 0..height as usize {\n        let y = height as usize - 1 - y_rev_idx;\n        let packed_row_input_global_offset = y * input_stride_bytes_packed;\n        let output_row_global_offset = y * output_stride_bytes_expanded;\n\n        for block_index in (0..packed_image_width_in_blocks).rev() {\n            let packed_index = image_data[packed_row_input_global_offset + block_index * 4 + 1];\n            let output_offset = output_row_global_offset + block_index * EXP_ENTRY_SIZE;\n            let is_final = block_index + 1 == packed_image_width_in_blocks;\n            if is_final && final_block_expanded_size_bytes != EXP_ENTRY_SIZE {\n                image_data[output_offset..output_offset + final_block_expanded_size_bytes]\n                    .copy_from_slice(\n                        &expanded_lookup_table_array[packed_index as usize]\n                            [..final_block_expanded_size_bytes],\n                    );\n            } else {\n                let dst: &mut [u8; EXP_ENTRY_SIZE] = image_data\n                    [output_offset..output_offset + EXP_ENTRY_SIZE]\n                    .try_into()\n                    .unwrap();\n                *dst = expanded_lookup_table_array[packed_index as usize];\n            }\n        }\n    }\n'''
 return s[:a]+new+s[b:]
def patch(r,v):
 p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text()
 if v in ('stack','both'):s=patch_stack(s)
 if v in ('reverse','both'):s=patch_reverse(s)
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
  (r/'examples').mkdir(exist_ok=True);(r/'examples/pal.rs').write_text(BENCH);run(['cargo','build','--release','--example','pal','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/pal'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
 ppm=TMP/'palette.ppm';w=h=2048;colors=[(10,20,30),(230,40,80),(20,220,60),(80,90,240),(240,210,20),(160,30,200),(30,200,210),(245,245,245)]
 with ppm.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):c=colors[((x>>5)+(y>>5)*3)&7];i=x*3;row[i:i+3]=bytes(c)
   f.write(row)
 palette=TMP/'palette.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(palette)])
 corpus={v:[roots[v]/x for x in rels]for v in VS};bh=inv(exes['base'],'h',1,corpus['base']+[palette])
 for v in VS[1:]:assert bh==inv(exes[v],'h',1,corpus[v]+[palette])
 results={}
 for name,files,it in [('corpus',corpus,60),('palette',{v:[palette]for v in VS},4)]:
  rows=[]
  for n in range(17):
   order=VS if n%2==0 else tuple(reversed(VS));z={}
   for v in order:z[v]=float(inv(exes[v],'t',it,files[v]))
   rows.append(z)
  results[name]=rows
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L small-palette layout current-tree matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- stack lookup table and scratchless reverse expansion; full verification passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for name,rows in results.items():
  for v in VS[1:]:q=[z['base']/z[v]for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-palette-layout-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
