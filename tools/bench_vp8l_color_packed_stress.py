#!/usr/bin/env python3
import os,re,shutil,statistics,subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44';TMP=Path('/tmp/vp8l-color-stress')
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.run(c,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,env=env)
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];z=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+z+(z&1)
 return o
HELPER=r'''#[inline(always)]
fn inverse_color_pixel_packed(pixel: &mut [u8], red_to_blue: u8, green_to_blue: u8, green_to_red: u8) {
    let argb = u32::from_le_bytes(pixel[..4].try_into().unwrap());
    let green = ((argb >> 8) & 0xff) as u8;
    let mut red = argb & 0xff;
    let mut blue = (argb >> 16) & 0xff;
    red += color_transform_delta(green_to_red as i8, green as i8);
    blue += color_transform_delta(green_to_blue as i8, green as i8);
    red &= 0xff;
    blue += color_transform_delta(red_to_blue as i8, red as u8 as i8);
    blue &= 0xff;
    let out = (argb & 0xff00_ff00) | red | (blue << 16);
    pixel[..4].copy_from_slice(&out.to_le_bytes());
}

'''
PACKED=r'''pub(crate) fn apply_color_transform(
    image_data: &mut [u8], width: u16, size_bits: u8, transform_data: &[u8],
) {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);
    let tile = 1usize << size_bits;
    let safe = width & !(tile - 1);
    for (y, row) in image_data.chunks_exact_mut(width * 4).enumerate() {
        let row_tf = &transform_data[(y >> size_bits) * block_xsize * 4..];
        let (full, tail) = row.split_at_mut(safe * 4);
        for (block, transform) in full.chunks_exact_mut(tile * 4).zip(row_tf.chunks_exact(4)) {
            let rb = transform[0]; let gb = transform[1]; let gr = transform[2];
            for pixel in block.chunks_exact_mut(4) { inverse_color_pixel_packed(pixel, rb, gb, gr); }
        }
        if !tail.is_empty() {
            let transform = &row_tf[(safe / tile) * 4..][..4];
            let rb = transform[0]; let gb = transform[1]; let gr = transform[2];
            for pixel in tail.chunks_exact_mut(4) { inverse_color_pixel_packed(pixel, rb, gb, gr); }
        }
    }
}

'''
TESTS=r'''
#[cfg(test)]
mod packed_color_stress_tests {
    use super::*;
    fn reference(image_data: &mut [u8], width: u16, size_bits: u8, transform_data: &[u8]) {
        let block_xsize = usize::from(subsample_size(width, size_bits));
        let width = usize::from(width);
        for (y, row) in image_data.chunks_exact_mut(width * 4).enumerate() {
            let y_block = y >> size_bits;
            for (x, pixel) in row.chunks_exact_mut(4).enumerate() {
                let x_block = x >> size_bits;
                let transform = &transform_data[(y_block * block_xsize + x_block) * 4..][..4];
                let green = u32::from(pixel[1]);
                let mut red = u32::from(pixel[0]);
                let mut blue = u32::from(pixel[2]);
                red += color_transform_delta(transform[2] as i8, green as i8);
                blue += color_transform_delta(transform[1] as i8, green as i8);
                blue += color_transform_delta(transform[0] as i8, red as i8);
                pixel[0] = (red & 0xff) as u8;
                pixel[2] = (blue & 0xff) as u8;
            }
        }
    }
    fn next(s: &mut u64) -> u8 { *s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407); (*s >> 33) as u8 }
    #[test]
    fn packed_color_matches_reference_matrix() {
        let widths=[1u16,2,3,4,5,7,8,15,16,17,31,32,33,63,64,65,127,128,129,255,257];
        let heights=[1u16,2,3,7,16];
        for seed0 in [1u64,0x123456789abcdef,0xfedcba9876543210] {
            for &width in &widths { for &height in &heights { for size_bits in 2u8..=7 {
                let bx=usize::from(subsample_size(width,size_bits));
                let by=usize::from(subsample_size(height,size_bits));
                let mut seed=seed0 ^ u64::from(width) ^ (u64::from(height)<<16) ^ (u64::from(size_bits)<<32);
                let mut data=vec![0u8;usize::from(width)*usize::from(height)*4];
                for x in &mut data {*x=next(&mut seed);}
                let mut tf=vec![0u8;bx*by*4];for x in &mut tf {*x=next(&mut seed);}
                let mut a=data.clone();let mut b=data.clone();reference(&mut a,width,size_bits,&tf);apply_color_transform(&mut b,width,size_bits,&tf);assert_eq!(a,b,"w={width} h={height} bits={size_bits} seed={seed0}");
                for coeff in [0u8,1,127,128,255] { for t in tf.chunks_exact_mut(4){t[0]=coeff;t[1]=coeff;t[2]=coeff;t[3]=0;} let mut a=data.clone();let mut b=data.clone();reference(&mut a,width,size_bits,&tf);apply_color_transform(&mut b,width,size_bits,&tf);assert_eq!(a,b,"constant coeff={coeff} w={width} h={height} bits={size_bits}"); }
            }}}
        }
    }
}
'''
def patch(root):
 p=root/'src/lossless/decoder/reverse_transform.rs';s=p.read_text();a=s.index('pub(crate) fn apply_color_transform(');b=s.index('pub(crate) fn apply_subtract_green_transform(',a);p.write_text(s[:a]+HELPER+PACKED+s[b:]+TESTS)
def patch_probe(root):
 p=root/'src/lossless/decoder/mod.rs';s=p.read_text();old='''                    TransformType::ColorTransform {\n                        size_bits,\n                        transform_data,\n                    }\n''';new='''                    { let nz = transform_data.chunks_exact(4).map(|t| usize::from(t[0]!=0)+usize::from(t[1]!=0)+usize::from(t[2]!=0)).sum::<usize>(); eprintln!("COLOR_META bits={} blocks={} nz={} total={}", size_bits, transform_data.len()/4, nz, (transform_data.len()/4)*3); }\n                    TransformType::ColorTransform {\n                        size_bits,\n                        transform_data,\n                    }\n'''
 if old not in s:raise SystemExit('probe marker');p.write_text(s.replace(old,new,1))
def prep(name):
 r=TMP/name;run(['git','worktree','add','--detach',str(r),BASE])
 if name=='cand':patch(r);run(['cargo','fmt'],cwd=r);run(['cargo','test','-q'],cwd=r);run(['cargo','doc','-q'],cwd=r);run(['cargo','clippy','--all-features','--','-D','warnings'],cwd=r);run(['cargo','fmt','--','--check'],cwd=r);run(['cargo','+1.80.1','build','-q'],cwd=r)
 if name=='probe':patch_probe(r);run(['cargo','fmt'],cwd=r)
 return r
def make(path,w,h,mode):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    if mode=='large':r=(x*3+y*5+((x>>5)^(y>>4))*17)&255;g=(x*2+y*7+((x*y)>>10))&255;b=(x*11+y*3+((x+y)>>3)*9)&255
    elif mode=='color':g=(x*9+y*13+((x>>3)^(y>>4))*21)&255;r=(g+((x*5-y*3)&255))&255;b=(g+((y*7-x*2)&255))&255
    elif mode=='rgcorr':g=(x*7+y*11+((x>>4)^(y>>5))*19)&255;r=(g+((x+y)&31)-16)&255;b=(x*29+y*3+((x*y)>>9))&255
    elif mode=='bgcorr':g=(x*5+y*17+((x>>3)^(y>>4))*13)&255;b=(g+((x*3+y)&31)-16)&255;r=(x*23+y*7+((x*y)>>8))&255
    elif mode=='gray':g=(x*13+y*9+((x>>4)^(y>>4))*17)&255;r=g;b=g
    elif mode=='tiles':q=((x>>5)+3*(y>>5))&15;r=(q*17)&255;g=(q*53)&255;b=(q*91)&255
    else:z=(x*1103515245+y*12345+((x*y)*2654435761))&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
    i=x*3;row[i:i+3]=bytes((r,g,b))
   f.write(row)
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def build(r,name):
 (r/'examples').mkdir(exist_ok=True);(r/f'examples/{name}.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example',name,'-q'],cwd=r,env=e);return r/f'target/release/examples/{name}'
def invoke(b,m,n,ps):return run(['taskset','-c','0',str(b),m,str(n),*[str(x)for x in ps]],cap=True).stdout.strip()
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();base=prep('base');cand=prep('cand');probe=prep('probe');rels=[p.relative_to(base)for p in sorted((base/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p.read_bytes())and b'ANIM'not in chunks(p.read_bytes())]
 fx={};modes=('large','color','rgcorr','bgcorr','gray','tiles','chaos')
 for mode in modes:
  ppm=TMP/f'{mode}.ppm';webp=TMP/f'{mode}.webp';make(ppm,1152,896,mode);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);fx[mode]=webp
 # Probe actual color-transform metadata.
 (probe/'examples').mkdir(exist_ok=True);(probe/'examples/probe.rs').write_text('''use image_webp::WebPDecoder;use std::io::Cursor;fn main(){for p in std::env::args().skip(1){eprintln!("FILE {}",p);let d=std::fs::read(&p).unwrap();let mut q=WebPDecoder::new(Cursor::new(d)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();}}''');run(['cargo','build','--release','--example','probe','-q'],cwd=probe);pr=run([str(probe/'target/release/examples/probe'),*[str(fx[m])for m in modes]],cwd=probe,cap=True);meta={};parts=re.split(r'FILE ',pr.stderr)[1:]
 for part in parts:
  ls=part.splitlines();name=Path(ls[0]).stem;records=re.findall(r'COLOR_META bits=(\d+) blocks=(\d+) nz=(\d+) total=(\d+)',part);meta[name]=records[-1] if records else None
 bb=build(base,'stress');cb=build(cand,'stress');bf=[base/r for r in rels];cf=[cand/r for r in rels]
 if invoke(bb,'h',1,bf+list(fx.values()))!=invoke(cb,'h',1,cf+list(fx.values())):raise SystemExit('hash mismatch')
 workloads={'corpus':(bf,cf,70)}
 for m in modes:workloads[m]=([fx[m]],[fx[m]],8)
 rows=[]
 for rnd in range(1,22):
  order=('base','cand')if rnd%2 else('cand','base')
  for w,(bps,cps,n) in workloads.items():
   for v in order:rows.append((w,rnd,v,float(invoke(bb if v=='base' else cb,'t',n,bps if v=='base' else cps))))
 vals={};pairs={}
 for w,r,v,x in rows:vals.setdefault((w,v),[]).append(x);pairs.setdefault((w,r),{})[v]=x
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True).stdout.strip();L=['# Deep VP8L packed-color stress','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- 21 alternating paired rounds; exhaustive randomized width/height/size-bit property test + full hashes/tests/docs/Clippy/fmt/MSRV passed','','| workload | color metadata | baseline | candidate | paired median | positive | range |','|---|---|---:|---:|---:|---:|---:|']
 for w in workloads:
  q=[z['base']/z['cand']for(ww,_),z in sorted(pairs.items())if ww==w];md='—' if w=='corpus' else ('none' if meta.get(w) is None else f'bits={meta[w][0]}, nz={meta[w][2]}/{meta[w][3]}');L.append(f'| {w} | {md} | {statistics.median(vals[w,"base"]):.3f} us | {statistics.median(vals[w,"cand"]):.3f} us | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-color-packed-stress.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
