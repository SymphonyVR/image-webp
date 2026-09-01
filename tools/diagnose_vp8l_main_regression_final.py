#!/usr/bin/env python3
import math, os, shutil, statistics, subprocess
from pathlib import Path

MILESTONES = [
    ('main', 'f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f'),
    ('root9', 'fc8b701a3cba33887e47768c7b1e5e6a44de239d'),
    ('predictor1', '00c9bf309f8286509832948a67d4fbcdb2933adc'),
    ('cache_tail', 'a062200e32527c73b4a4e5a3de0f087f61b64337'),
    ('single_group', '509d11c2bf102929ded4be05d3c54b06032fdc44'),
    ('final', '4cd194935d100a09acf24eb24d8c1343c7844844'),
]
TMP = Path('/tmp/vp8l-main-regression-final')

BENCH = r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};
fn one(d:&[u8])->u64{let mut q=WebPDecoder::new(Cursor::new(d)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();let mut h=0xcbf29ce484222325u64;for &z in &b{h=(h^z as u64).wrapping_mul(1099511628211)}black_box(h)}
fn main(){let a:Vec<_>=std::env::args().skip(1).collect();let mode=&a[0];let n:usize=a[1].parse().unwrap();let ds:Vec<Vec<u8>>=a[2..].iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if mode=="h"{for d in&ds{println!("{:016x}",one(d))}return}for d in&ds{black_box(one(d));}let t=Instant::now();for _ in 0..n{for d in&ds{black_box(one(d));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''

def run(cmd, cwd=None, cap=False, env=None):
    print('+', ' '.join(map(str, cmd)), flush=True)
    if cap:
        return subprocess.check_output(cmd, cwd=cwd, text=True, env=env).strip()
    subprocess.run(cmd, cwd=cwd, check=True, env=env)

def chunks(p):
    d=p.read_bytes(); out=[]
    if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP': return out
    q=12
    while q+8<=len(d):
        t=d[q:q+4]; n=int.from_bytes(d[q+4:q+8],'little'); out.append(t); q += 8+n+(n&1)
    return out

def ppm(path,w,h,k):
    with path.open('wb') as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode())
        for y in range(h):
            row=bytearray()
            for x in range(w):
                if k=='gradient':
                    r=x*255//max(1,w-1); g=y*255//max(1,h-1); b=(x+y)*255//max(1,w+h-2)
                elif k=='corr':
                    g=(x*7+y*11+((x*y)>>7))&255; r=(g+((x>>3)&15))&255; b=(g-((y>>3)&15))&255
                elif k=='color':
                    r=(x*11+y*3)&255; g=(x*5+y*13)&255; b=(r+g*3)&255
                elif k=='structured':
                    q=((x>>5)+3*(y>>5))&15; r=q*17; g=(q*53+(x&31)*3)&255; b=(q*91+(y&31)*5)&255
                else:
                    z=(x*1103515245+y*12345+(x*y)*2654435761+0x9e3779b9)&0xffffffff; r=(z>>8)&255; g=(z>>16)&255; b=(z>>24)&255
                row += bytes((r,g,b))
            f.write(row)

def paired(exes, files, iters, rounds=13):
    samples={name:[] for name,_ in MILESTONES}
    order_names=[n for n,_ in MILESTONES]
    for r in range(rounds):
        order = order_names if r%2==0 else list(reversed(order_names))
        for name in order:
            v=float(run(['taskset','-c','0',str(exes[name]),'t',str(iters),*[str(x) for x in files]],cap=True))
            samples[name].append(v)
    med={k:statistics.median(v) for k,v in samples.items()}
    return med, samples

def main():
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir()
    roots={}; exes={}
    env=os.environ.copy(); env['RUSTFLAGS']='-C target-cpu=native'
    for name,sha in MILESTONES:
        root=TMP/name; roots[name]=root
        run(['git','worktree','add','--detach',str(root),sha])
        (root/'examples').mkdir(exist_ok=True)
        (root/'examples/milestone_decode.rs').write_text(BENCH)
        run(['cargo','build','--release','--example','milestone_decode','-q'],cwd=root,env=env)
        exes[name]=root/'target/release/examples/milestone_decode'

    generated={}
    for kind in ('structured','gradient','corr','color','noise'):
        src=TMP/f'{kind}.ppm'; ppm(src,2048,2048,kind)
        for z in (0,9):
            out=TMP/f'{kind}-z{z}.webp'
            run(['cwebp','-quiet','-lossless','-z',str(z),str(src),'-o',str(out)])
            generated[f'{kind}-z{z}']=out

    repo_main=[]
    for p in sorted((roots['main']/'tests/images').rglob('*.webp')):
        t=chunks(p)
        if b'VP8L' in t and b'ANIM' not in t: repo_main.append(p)
    repo_files={name:[roots[name]/p.relative_to(roots['main']) for p in repo_main] for name,_ in MILESTONES}

    # All milestone outputs must match the independently validated final on generated streams and issue119.
    final_hash={}
    for label,p in generated.items(): final_hash[label]=run([str(exes['final']),'h','1',str(p)],cap=True)
    hash_notes=[]
    for name,_ in MILESTONES:
        for label,p in generated.items():
            ok=run([str(exes[name]),'h','1',str(p)],cap=True)==final_hash[label]
            if not ok: hash_notes.append(f'{name}:{label}')

    run(['curl','-L','--fail','--retry','3','-o',str(TMP/'sample.zip'),'https://github.com/user-attachments/files/17482915/sample.zip'])
    (TMP/'issue').mkdir(); run(['unzip','-q',str(TMP/'sample.zip'),'-d',str(TMP/'issue')])
    issue=next((TMP/'issue').rglob('*.webp'))
    final_issue_hash=run([str(exes['final']),'h','1',str(issue)],cap=True)
    for name,_ in MILESTONES:
        if run([str(exes[name]),'h','1',str(issue)],cap=True)!=final_issue_hash: hash_notes.append(f'{name}:issue119')

    workloads=[]
    # Individual generated images; calibrate from main to ~100ms/sample.
    for label,p in generated.items():
        probe=float(run([str(exes['main']),'t','1',str(p)],cap=True)); it=max(1,min(25,math.ceil(100000/max(probe,1))))
        med,samples=paired(exes,[p],it,17)
        workloads.append((label,med,samples))
    # Repo corpus uses per-milestone copies but same content.
    # paired helper expects same file list; benchmark separately here to preserve each checkout.
    samples={name:[] for name,_ in MILESTONES}; order_names=[n for n,_ in MILESTONES]
    probe=float(run([str(exes['main']),'t','1',*[str(x) for x in repo_files['main']]],cap=True)); it=max(1,min(100,math.ceil(150000/max(probe,1))))
    for r in range(17):
        order=order_names if r%2==0 else list(reversed(order_names))
        for name in order:
            samples[name].append(float(run(['taskset','-c','0',str(exes[name]),'t',str(it),*[str(x) for x in repo_files[name]]],cap=True)))
    workloads.append(('repo-vp8l-corpus',{k:statistics.median(v) for k,v in samples.items()},samples))
    probe=float(run([str(exes['main']),'t','1',str(issue)],cap=True)); it=max(1,min(20,math.ceil(150000/max(probe,1))))
    med,samples=paired(exes,[issue],it,17); workloads.append(('issue119',med,samples))

    cpu=run(['bash','-lc',"lscpu | sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
    L=['# VP8L historical regression diagnosis','',f'- CPU: `{cpu}`','- release, `-C target-cpu=native`, CPU 0 pinned','- 17 alternating/reversed milestone rounds per workload','', '## Milestones','']
    for n,s in MILESTONES:L.append(f'- `{n}`: `{s}`')
    L += ['',f'- generated/issue output mismatches vs validated final: **{len(hash_notes)}**']
    if hash_notes:L += ['']+[f'- `{x}`' for x in hash_notes]
    L += ['','## Runtime medians','','| workload | main | root9 | predictor1 | cache_tail | single_group | final | final/main |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for label,med,samples in workloads:
        L.append(f"| {label} | {med['main']:.3f} | {med['root9']:.3f} | {med['predictor1']:.3f} | {med['cache_tail']:.3f} | {med['single_group']:.3f} | {med['final']:.3f} | {med['main']/med['final']:.4f}x |")
    L += ['','## Step ratios (previous/current; >1 faster)','','| workload | main→root9 | root9→predictor1 | predictor1→cache-tail | cache-tail→single-group | single-group→final |','|---|---:|---:|---:|---:|---:|']
    for label,med,_ in workloads:
        vals=[med['main']/med['root9'],med['root9']/med['predictor1'],med['predictor1']/med['cache_tail'],med['cache_tail']/med['single_group'],med['single_group']/med['final']]
        L.append('| '+label+' | '+' | '.join(f'{x:.4f}x' for x in vals)+' |')
    Path('diagnosis-vp8l-main-regression-final.md').write_text('\n'.join(L)+'\n'); print('\n'.join(L))

if __name__=='__main__': main()
