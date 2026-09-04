#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path
BASE='4f322d44fb38747659451db3d7f1dac7ff8ff21f'
TMP=Path('/tmp/vp8l-predictor234-zip-current')
VS=('base','p2','p3','p4','all')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
FUNCS={
2:r'''pub fn apply_predictor_transform_2(image_data: &mut [u8], range: Range<usize>, width: usize) {
    assert!(range.end <= image_data.len());
    let len = range.end - range.start;
    let source_start = range.start - width * 4;
    let (before, after) = image_data.split_at_mut(range.start);
    let source = &before[source_start..source_start + len];
    let current = &mut after[..len];
    for (dst, &src) in current.iter_mut().zip(source) {
        *dst = dst.wrapping_add(src);
    }
}
''',
3:r'''pub fn apply_predictor_transform_3(image_data: &mut [u8], range: Range<usize>, width: usize) {
    assert!(range.end <= image_data.len());
    let len = range.end - range.start;
    let source_start = range.start - width * 4 + 4;
    let (before, after) = image_data.split_at_mut(range.start);
    let source = &before[source_start..source_start + len];
    let current = &mut after[..len];
    for (dst, &src) in current.iter_mut().zip(source) {
        *dst = dst.wrapping_add(src);
    }
}
''',
4:r'''pub fn apply_predictor_transform_4(image_data: &mut [u8], range: Range<usize>, width: usize) {
    assert!(range.end <= image_data.len());
    let len = range.end - range.start;
    let source_start = range.start - width * 4 - 4;
    let (before, after) = image_data.split_at_mut(range.start);
    let source = &before[source_start..source_start + len];
    let current = &mut after[..len];
    for (dst, &src) in current.iter_mut().zip(source) {
        *dst = dst.wrapping_add(src);
    }
}
'''}
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(p):
 d=p.read_bytes();o=[];q=12
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return o
 while q+8<=len(d):t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
 return o
def patch(r,v):
 p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text();nums=[2,3,4] if v=='all' else [int(v[1:])]
 for n in nums:
  a=s.index(f'pub fn apply_predictor_transform_{n}(');b=s.index(f'pub fn apply_predictor_transform_{n+1}(',a);s=s[:a]+FUNCS[n]+s[b:]
 p.write_text(s)
def invoke(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)
def make_ppm(p,w,h):
 with p.open('wb') as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    i=x*3;row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
   f.write(row)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for v in VS:
  r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
  if v!='base':
   patch(r,v);run(['cargo','fmt'],cwd=r)
   for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
  (r/'examples').mkdir(exist_ok=True);(r/'examples/p234z.rs').write_text(BENCH);run(['cargo','build','--release','--example','p234z','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/p234z'
 rels=[p.relative_to(roots['base']) for p in sorted((roots['base']/'tests/images').rglob('*.webp')) if b'VP8L'in chunks(p) and b'ANIM'not in chunks(p)]
 ppm=TMP/'large.ppm';make_ppm(ppm,2048,2048);large=TMP/'large.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(large)])
 corpus={v:[roots[v]/r for r in rels] for v in VS};bh=invoke(exes['base'],'h',1,corpus['base']+[large])
 for v in VS[1:]:assert bh==invoke(exes[v],'h',1,corpus[v]+[large])
 results={}
 for name,files,it in [('corpus',corpus,70),('large',{v:[large] for v in VS},4)]:
  rows=[]
  for n in range(17):
   order=VS if n%2==0 else tuple(reversed(VS));z={}
   for v in order:z[v]=float(invoke(exes[v],'t',it,files[v]))
   rows.append(z)
  results[name]=rows
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L predictor 2/3/4 disjoint-zip current-tree matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- disjoint previous-row slices expose alias-free byte loops; hashes + full verification passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for name,rows in results.items():
  for v in VS[1:]:q=[z['base']/z[v] for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-predictor234-zip-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
