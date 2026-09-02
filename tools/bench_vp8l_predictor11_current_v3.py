#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path

BASE = 'c52de05b9c902a6743941b998c96d5e4d3ba3609'
TMP = Path('/tmp/vp8l-p11-v3')
BENCH = r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
NEW = r'''pub fn apply_predictor_transform_11(image_data: &mut [u8], range: Range<usize>, width: usize) {
    let (old, current) = image_data[..range.end].split_at_mut(range.start);
    let top = &old[range.start - width * 4..];

    let mut l = [
        i16::from(old[range.start - 4]),
        i16::from(old[range.start - 3]),
        i16::from(old[range.start - 2]),
        i16::from(old[range.start - 1]),
    ];
    let mut tl = [
        i16::from(old[range.start - width * 4 - 4]),
        i16::from(old[range.start - width * 4 - 3]),
        i16::from(old[range.start - width * 4 - 2]),
        i16::from(old[range.start - width * 4 - 1]),
    ];

    for (chunk, top) in current.chunks_exact_mut(4).zip(top.chunks_exact(4)) {
        let t = [
            i16::from(top[0]),
            i16::from(top[1]),
            i16::from(top[2]),
            i16::from(top[3]),
        ];

        let mut predict_left = 0;
        let mut predict_top = 0;
        for i in 0..4 {
            predict_left += i16::abs(t[i] - tl[i]);
            predict_top += i16::abs(l[i] - tl[i]);
        }

        if predict_left < predict_top {
            chunk[0] = chunk[0].wrapping_add(l[0] as u8);
            chunk[1] = chunk[1].wrapping_add(l[1] as u8);
            chunk[2] = chunk[2].wrapping_add(l[2] as u8);
            chunk[3] = chunk[3].wrapping_add(l[3] as u8);
        } else {
            chunk[0] = chunk[0].wrapping_add(t[0] as u8);
            chunk[1] = chunk[1].wrapping_add(t[1] as u8);
            chunk[2] = chunk[2].wrapping_add(t[2] as u8);
            chunk[3] = chunk[3].wrapping_add(t[3] as u8);
        }

        tl = t;
        l = [i16::from(chunk[0]), i16::from(chunk[1]), i16::from(chunk[2]), i16::from(chunk[3])];
    }
}
'''

def run(cmd, cwd=None, cap=False, env=None):
    print('+', ' '.join(map(str, cmd)), flush=True)
    if cap:
        return subprocess.check_output(cmd, cwd=cwd, text=True, env=env).strip()
    subprocess.run(cmd, cwd=cwd, check=True, env=env)

def chunks(p):
    d=p.read_bytes(); out=[]; q=12
    if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP': return out
    while q+8<=len(d):
        t=d[q:q+4]; n=int.from_bytes(d[q+4:q+8],'little'); out.append(t); q+=8+n+(n&1)
    return out

def invoke(exe, mode, n, files):
    return run(['taskset','-c','0',str(exe),mode,str(n),*map(str,files)], cap=True)

def main():
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir(); roots={}; exes={}; env=os.environ.copy(); env['RUSTFLAGS']='-C target-cpu=native'
    for v in ('base','cand'):
        r=TMP/v; roots[v]=r; run(['git','worktree','add','--detach',str(r),BASE])
        if v=='cand':
            p=r/'src/lossless/decoder/reverse_transform.rs'; s=p.read_text(); a=s.index('pub fn apply_predictor_transform_11('); b=s.index('pub fn apply_predictor_transform_12(',a); p.write_text(s[:a]+NEW+s[b:]); run(['cargo','fmt'],cwd=r)
            for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']): run(c,cwd=r)
        (r/'examples').mkdir(exist_ok=True); (r/'examples/p11v3.rs').write_text(BENCH); run(['cargo','build','--release','--example','p11v3','-q'],cwd=r,env=env); exes[v]=r/'target/release/examples/p11v3'
    rels=[p.relative_to(roots['base']) for p in sorted((roots['base']/'tests/images').rglob('*.webp')) if b'VP8L' in chunks(p) and b'ANIM' not in chunks(p)]
    ppm=TMP/'large.ppm'; w=h=2048
    with ppm.open('wb') as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode()); row=bytearray(w*3)
        for y in range(h):
            for x in range(w):
                i=x*3; row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255; row[i+1]=(x*2+y*7+((x*y)>>10))&255; row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
            f.write(row)
    large=TMP/'large.webp'; run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(large)])
    corpus={v:[roots[v]/x for x in rels] for v in ('base','cand')}; assert invoke(exes['base'],'h',1,corpus['base']+[large])==invoke(exes['cand'],'h',1,corpus['cand']+[large])
    results={}
    for name,files,it in [('corpus',corpus,70),('large',{'base':[large],'cand':[large]},4)]:
        q=[]
        for n in range(25):
            order=('base','cand') if n%2==0 else ('cand','base'); z={}
            for v in order: z[v]=float(invoke(exes[v],'t',it,files[v]))
            q.append(z['base']/z['cand'])
        results[name]=q
    cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
    out=['# VP8L predictor-11 current-tree confirmation','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed','- algebra simplification only','','| workload | paired median | positive | range |','|---|---:|---:|---:|']
    for name,q in results.items(): out.append(f'| {name} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
    Path('benchmark-vp8l-predictor11-current-v3.md').write_text('\n'.join(out)+'\n'); print('\n'.join(out))

if __name__=='__main__': main()
