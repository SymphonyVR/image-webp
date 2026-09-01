#!/usr/bin/env python3
import re,subprocess,shutil
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44';TMP=Path('/tmp/vp8l-meta-fixed')
def run(c,cwd=None,cap=False):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.run(c,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
 subprocess.run(c,cwd=cwd,check=True)
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 out=[];p=12
 while p+8<=len(d):f=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');out.append(f);p+=8+n+(n&1)
 return out
def make(path,w,h,kind):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    i=x*3
    if kind=='structured':a=(x*5+y*3+((x>>4)^(y>>3))*29)&255;b=(x*13+y*7+((x*y)>>8))&255;c=(x*2+y*17+((x+y)>>2)*11)&255
    elif kind=='tiles':q=((x>>5)+3*(y>>5))&15;a=(q*17)&255;b=((q*53)+(x&31)*3)&255;c=((q*91)+(y&31)*5)&255
    else:z=(x*1103515245+y*12345+((x*y)*2654435761))&0xffffffff;a=(z>>8)&255;b=(z>>16)&255;c=(z>>24)&255
    row[i:i+3]=bytes((a,b,c))
   f.write(row)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();root=TMP/'tree';run(['git','worktree','add','--detach',str(root),BASE]);p=root/'src/lossless/decoder/mod.rs';s=p.read_text();marker='        let mut hufftree_groups = Vec::new();\n\n        for _i in 0..num_huff_groups {\n'
 if marker not in s:raise SystemExit('marker')
 p.write_text(s.replace(marker,'        if read_meta { eprintln!("VP8L_META bits={} groups={} grid={}x{}", huffman_bits, num_huff_groups, huffman_xsize, huffman_ysize); }\n\n'+marker,1));run(['cargo','fmt'],cwd=root)
 (root/'examples').mkdir(exist_ok=True);(root/'examples/meta_probe.rs').write_text('''use image_webp::WebPDecoder;use std::io::Cursor;fn main(){for p in std::env::args().skip(1){eprintln!("FILE {}",p);let d=std::fs::read(&p).unwrap();let mut x=WebPDecoder::new(Cursor::new(d)).unwrap();let mut b=vec![0;x.output_buffer_size().unwrap()];x.read_image(&mut b).unwrap();}}''');run(['cargo','build','--release','--example','meta_probe','-q'],cwd=root)
 files=[]
 for q in sorted((root/'tests/images').rglob('*.webp')):
  c=chunks(q.read_bytes())
  if b'VP8L'in c and b'ANIM'not in c:files.append(q)
 for kind in('structured','tiles','noise'):
  ppm=TMP/(kind+'.ppm');webp=TMP/(kind+'.webp');make(ppm,2048,1536,kind);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);files.append(webp)
 q=run([str(root/'target/release/examples/meta_probe'),*[str(x)for x in files]],cap=True);parts=re.split(r'FILE ',q.stderr)[1:];L=['# VP8L meta-Huffman coverage','',f'- baseline: `{BASE}`','','| file | bits | groups | grid |','|---|---:|---:|---:|'];metas=[]
 for part in parts:
  lines=part.splitlines();name=Path(lines[0]).name;m=re.search(r'VP8L_META bits=(\d+) groups=(\d+) grid=(\d+)x(\d+)',part)
  if not m:raise SystemExit('no meta record for '+name)
  bits,groups,gx,gy=map(int,m.groups());metas.append((bits,groups,gx,gy));L.append(f'| {name} | {bits} | {groups} | {gx}x{gy} |')
 L+=['',f'- multi-group streams: **{sum(g>1 for _,g,_,_ in metas)}/{len(metas)}**',f'- maximum groups observed: **{max(g for _,g,_,_ in metas)}**'];Path('analysis-vp8l-meta-groups.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
