#!/usr/bin/env python3
import os,re,subprocess,shutil
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44';TMP=Path('/tmp/vp8l-meta-analysis')
def run(c,cwd=None,cap=False,err=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:
  p=subprocess.run(c,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,env=env);return p.stdout,p.stderr
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+n+(n&1)
 return o
def make_ppm(path,w,h,kind):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    i=x*3
    if kind=='structured':a=(x*5+y*3+((x>>4)^(y>>3))*29)&255;b=(x*13+y*7+((x*y)>>8))&255;c=(x*2+y*17+((x+y)>>2)*11)&255
    elif kind=='tiles':
     q=((x>>5)+3*(y>>5))&15;a=(q*17)&255;b=((q*53)+(x&31)*3)&255;c=((q*91)+(y&31)*5)&255
    else:
     z=(x*1103515245+y*12345+((x*y)*2654435761))&0xffffffff;a=(z>>8)&255;b=(z>>16)&255;c=(z>>24)&255
    row[i:i+3]=bytes((a,b,c))
   f.write(row)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();root=TMP/'tree';run(['git','worktree','add','--detach',str(root),BASE]);p=root/'src/lossless/decoder/mod.rs';s=p.read_text();marker='''        let mut hufftree_groups = Vec::new();\n\n        for _i in 0..num_huff_groups {\n''';new='''        if read_meta {\n            eprintln!("VP8L_META bits={} groups={} grid={}x{}", huffman_bits, num_huff_groups, huffman_xsize, huffman_ysize);\n        }\n\n        let mut hufftree_groups = Vec::new();\n\n        for _i in 0..num_huff_groups {\n'''
 if marker not in s:raise SystemExit('marker');p.write_text(s.replace(marker,new,1));run(['cargo','fmt'],cwd=root)
 ex=root/'examples';ex.mkdir(exist_ok=True);(ex/'meta_probe.rs').write_text('''use image_webp::WebPDecoder;use std::io::Cursor;fn main(){for p in std::env::args().skip(1){let d=std::fs::read(&p).unwrap();let mut x=WebPDecoder::new(Cursor::new(d)).unwrap();let mut b=vec![0;x.output_buffer_size().unwrap()];x.read_image(&mut b).unwrap();eprintln!("FILE {}",p);}}''');run(['cargo','build','--release','--example','meta_probe','-q'],cwd=root)
 files=[]
 for q in sorted((root/'tests/images').rglob('*.webp')):
  c=chunks(q.read_bytes())
  if b'VP8L'in c and b'ANIM'not in c:files.append(q)
 for kind in('structured','tiles','noise'):
  ppm=TMP/(kind+'.ppm');webp=TMP/(kind+'.webp');make_ppm(ppm,2048,1536,kind);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);files.append(webp)
 _,stderr=run([str(root/'target/release/examples/meta_probe'),*[str(x)for x in files]],cap=True)
 metas=[tuple(map(int,m.groups()))for m in re.finditer(r'VP8L_META bits=(\d+) groups=(\d+) grid=(\d+)x(\d+)',stderr)]
 if len(metas)!=len(files):raise SystemExit(f'expected {len(files)} meta records, got {len(metas)}')
 L=['# VP8L meta-Huffman coverage','',f'- baseline: `{BASE}`','','| file | bits | groups | grid |','|---|---:|---:|---:|']
 for path,(bits,groups,gx,gy) in zip(files,metas):L.append(f'| {path.name} | {bits} | {groups} | {gx}x{gy} |')
 multi=sum(g>1 for _,g,_,_ in metas);L+=['',f'- multi-group streams: **{multi}/{len(metas)}**',f'- maximum groups observed: **{max(g for _,g,_,_ in metas)}**']
 Path('analysis-vp8l-meta-groups.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
