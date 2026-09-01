#!/usr/bin/env python3
import re,shutil,subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44';TMP=Path('/tmp/vp8l-meta-runs')
def run(c,cwd=None,cap=False):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.run(c,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
 subprocess.run(c,cwd=cwd,check=True)
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return[]
 o=[];p=12
 while p+8<=len(d):f=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');o.append(f);p+=8+n+(n&1)
 return o
def make(path,w,h,kind):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    if kind=='structured':r=(x*3+y*5+((x>>5)^(y>>4))*17)&255;g=(x*2+y*7+((x*y)>>10))&255;b=(x*11+y*3+((x+y)>>3)*9)&255
    elif kind=='tiles':q=((x>>5)+3*(y>>5))&15;r=q*17;g=(q*53+(x&31)*3)&255;b=(q*91+(y&31)*5)&255
    else:z=(x*1103515245+y*12345+(x*y)*2654435761)&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
    i=x*3;row[i:i+3]=bytes((r,g,b))
   f.write(row)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();root=TMP/'tree';run(['git','worktree','add','--detach',str(root),BASE]);p=root/'src/lossless/decoder/mod.rs';s=p.read_text()
 marker='''        let mut hufftree_groups = Vec::new();\n\n        for _i in 0..num_huff_groups {\n'''
 add=r'''        if read_meta {
            let cells = entropy_image.len();
            let mut runs = 0usize;
            let mut same_right = 0usize;
            if huffman_xsize > 0 {
                let w = usize::from(huffman_xsize);
                for row in entropy_image.chunks_exact(w) {
                    if !row.is_empty() { runs += 1; }
                    for pair in row.windows(2) {
                        if pair[0] == pair[1] { same_right += 1; } else { runs += 1; }
                    }
                }
            }
            eprintln!("VP8L_META_RUNS bits={} groups={} grid={}x{} cells={} runs={} same_right={}", huffman_bits, num_huff_groups, huffman_xsize, huffman_ysize, cells, runs, same_right);
        }

'''
 if marker not in s:raise SystemExit('marker')
 p.write_text(s.replace(marker,add+marker,1));run(['cargo','fmt'],cwd=root)
 (root/'examples').mkdir(exist_ok=True);(root/'examples/meta_runs.rs').write_text('''use image_webp::WebPDecoder;use std::io::Cursor;fn main(){for p in std::env::args().skip(1){eprintln!("FILE {}",p);let d=std::fs::read(&p).unwrap();let mut x=WebPDecoder::new(Cursor::new(d)).unwrap();let mut b=vec![0;x.output_buffer_size().unwrap()];x.read_image(&mut b).unwrap();}}''');run(['cargo','build','--release','--example','meta_runs','-q'],cwd=root)
 files=[]
 for q in sorted((root/'tests/images').rglob('*.webp')):
  c=chunks(q.read_bytes())
  if b'VP8L'in c and b'ANIM'not in c:files.append(q)
 for k in('structured','tiles','noise'):
  ppm=TMP/(k+'.ppm');webp=TMP/(k+'.webp');make(ppm,2048,1536,k);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);files.append(webp)
 q=run([str(root/'target/release/examples/meta_runs'),*[str(x)for x in files]],cap=True);parts=re.split(r'FILE ',q.stderr)[1:]
 L=['# VP8L meta-Huffman horizontal-run analysis','',f'- baseline: `{BASE}`','','| file | bits | groups | grid | cells | runs | same-right | dispatch reduction |','|---|---:|---:|---:|---:|---:|---:|---:|']
 for part in parts:
  lines=part.splitlines();name=Path(lines[0]).name;m=re.search(r'VP8L_META_RUNS bits=(\d+) groups=(\d+) grid=(\d+)x(\d+) cells=(\d+) runs=(\d+) same_right=(\d+)',part)
  if not m:raise SystemExit('missing '+name)
  bits,groups,gx,gy,cells,runs,same=map(int,m.groups());red=(1-runs/cells)*100 if cells else 0;L.append(f'| {name} | {bits} | {groups} | {gx}x{gy} | {cells} | {runs} | {same} | {red:.1f}% |')
 Path('analysis-vp8l-meta-runs.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
