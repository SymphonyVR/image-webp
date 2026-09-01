#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44';TMP=Path('/tmp/vp8l-staged-row-v2');VS=['b8','b16','b32','b64']
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def rep(s,o,n,l):
 if o not in s:raise SystemExit('missing '+l)
 return s.replace(o,n,1)
PRED_ROWS=r'''pub(crate) fn apply_predictor_transform_rows(
    image_data: &mut [u8], width: u16, height: u16, size_bits: u8,
    predictor_data: &[u8], start_row: u16, end_row: u16,
) -> Result<(), DecodingError> {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width); let height = usize::from(height);
    let start_row = usize::from(start_row); let end_row = usize::from(end_row);
    assert!(start_row <= end_row && end_row <= height);
    if start_row == end_row { return Ok(()); }
    if start_row == 0 {
        image_data[3] = image_data[3].wrapping_add(255);
        apply_predictor_transform_1(image_data, 4..width * 4, width);
    }
    let first = start_row.max(1);
    for y in first..end_row {
        for i in 0..4 {
            image_data[y * width * 4 + i] = image_data[y * width * 4 + i]
                .wrapping_add(image_data[(y - 1) * width * 4 + i]);
        }
        for block_x in 0..block_xsize {
            let block_index = (y >> size_bits) * block_xsize + block_x;
            let predictor = predictor_data[block_index * 4 + 1];
            let start_index = (y * width + (block_x << size_bits).max(1)) * 4;
            let end_index = (y * width + ((block_x + 1) << size_bits).min(width)) * 4;
            match predictor {
                0=>apply_predictor_transform_0(image_data,start_index..end_index,width),
                1=>apply_predictor_transform_1(image_data,start_index..end_index,width),
                2=>apply_predictor_transform_2(image_data,start_index..end_index,width),
                3=>apply_predictor_transform_3(image_data,start_index..end_index,width),
                4=>apply_predictor_transform_4(image_data,start_index..end_index,width),
                5=>apply_predictor_transform_5(image_data,start_index..end_index,width),
                6=>apply_predictor_transform_6(image_data,start_index..end_index,width),
                7=>apply_predictor_transform_7(image_data,start_index..end_index,width),
                8=>apply_predictor_transform_8(image_data,start_index..end_index,width),
                9=>apply_predictor_transform_9(image_data,start_index..end_index,width),
                10=>apply_predictor_transform_10(image_data,start_index..end_index,width),
                11=>apply_predictor_transform_11(image_data,start_index..end_index,width),
                12=>apply_predictor_transform_12(image_data,start_index..end_index,width),
                13=>apply_predictor_transform_13(image_data,start_index..end_index,width), _=>{}
            }
        }
    }
    Ok(())
}

'''
COLOR_ROWS=r'''pub(crate) fn apply_color_transform_rows(
    image_data: &mut [u8], width: u16, size_bits: u8, transform_data: &[u8], start_row: u16, end_row: u16,
) {
    let block_xsize=usize::from(subsample_size(width,size_bits)); let width=usize::from(width); let row_bytes=width*4;
    let start=usize::from(start_row); let end=usize::from(end_row);
    for (dy,row) in image_data[start*row_bytes..end*row_bytes].chunks_exact_mut(row_bytes).enumerate() {
        let y=start+dy; let row_tf=&transform_data[(y >> size_bits)*block_xsize*4..];
        for (block,transform) in row.chunks_mut(4 << size_bits).zip(row_tf.chunks_exact(4)) {
            let rb=transform[0];let gb=transform[1];let gr=transform[2];
            for pixel in block.chunks_exact_mut(4) {
                let green=u32::from(pixel[1]);let mut red=u32::from(pixel[0]);let mut blue=u32::from(pixel[2]);
                red+=color_transform_delta(gr as i8,green as i8);blue+=color_transform_delta(gb as i8,green as i8);blue+=color_transform_delta(rb as i8,red as i8);
                pixel[0]=(red&0xff)as u8;pixel[2]=(blue&0xff)as u8;
            }
        }
    }
}

pub(crate) fn apply_subtract_green_transform_rows(image_data:&mut[u8],start_pixel:usize,end_pixel:usize){
    for pixel in image_data[start_pixel*4..end_pixel*4].chunks_exact_mut(4){pixel[0]=pixel[0].wrapping_add(pixel[1]);pixel[2]=pixel[2].wrapping_add(pixel[1]);}
}

'''
def patch(name,root):
 batch=int(name[1:]);rp=root/'src/lossless/decoder/reverse_transform.rs';s=rp.read_text();pos=s.index('pub fn apply_predictor_transform_0(');s=s[:pos]+PRED_ROWS+s[pos:];pos=s.index('pub(crate) fn apply_color_transform(');s=s[:pos]+COLOR_ROWS+s[pos:];rp.write_text(s)
 p=root/'src/lossless/decoder/mod.rs';s=p.read_text();s=rep(s,'''use reverse_transform::{\n    apply_color_indexing_transform, apply_color_transform, apply_predictor_transform,\n    apply_subtract_green_transform, TransformType,\n};''','''use reverse_transform::{\n    apply_color_indexing_transform, apply_color_transform, apply_color_transform_rows,\n    apply_predictor_transform, apply_predictor_transform_rows, apply_subtract_green_transform,\n    apply_subtract_green_transform_rows, TransformType,\n};''','imports')
 a=s.index('        let mut image_size = transformed_size;');b=s.index('\n\n        Ok(())',a)
 body=f'''        let has_color_indexing = self.transform_order.iter().any(|&i| matches!(self.transforms[usize::from(i)].as_ref(), Some(TransformType::ColorIndexingTransform {{ .. }})));\n        if !has_color_indexing {{\n            const ROW_BATCH: u16 = {batch};\n            let width = transformed_width; let row_bytes = usize::from(width) * 4;\n            let has_predictor = self.transform_order.iter().any(|&i| matches!(self.transforms[usize::from(i)].as_ref(), Some(TransformType::PredictorTransform {{ .. }})));\n            let mut predictor_row = has_predictor.then(|| vec![0u8; row_bytes]);\n            let mut final_prev = has_predictor.then(|| vec![0u8; row_bytes]);\n            let mut have_predictor_row = false; let mut start_row = 0u16;\n            while start_row < self.height {{\n                let end_row = (start_row + ROW_BATCH).min(self.height);\n                for &trans_index in self.transform_order.iter().rev() {{\n                    let transform = self.transforms[usize::from(trans_index)].as_ref().unwrap();\n                    match transform {{\n                        TransformType::PredictorTransform {{ size_bits, predictor_data }} => {{\n                            if start_row > 0 && have_predictor_row {{\n                                let prev=(usize::from(start_row)-1)*row_bytes;\n                                final_prev.as_mut().unwrap().copy_from_slice(&buf[prev..prev+row_bytes]);\n                                buf[prev..prev+row_bytes].copy_from_slice(predictor_row.as_ref().unwrap());\n                                apply_predictor_transform_rows(&mut buf[..transformed_size],width,self.height,*size_bits,predictor_data,start_row,end_row)?;\n                                let last=(usize::from(end_row)-1)*row_bytes;predictor_row.as_mut().unwrap().copy_from_slice(&buf[last..last+row_bytes]);\n                                buf[prev..prev+row_bytes].copy_from_slice(final_prev.as_ref().unwrap());\n                            }} else {{\n                                apply_predictor_transform_rows(&mut buf[..transformed_size],width,self.height,*size_bits,predictor_data,start_row,end_row)?;\n                                let last=(usize::from(end_row)-1)*row_bytes;predictor_row.as_mut().unwrap().copy_from_slice(&buf[last..last+row_bytes]);have_predictor_row=true;\n                            }}\n                        }}\n                        TransformType::ColorTransform {{ size_bits, transform_data }} => apply_color_transform_rows(&mut buf[..transformed_size],width,*size_bits,transform_data,start_row,end_row),\n                        TransformType::SubtractGreen => apply_subtract_green_transform_rows(&mut buf[..transformed_size],usize::from(start_row)*usize::from(width),usize::from(end_row)*usize::from(width)),\n                        TransformType::ColorIndexingTransform {{ .. }} => unreachable!(),\n                    }}\n                }}\n                start_row=end_row;\n            }}\n        }} else {{\n            let mut image_size=transformed_size;let mut width=transformed_width;\n            for &trans_index in self.transform_order.iter().rev() {{\n                let transform=self.transforms[usize::from(trans_index)].as_ref().unwrap();\n                match transform {{\n                    TransformType::PredictorTransform {{ size_bits,predictor_data }}=>apply_predictor_transform(&mut buf[..image_size],width,self.height,*size_bits,predictor_data)?,\n                    TransformType::ColorTransform {{ size_bits,transform_data }}=>apply_color_transform(&mut buf[..image_size],width,*size_bits,transform_data),\n                    TransformType::SubtractGreen=>apply_subtract_green_transform(&mut buf[..image_size]),\n                    TransformType::ColorIndexingTransform {{ table_size,table_data }}=>{{width=self.width;image_size=usize::from(width)*usize::from(self.height)*4;apply_color_indexing_transform(buf,width,self.height,*table_size,table_data);}}\n                }}\n            }}\n        }}'''
 p.write_text(s[:a]+body+s[b:])
def ch(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];z=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+z+(z&1)
 return o
BENCH='''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={}
 for n in['base',*VS]:
  r=TMP/n;run(['git','worktree','add','--detach',str(r),BASE]);roots[n]=r
  if n!='base':patch(n,r);run(['cargo','fmt'],cwd=r);run(['cargo','test','-q'],cwd=r);run(['cargo','+1.80.1','build','-q'],cwd=r)
 rel=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in ch(p.read_bytes())and b'ANIM'not in ch(p.read_bytes())];ppm=TMP/'large.ppm';w=1792;h=1536
 with ppm.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):i=x*3;row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
   f.write(row)
 webp=TMP/'large.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);bins={}
 for n,r in roots.items():(r/'examples').mkdir(exist_ok=True);(r/'examples/stage2.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','stage2','-q'],cwd=r,env=e);bins[n]=r/'target/release/examples/stage2'
 def inv(n,m,it,ps):return run(['taskset','-c','0',str(bins[n]),m,str(it),*[str(x)for x in ps]],cap=True)
 bh=inv('base','h',1,[*[roots['base']/x for x in rel],webp])
 for n in VS:
  if inv(n,'h',1,[*[roots[n]/x for x in rel],webp])!=bh:raise SystemExit('hash mismatch '+n)
 rows=[]
 for rnd in range(1,12):
  order=['base',*VS]if rnd%2 else[*reversed(VS),'base']
  for n in order:rows.append(('corpus',rnd,n,float(inv(n,'t',45,[roots[n]/x for x in rel]))));rows.append(('large',rnd,n,float(inv(n,'t',3,[webp]))))
 rr={}
 for w,r,n,x in rows:rr.setdefault((w,r),{})[n]=x
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L correct staged-row matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- reusable predictor-stage row buffers; palette/indexed streams fall back to full passes','- hashes + tests + MSRV passed','','| workload | batch | paired median | positive | range |','|---|---|---:|---:|---:|']
 for w in('corpus','large'):
  for n in VS:q=[z['base']/z[n]for(ww,_),z in sorted(rr.items())if ww==w];L.append(f'| {w} | {n[1:]} | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-staged-row-v2.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
