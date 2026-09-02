#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='84d8d20753fce0a9972e8a244fdf929b5a55671c';TMP=Path('/tmp/vp8l-staged-rows');VS=('base','r8','r16','r32')
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
def patch_reverse(r):
 p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text()
 a=s.index('pub(crate) fn apply_predictor_transform(');b=s.index('pub fn apply_predictor_transform_0(',a)
 pred=r'''pub(crate) fn apply_predictor_transform(
    image_data: &mut [u8],
    width: u16,
    height: u16,
    size_bits: u8,
    predictor_data: &[u8],
) -> Result<(), DecodingError> {
    apply_predictor_transform_rows(
        image_data,
        width,
        height,
        size_bits,
        predictor_data,
        0,
        height,
    )
}

pub(crate) fn apply_predictor_transform_rows(
    image_data: &mut [u8],
    width: u16,
    height: u16,
    size_bits: u8,
    predictor_data: &[u8],
    start_row: u16,
    end_row: u16,
) -> Result<(), DecodingError> {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);
    let height = usize::from(height);
    let start_row = usize::from(start_row);
    let end_row = usize::from(end_row);
    assert!(start_row <= end_row && end_row <= height);
    if start_row == end_row {
        return Ok(());
    }

    if start_row == 0 {
        image_data[3] = image_data[3].wrapping_add(255);
        apply_predictor_transform_1(image_data, 4..width * 4, width);
    }

    let first_row = start_row.max(1);
    for y in first_row..end_row {
        for i in 0..4 {
            image_data[y * width * 4 + i] =
                image_data[y * width * 4 + i].wrapping_add(image_data[(y - 1) * width * 4 + i]);
        }
    }

    for y in first_row..end_row {
        for block_x in 0..block_xsize {
            let block_index = (y >> size_bits) * block_xsize + block_x;
            let predictor = predictor_data[block_index * 4 + 1];
            let start_index = (y * width + (block_x << size_bits).max(1)) * 4;
            let end_index = (y * width + ((block_x + 1) << size_bits).min(width)) * 4;

            match predictor {
                0 => apply_predictor_transform_0(image_data, start_index..end_index, width),
                1 => apply_predictor_transform_1(image_data, start_index..end_index, width),
                2 => apply_predictor_transform_2(image_data, start_index..end_index, width),
                3 => apply_predictor_transform_3(image_data, start_index..end_index, width),
                4 => apply_predictor_transform_4(image_data, start_index..end_index, width),
                5 => apply_predictor_transform_5(image_data, start_index..end_index, width),
                6 => apply_predictor_transform_6(image_data, start_index..end_index, width),
                7 => apply_predictor_transform_7(image_data, start_index..end_index, width),
                8 => apply_predictor_transform_8(image_data, start_index..end_index, width),
                9 => apply_predictor_transform_9(image_data, start_index..end_index, width),
                10 => apply_predictor_transform_10(image_data, start_index..end_index, width),
                11 => apply_predictor_transform_11(image_data, start_index..end_index, width),
                12 => apply_predictor_transform_12(image_data, start_index..end_index, width),
                13 => apply_predictor_transform_13(image_data, start_index..end_index, width),
                _ => {}
            }
        }
    }

    Ok(())
}
'''
 s=s[:a]+pred+s[b:]
 a=s.index('pub(crate) fn apply_color_transform(');b=s.index('pub(crate) fn apply_subtract_green_transform(',a)
 color=r'''pub(crate) fn apply_color_transform(
    image_data: &mut [u8],
    width: u16,
    size_bits: u8,
    transform_data: &[u8],
) {
    let row_bytes = usize::from(width) * 4;
    let height = image_data.len() / row_bytes;
    apply_color_transform_rows(
        image_data,
        width,
        size_bits,
        transform_data,
        0,
        height as u16,
    );
}

pub(crate) fn apply_color_transform_rows(
    image_data: &mut [u8],
    width: u16,
    size_bits: u8,
    transform_data: &[u8],
    start_row: u16,
    end_row: u16,
) {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);
    let start_row = usize::from(start_row);
    let end_row = usize::from(end_row);
    let row_bytes = width * 4;
    assert!(start_row <= end_row && end_row * row_bytes <= image_data.len());

    for (dy, row) in image_data[start_row * row_bytes..end_row * row_bytes]
        .chunks_exact_mut(row_bytes)
        .enumerate()
    {
        let y = start_row + dy;
        let row_transform_data_start = (y >> size_bits) * block_xsize * 4;
        let row_tf_data = &transform_data[row_transform_data_start..];

        for (block, transform) in row
            .chunks_mut(4 << size_bits)
            .zip(row_tf_data.chunks_exact(4))
        {
            let red_to_blue = transform[0];
            let green_to_blue = transform[1];
            let green_to_red = transform[2];

            for pixel in block.chunks_exact_mut(4) {
                inverse_color_pixel_packed(pixel, red_to_blue, green_to_blue, green_to_red);
            }
        }
    }
}

'''
 p.write_text(s[:a]+color+s[b:])
def patch_mod(r,batch):
 p=r/'src/lossless/decoder/mod.rs';s=p.read_text()
 old='''use reverse_transform::{\n    apply_color_indexing_transform, apply_color_transform, apply_predictor_transform,\n    apply_subtract_green_transform, TransformType,\n};'''
 new='''use reverse_transform::{\n    apply_color_indexing_transform, apply_color_transform, apply_color_transform_rows,\n    apply_predictor_transform, apply_predictor_transform_rows, apply_subtract_green_transform,\n    TransformType,\n};'''
 assert old in s;s=s.replace(old,new,1)
 a=s.index('        let mut image_size = transformed_size;');b=s.index('\n\n        Ok(())',a)
 body=f'''        let has_color_indexing = self.transform_order.iter().any(|&trans_index| {{\n            matches!(\n                self.transforms[usize::from(trans_index)].as_ref(),\n                Some(TransformType::ColorIndexingTransform {{ .. }})\n            )\n        }});\n\n        if has_color_indexing {{\n            let mut image_size = transformed_size;\n            let mut width = transformed_width;\n            for &trans_index in self.transform_order.iter().rev() {{\n                let transform = self.transforms[usize::from(trans_index)].as_ref().unwrap();\n                match transform {{\n                    TransformType::PredictorTransform {{\n                        size_bits,\n                        predictor_data,\n                    }} => apply_predictor_transform(\n                        &mut buf[..image_size],\n                        width,\n                        self.height,\n                        *size_bits,\n                        predictor_data,\n                    )?,\n                    TransformType::ColorTransform {{\n                        size_bits,\n                        transform_data,\n                    }} => apply_color_transform(\n                        &mut buf[..image_size],\n                        width,\n                        *size_bits,\n                        transform_data,\n                    ),\n                    TransformType::SubtractGreen => {{\n                        apply_subtract_green_transform(&mut buf[..image_size]);\n                    }}\n                    TransformType::ColorIndexingTransform {{\n                        table_size,\n                        table_data,\n                    }} => {{\n                        width = self.width;\n                        image_size = usize::from(width) * usize::from(self.height) * 4;\n                        apply_color_indexing_transform(\n                            buf,\n                            width,\n                            self.height,\n                            *table_size,\n                            table_data,\n                        );\n                    }}\n                }}\n            }}\n        }} else {{\n            const ROW_BATCH: u16 = {batch};\n            let width = transformed_width;\n            let row_bytes = usize::from(width) * 4;\n            let has_predictor = self.transform_order.iter().any(|&trans_index| {{\n                matches!(\n                    self.transforms[usize::from(trans_index)].as_ref(),\n                    Some(TransformType::PredictorTransform {{ .. }})\n                )\n            }});\n            let mut predictor_row = if has_predictor {{\n                vec![0u8; row_bytes]\n            }} else {{\n                Vec::new()\n            }};\n            let mut saved_previous_row = if has_predictor {{\n                vec![0u8; row_bytes]\n            }} else {{\n                Vec::new()\n            }};\n\n            let mut start_row = 0u16;\n            while start_row < self.height {{\n                let end_row = (start_row + ROW_BATCH).min(self.height);\n                for &trans_index in self.transform_order.iter().rev() {{\n                    let transform = self.transforms[usize::from(trans_index)].as_ref().unwrap();\n                    match transform {{\n                        TransformType::PredictorTransform {{\n                            size_bits,\n                            predictor_data,\n                        }} => {{\n                            if start_row == 0 {{\n                                apply_predictor_transform_rows(\n                                    &mut buf[..transformed_size],\n                                    width,\n                                    self.height,\n                                    *size_bits,\n                                    predictor_data,\n                                    start_row,\n                                    end_row,\n                                )?;\n                            }} else {{\n                                let previous_offset =\n                                    (usize::from(start_row) - 1) * row_bytes;\n                                saved_previous_row.copy_from_slice(\n                                    &buf[previous_offset..previous_offset + row_bytes],\n                                );\n                                buf[previous_offset..previous_offset + row_bytes]\n                                    .copy_from_slice(&predictor_row);\n                                apply_predictor_transform_rows(\n                                    &mut buf[..transformed_size],\n                                    width,\n                                    self.height,\n                                    *size_bits,\n                                    predictor_data,\n                                    start_row,\n                                    end_row,\n                                )?;\n                                buf[previous_offset..previous_offset + row_bytes]\n                                    .copy_from_slice(&saved_previous_row);\n                            }}\n                            let last_row_offset =\n                                (usize::from(end_row) - 1) * row_bytes;\n                            predictor_row.copy_from_slice(\n                                &buf[last_row_offset..last_row_offset + row_bytes],\n                            );\n                        }}\n                        TransformType::ColorTransform {{\n                            size_bits,\n                            transform_data,\n                        }} => apply_color_transform_rows(\n                            &mut buf[..transformed_size],\n                            width,\n                            *size_bits,\n                            transform_data,\n                            start_row,\n                            end_row,\n                        ),\n                        TransformType::SubtractGreen => {{\n                            let start = usize::from(start_row) * row_bytes;\n                            let end = usize::from(end_row) * row_bytes;\n                            apply_subtract_green_transform(&mut buf[start..end]);\n                        }}\n                        TransformType::ColorIndexingTransform {{ .. }} => unreachable!(),\n                    }}\n                }}\n                start_row = end_row;\n            }}\n        }}'''
 p.write_text(s[:a]+body+s[b:])
def patch(r,batch):patch_reverse(r);patch_mod(r,batch)
def inv(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for v in VS:
  r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
  if v!='base':
   patch(r,int(v[1:]));run(['cargo','fmt'],cwd=r)
   for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
  (r/'examples').mkdir(exist_ok=True);(r/'examples/staged.rs').write_text(BENCH);run(['cargo','build','--release','--example','staged','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/staged'
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
 results={}
 for name,files,it in [('corpus',corpus,50),('large',{v:[large]for v in VS},3)]:
  rows=[]
  for n in range(13):
   order=VS if n%2==0 else tuple(reversed(VS));z={}
   for v in order:z[v]=float(inv(exes[v],'t',it,files[v]))
   rows.append(z)
  results[name]=rows
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L staged-row current-tree matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- non-palette images only; predictor-stage boundary row preserved; full verification passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for name,rows in results.items():
  for v in VS[1:]:q=[z['base']/z[v]for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-staged-rows-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
