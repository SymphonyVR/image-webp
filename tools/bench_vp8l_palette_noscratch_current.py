#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path

BASE='0881ec1a66f09e11b766c309cf6e651077775bd9'
TMP=Path('/tmp/vp8l-palette-noscratch-current')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
NEW=r'''    for y_rev_idx in 0..height as usize {
        let y = height as usize - 1 - y_rev_idx;
        let packed_row_input_global_offset = y * input_stride_bytes_packed;
        let output_row_global_offset = y * output_stride_bytes_expanded;
        for block_index in (0..packed_image_width_in_blocks).rev() {
            let packed_index = image_data[packed_row_input_global_offset + block_index * 4 + 1];
            let output_offset = output_row_global_offset + block_index * EXP_ENTRY_SIZE;
            let is_final = block_index + 1 == packed_image_width_in_blocks;
            if is_final && final_block_expanded_size_bytes != EXP_ENTRY_SIZE {
                image_data[output_offset..output_offset + final_block_expanded_size_bytes]
                    .copy_from_slice(&expanded_lookup_table_array[packed_index as usize][..final_block_expanded_size_bytes]);
            } else {
                let dst: &mut [u8; EXP_ENTRY_SIZE] = image_data[output_offset..output_offset + EXP_ENTRY_SIZE]
                    .try_into().unwrap();
                *dst = expanded_lookup_table_array[packed_index as usize];
            }
        }
    }
'''
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(p):
 d=p.read_bytes();o=[];q=12
 if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP':return o
 while q+8<=len(d):t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
 return o
def inv(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for v in ('base','cand'):
  r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
  if v=='cand':
   p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text();a=s.index('    let mut packed_indices_for_row: Vec<u8> = vec![0; packed_image_width_in_blocks];');b=s.index('\n}\n\n//predictor functions',a);p.write_text(s[:a]+NEW+s[b:]);run(['cargo','fmt'],cwd=r)
   for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q']):run(c,cwd=r)
  (r/'examples').mkdir(exist_ok=True);(r/'examples/palc.rs').write_text(BENCH);run(['cargo','build','--release','--example','palc','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/palc'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
 w=h=2048;colors=[(10,20,30),(230,40,80),(20,220,60),(80,90,240),(240,210,20),(160,30,200),(30,200,210),(245,245,245)];ppm=TMP/'palette.ppm'
 with ppm.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):c=colors[((x>>5)+(y>>5)*3)&7];i=x*3;row[i:i+3]=bytes(c)
   f.write(row)
 pal=TMP/'palette.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(pal)])
 files={v:[roots[v]/x for x in rels]for v in ('base','cand')};assert inv(exes['base'],'h',1,files['base']+[pal])==inv(exes['cand'],'h',1,files['cand']+[pal])
 res={}
 for label,ps,it in [('corpus',files,60),('palette',{'base':[pal],'cand':[pal]},4)]:
  q=[]
  for n in range(17):
   order=('base','cand')if n%2==0 else('cand','base');z={}
   for v in order:z[v]=float(inv(exes[v],'t',it,ps[v]))
   q.append(z['base']/z['cand'])
  res[label]=q
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L scratchless palette current-final benchmark','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed','','| workload | paired median | positive | range |','|---|---:|---:|---:|']
 for label,q in res.items():L.append(f'| {label} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-palette-noscratch-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
