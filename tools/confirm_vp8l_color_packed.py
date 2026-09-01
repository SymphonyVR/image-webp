#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44';TMP=Path('/tmp/vp8l-color-packed-confirm')
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def patch(root):
 p=root/'src/lossless/decoder/reverse_transform.rs';s=p.read_text();a=s.index('pub(crate) fn apply_color_transform(');b=s.index('pub(crate) fn apply_subtract_green_transform(',a)
 helper='''#[inline(always)]\nfn inverse_color_pixel_packed(pixel: &mut [u8], red_to_blue: u8, green_to_blue: u8, green_to_red: u8) {\n    let argb = u32::from_le_bytes(pixel[..4].try_into().unwrap());\n    let green = ((argb >> 8) & 0xff) as u8;\n    let mut red = argb & 0xff;\n    let mut blue = (argb >> 16) & 0xff;\n    red += color_transform_delta(green_to_red as i8, green as i8);\n    blue += color_transform_delta(green_to_blue as i8, green as i8);\n    red &= 0xff;\n    blue += color_transform_delta(red_to_blue as i8, red as u8 as i8);\n    blue &= 0xff;\n    let out = (argb & 0xff00_ff00) | red | (blue << 16);\n    pixel[..4].copy_from_slice(&out.to_le_bytes());\n}\n\n'''
 fn='''pub(crate) fn apply_color_transform(\n    image_data: &mut [u8], width: u16, size_bits: u8, transform_data: &[u8],\n) {\n    let block_xsize = usize::from(subsample_size(width, size_bits));\n    let width = usize::from(width);\n    let tile = 1usize << size_bits;\n    let safe = width & !(tile - 1);\n    for (y, row) in image_data.chunks_exact_mut(width * 4).enumerate() {\n        let row_tf = &transform_data[(y >> size_bits) * block_xsize * 4..];\n        let (full, tail) = row.split_at_mut(safe * 4);\n        for (block, transform) in full.chunks_exact_mut(tile * 4).zip(row_tf.chunks_exact(4)) {\n            let rb = transform[0]; let gb = transform[1]; let gr = transform[2];\n            for pixel in block.chunks_exact_mut(4) { inverse_color_pixel_packed(pixel, rb, gb, gr); }\n        }\n        if !tail.is_empty() {\n            let transform = &row_tf[(safe / tile) * 4..][..4];\n            let rb = transform[0]; let gb = transform[1]; let gr = transform[2];\n            for pixel in tail.chunks_exact_mut(4) { inverse_color_pixel_packed(pixel, rb, gb, gr); }\n        }\n    }\n}\n\n'''
 p.write_text(s[:a]+helper+fn+s[b:])
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];z=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+z+(z&1)
 return o
BENCH='''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def inv(b,m,n,ps):return run(['taskset','-c','0',str(b),m,str(n),*[str(x)for x in ps]],cap=True)
def make_ppm(path,w,h,mode):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());r=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    i=x*3
    if mode=='large':rv=(x*3+y*5+((x>>5)^(y>>4))*17)&255;g=(x*2+y*7+((x*y)>>10))&255;b=(x*11+y*3+((x+y)>>3)*9)&255
    else:g=(x*9+y*13+((x>>3)^(y>>4))*21)&255;rv=(g+((x*5-y*3)&255))&255;b=(g+((y*7-x*2)&255))&255
    r[i:i+3]=bytes((rv,g,b))
   f.write(r)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();base=TMP/'base';cand=TMP/'cand';run(['git','worktree','add','--detach',str(base),BASE]);run(['git','worktree','add','--detach',str(cand),BASE]);patch(cand);run(['cargo','fmt'],cwd=cand);run(['cargo','test','-q'],cwd=cand);run(['cargo','doc','-q'],cwd=cand);run(['cargo','clippy','--all-features','--','-D','warnings'],cwd=cand);run(['cargo','fmt','--','--check'],cwd=cand);run(['cargo','+1.80.1','build','-q'],cwd=cand)
 rel=[p.relative_to(base)for p in sorted((base/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p.read_bytes())and b'ANIM'not in chunks(p.read_bytes())]
 fx={}
 for mode in('large','color'):
  ppm=TMP/(mode+'.ppm');webp=TMP/(mode+'.webp');make_ppm(ppm,1792,1536,mode);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);fx[mode]=webp
 bins={}
 for n,r in(('base',base),('cand',cand)):
  (r/'examples').mkdir(exist_ok=True);(r/'examples/colorconfirm.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','colorconfirm','-q'],cwd=r,env=e);bins[n]=r/'target/release/examples/colorconfirm'
 if inv(bins['base'],'h',1,[*[base/x for x in rel],*fx.values()])!=inv(bins['cand'],'h',1,[*[cand/x for x in rel],*fx.values()]):raise SystemExit('hash mismatch')
 rows=[]
 for rnd in range(1,26):
  order=('base','cand')if rnd%2 else('cand','base')
  for n in order:
   root=base if n=='base'else cand;rows.append(('corpus',rnd,n,float(inv(bins[n],'t',70,[root/x for x in rel]))));rows.append(('large',rnd,n,float(inv(bins[n],'t',4,[fx['large']]))));rows.append(('color',rnd,n,float(inv(bins[n],'t',4,[fx['color']]))))
 rr={};vals={}
 for w,r,n,x in rows:rr.setdefault((w,r),{})[n]=x;vals.setdefault((w,n),[]).append(x)
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# Final VP8L packed-color confirmation','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- 25 alternating paired rounds; full hashes/tests/docs/Clippy/fmt/MSRV passed','','| workload | baseline | candidate | paired median | positive | range |','|---|---:|---:|---:|---:|---:|']
 for w in('corpus','large','color'):
  q=[z['base']/z['cand']for(ww,_),z in sorted(rr.items())if ww==w];L.append(f'| {w} | {statistics.median(vals[w,"base"]):.3f} us | {statistics.median(vals[w,"cand"]):.3f} us | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-color-packed-confirm-v2.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
