#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44';TMP=Path('/tmp/vp8l-tail-v3');VS=['hash','colormap','both']
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def rep(s,o,n,l):
 if o not in s:raise SystemExit('missing '+l)
 return s.replace(o,n,1)
def patch(n,r):
 p=r/'src/lossless/decoder/mod.rs';s=p.read_text()
 if n in('hash','both'):
  s=rep(s,'''        let [r, g, b, a] = color;\n        let color_u32 =\n            (u32::from(r) << 16) | (u32::from(g) << 8) | (u32::from(b)) | (u32::from(a) << 24);\n''','''        let [r, g, b, a] = color;\n        let color_u32 = u32::from_be_bytes([a, r, g, b]);\n''','hash')
 if n in('colormap','both'):
  s=rep(s,'''    fn adjust_color_map(color_map: &mut [u8]) {\n        for i in 4..color_map.len() {\n            color_map[i] = color_map[i].wrapping_add(color_map[i - 4]);\n        }\n    }\n''','''    fn adjust_color_map(color_map: &mut [u8]) {\n        if color_map.len() <= 4 { return; }\n        let mut previous: [u8; 4] = color_map[..4].try_into().unwrap();\n        for color in color_map[4..].chunks_exact_mut(4) {\n            previous = [color[0].wrapping_add(previous[0]), color[1].wrapping_add(previous[1]), color[2].wrapping_add(previous[2]), color[3].wrapping_add(previous[3])];\n            color.copy_from_slice(&previous);\n        }\n    }\n''','colormap')
 p.write_text(s)
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
 rel=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in ch(p.read_bytes())and b'ANIM'not in ch(p.read_bytes())];bins={}
 for n,r in roots.items():
  (r/'examples').mkdir(exist_ok=True);(r/'examples/tailv3.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','tailv3','-q'],cwd=r,env=e);bins[n]=r/'target/release/examples/tailv3'
 def inv(n,m,it):return run(['taskset','-c','0',str(bins[n]),m,str(it),*[str(roots[n]/x)for x in rel]],cap=True)
 bh=inv('base','h',1)
 for n in VS:
  if inv(n,'h',1)!=bh:raise SystemExit('hash mismatch '+n)
 rows=[]
 for rnd in range(1,16):
  order=['base',*VS]if rnd%2 else[*reversed(VS),'base']
  for n in order:rows.append((rnd,n,float(inv(n,'t',70))))
 rr={}
 for r,n,x in rows:rr.setdefault(r,{})[n]=x
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L final tail closure','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + MSRV passed','','| candidate | paired median | positive | range |','|---|---:|---:|---:|']
 for n in VS:q=[z['base']/z[n]for _,z in sorted(rr.items())];L.append(f'| {n} | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-tail-closure-v3.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
