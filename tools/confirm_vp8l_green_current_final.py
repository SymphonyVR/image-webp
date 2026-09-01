#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path

BASE='6f8f7d994e2f747d46621812e01c27a29ff4be4a'
TMP=Path('/tmp/vp8l-green-current-final')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
GREEN=r'''pub(crate) fn apply_subtract_green_transform(image_data: &mut [u8]) {
    for pixel in image_data.chunks_exact_mut(4) {
        let value = u32::from_le_bytes(pixel.try_into().unwrap());
        let green = (value >> 8) & 0xff;
        let red_blue = ((value & 0x00ff_00ff).wrapping_add(green | (green << 16))) & 0x00ff_00ff;
        pixel.copy_from_slice(&((value & 0xff00_ff00) | red_blue).to_le_bytes());
    }
}
'''

def run(cmd,cwd=None,cap=False,env=None):
    print('+',' '.join(map(str,cmd)),flush=True)
    if cap:return subprocess.check_output(cmd,cwd=cwd,text=True,env=env).strip()
    subprocess.run(cmd,cwd=cwd,check=True,env=env)

def chunks(p):
    d=p.read_bytes();o=[];q=12
    if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP':return o
    while q+8<=len(d):
        t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
    return o

def invoke(exe,mode,n,files):
    return run(['taskset','-c','0',str(exe),mode,str(n),*map(str,files)],cap=True)

def fixture(path,kind):
    w=h=2048
    with path.open('wb') as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
        for y in range(h):
            for x in range(w):
                i=x*3
                if kind=='green':
                    g=(x*3+y*5+((x>>4)^(y>>4))*7)&255;row[i:i+3]=bytes((g,g,g))
                else:
                    row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255
                    row[i+1]=(x*2+y*7+((x*y)>>10))&255
                    row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
            f.write(row)

def main():
    if TMP.exists():shutil.rmtree(TMP)
    TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
    for v in ('base','cand'):
        r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
        if v=='cand':
            p=r/'src/lossless/decoder/reverse_transform.rs';s=p.read_text();a=s.index('pub(crate) fn apply_subtract_green_transform(');b=s.index('\npub(crate) fn apply_color_indexing_transform(',a);p.write_text(s[:a]+GREEN+s[b:]);run(['cargo','fmt'],cwd=r)
            for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
        (r/'examples').mkdir(exist_ok=True);(r/'examples/greenc.rs').write_text(BENCH);run(['cargo','build','--release','--example','greenc','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/greenc'
    rels=[p.relative_to(roots['base']) for p in sorted((roots['base']/'tests/images').rglob('*.webp')) if b'VP8L' in chunks(p) and b'ANIM' not in chunks(p)]
    for kind in ('green','large'):
        ppm=TMP/f'{kind}.ppm';fixture(ppm,kind);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(TMP/f'{kind}.webp')])
    corpus={v:[roots[v]/x for x in rels] for v in ('base','cand')};extras=[TMP/'green.webp',TMP/'large.webp'];assert invoke(exes['base'],'h',1,corpus['base']+extras)==invoke(exes['cand'],'h',1,corpus['cand']+extras)
    workloads={'corpus':(corpus,80),'green':({'base':[TMP/'green.webp'],'cand':[TMP/'green.webp']},4),'large':({'base':[TMP/'large.webp'],'cand':[TMP/'large.webp']},4)};results={}
    for name,(files,it) in workloads.items():
        q=[]
        for n in range(25):
            order=('base','cand') if n%2==0 else ('cand','base');z={}
            for v in order:z[v]=float(invoke(exes[v],'t',it,files[v]))
            q.append(z['base']/z['cand'])
        results[name]=q
    cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L packed subtract-green current-final confirmation','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed','- 25 alternating paired rounds','','| workload | paired median | positive | range |','|---|---:|---:|---:|']
    for name,q in results.items():L.append(f'| {name} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
    Path('benchmark-vp8l-green-current-final.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
