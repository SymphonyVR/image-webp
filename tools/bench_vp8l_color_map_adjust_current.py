#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='4f322d44fb38747659451db3d7f1dac7ff8ff21f';TMP=Path('/tmp/vp8l-color-map-adjust-current')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
NEW=r'''    fn adjust_color_map(color_map: &mut [u8]) {
        if color_map.len() < 8 { return; }
        let mut previous = u32::from_le_bytes(color_map[..4].try_into().unwrap());
        for pixel in color_map[4..].chunks_exact_mut(4) {
            let current = u32::from_le_bytes(pixel.try_into().unwrap());
            let lo = (current & 0x00ff_00ff).wrapping_add(previous & 0x00ff_00ff) & 0x00ff_00ff;
            let hi = (current & 0xff00_ff00).wrapping_add(previous & 0xff00_ff00) & 0xff00_ff00;
            previous = lo | hi;
            pixel.copy_from_slice(&previous.to_le_bytes());
        }
    }
'''
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(p):
 d=p.read_bytes();o=[];q=12
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return o
 while q+8<=len(d):t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
 return o
def inv(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for v in ('base','cand'):
  r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
  if v=='cand':
   p=r/'src/lossless/decoder/mod.rs';s=p.read_text();a=s.index('    fn adjust_color_map(');b=s.index('    /// Reads huffman codes associated with an image',a);p.write_text(s[:a]+NEW+'\n'+s[b:]);run(['cargo','fmt'],cwd=r)
   for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
  (r/'examples').mkdir(exist_ok=True);(r/'examples/cmap.rs').write_text(BENCH);run(['cargo','build','--release','--example','cmap','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/cmap'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)];corpus={v:[roots[v]/x for x in rels]for v in ('base','cand')}
 w=h=2048;ppm=TMP/'palette256.ppm';colors=[(i,(i*37)&255,(i*91)&255)for i in range(256)]
 with ppm.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):c=colors[((x>>3)+17*(y>>3))&255];i=x*3;row[i:i+3]=bytes(c)
   f.write(row)
 pal=TMP/'palette256.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(pal)]);assert inv(exes['base'],'h',1,corpus['base']+[pal])==inv(exes['cand'],'h',1,corpus['cand']+[pal])
 results={}
 for name,files,it in [('corpus',corpus,70),('palette256',{'base':[pal],'cand':[pal]},5)]:
  q=[]
  for n in range(17):
   order=('base','cand')if n%2==0 else('cand','base');z={}
   for v in order:z[v]=float(inv(exes[v],'t',it,files[v]))
   q.append(z['base']/z['cand'])
  results[name]=q
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L color-map adjustment current-tree benchmark','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- safe packed four-lane cumulative palette reconstruction; hashes + full verification passed','','| workload | paired median | positive | range |','|---|---:|---:|---:|']
 for name,q in results.items():L.append(f'| {name} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-color-map-adjust-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
