#!/usr/bin/env python3
import re,shutil,subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44';TMP=Path('/tmp/vp8l-color-fixture-fixed')
def run(c,cwd=None,cap=False):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.run(c,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
 subprocess.run(c,cwd=cwd,check=True)
def make(path,w,h,mode):
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
 TMP.mkdir();root=TMP/'tree';run(['git','worktree','add','--detach',str(root),BASE]);p=root/'src/lossless/decoder/mod.rs';s=p.read_text();marker='            let transform_type_val = self.bit_reader.read_bits::<u8>(2)?;\n'
 if marker not in s:raise SystemExit('marker')
 p.write_text(s.replace(marker,marker+'            eprintln!("VP8L_TRANSFORM {}", transform_type_val);\n',1));run(['cargo','fmt'],cwd=root)
 (root/'examples').mkdir(exist_ok=True);(root/'examples/tprobe.rs').write_text('''use image_webp::WebPDecoder;use std::io::Cursor;fn main(){for p in std::env::args().skip(1){eprintln!("FILE {}",p);let d=std::fs::read(&p).unwrap();let mut x=WebPDecoder::new(Cursor::new(d)).unwrap();let mut b=vec![0;x.output_buffer_size().unwrap()];x.read_image(&mut b).unwrap();}}''');run(['cargo','build','--release','--example','tprobe','-q'],cwd=root)
 fs=[]
 for mode in('large','color'):
  ppm=TMP/(mode+'.ppm');webp=TMP/(mode+'.webp');make(ppm,1792,1536,mode);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);fs.append(webp)
 q=run([str(root/'target/release/examples/tprobe'),*[str(x)for x in fs]],cap=True);parts=re.split(r'FILE ',q.stderr)[1:];L=['# Generated VP8L fixture transform coverage','',f'- baseline: `{BASE}`','','| fixture | transforms | has color transform |','|---|---|---|']
 for part in parts:
  lines=part.splitlines();name=Path(lines[0]).name;types=[int(x)for x in re.findall(r'VP8L_TRANSFORM (\d+)',part)];L.append(f'| {name} | {types} | {1 in types} |')
 Path('analysis-vp8l-color-fixture.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
