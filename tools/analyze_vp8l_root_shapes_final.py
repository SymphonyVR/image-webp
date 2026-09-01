#!/usr/bin/env python3
import os, shutil, subprocess, statistics
from pathlib import Path

BASE = '4cd194935d100a09acf24eb24d8c1343c7844844'
TMP = Path('/tmp/vp8l-root-shapes-final')

def run(cmd, cwd=None, cap=False, env=None, stderr=None):
    print('+', ' '.join(map(str, cmd)), flush=True)
    if cap:
        return subprocess.check_output(cmd, cwd=cwd, text=True, env=env, stderr=stderr).strip()
    return subprocess.run(cmd, cwd=cwd, check=True, env=env, stderr=stderr)

def ppm(path, w, h, kind):
    with path.open('wb') as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode())
        for y in range(h):
            row = bytearray()
            for x in range(w):
                if kind == 'structured':
                    q=((x>>5)+3*(y>>5))&15; r=q*17; g=(q*53+(x&31)*3)&255; b=(q*91+(y&31)*5)&255
                elif kind == 'gradient':
                    r=x*255//max(1,w-1); g=y*255//max(1,h-1); b=(x+y)*255//max(1,w+h-2)
                elif kind == 'corr':
                    g=(x*7+y*11+((x*y)>>7))&255; r=(g+((x>>3)&15))&255; b=(g-((y>>3)&15))&255
                elif kind == 'color':
                    r=(x*11+y*3)&255; g=(x*5+y*13)&255; b=(r+g*3)&255
                else:
                    z=(x*1103515245+y*12345+(x*y)*2654435761+0x9e3779b9)&0xffffffff; r=(z>>8)&255; g=(z>>16)&255; b=(z>>24)&255
                row += bytes((r,g,b))
            f.write(row)

BENCH = r'''use image_webp::WebPDecoder;use std::{io::Cursor,hint::black_box};fn main(){for p in std::env::args().skip(1){let d=std::fs::read(p).unwrap();let mut q=WebPDecoder::new(Cursor::new(d)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();black_box(b);}}'''

def parse(stderr_text):
    out=[]
    for line in stderr_text.splitlines():
        if not line.startswith('HUFF '): continue
        xs=list(map(int,line.split()[1:]))
        # symbols,maxlen,h9,h10,h11,h12,h13,h14,h15
        out.append(xs)
    return out

def summarize(label, rows):
    if not rows: return [f'| {label} | 0 | - | - | - | - | - | - |']
    ns=[r[0] for r in rows]; mx=[r[1] for r in rows]; longs=[sum(r[3:]) for r in rows]
    frac=[100*l/max(1,n) for l,n in zip(longs,ns)]
    def count(pred): return sum(1 for r in rows if pred(r))
    return [f'| {label} | {len(rows)} | {statistics.median(ns):.1f} | {max(mx)} | {statistics.median(frac):.2f}% | {count(lambda r:r[1]>=10)} | {count(lambda r:r[1]>=11)} | {count(lambda r:sum(r[3:])*8>=r[0])} |']

def main():
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir()
    root=TMP/'repo'; run(['git','worktree','add','--detach',str(root),BASE])
    p=root/'src/lossless/decoder/huffman.rs'; s=p.read_text()
    needle='        let table_bits = (max_length as u16).min(u16::from(MAX_TABLE_BITS));\n'
    repl='        eprintln!("HUFF {} {} {} {} {} {} {} {} {}", num_symbols, max_length, histogram[9], histogram[10], histogram[11], histogram[12], histogram[13], histogram[14], histogram[15]);\n'+needle
    if needle not in s: raise SystemExit('patch anchor missing')
    p.write_text(s.replace(needle,repl,1))
    (root/'examples').mkdir(exist_ok=True); (root/'examples/root_shapes.rs').write_text(BENCH)
    env=os.environ.copy(); env['RUSTFLAGS']='-C target-cpu=native'
    run(['cargo','build','--release','--example','root_shapes','-q'],cwd=root,env=env)
    exe=root/'target/release/examples/root_shapes'

    files={}
    for kind in ('structured','gradient','corr','color','noise'):
        src=TMP/f'{kind}.ppm'; ppm(src,1024,1024,kind)
        for z in (0,9):
            out=TMP/f'{kind}-z{z}.webp'; run(['cwebp','-quiet','-lossless','-z',str(z),str(src),'-o',str(out)])
            files[f'{kind}-z{z}']=[out]
    repo_files=[]
    for q in sorted((root/'tests/images').rglob('*.webp')):
        d=q.read_bytes()
        if b'VP8L' in d and b'ANIM' not in d: repo_files.append(q)
    files['repo-vp8l-corpus']=repo_files
    run(['curl','-L','--fail','--retry','3','-o',str(TMP/'sample.zip'),'https://github.com/user-attachments/files/17482915/sample.zip'])
    (TMP/'issue').mkdir(); run(['unzip','-q',str(TMP/'sample.zip'),'-d',str(TMP/'issue')]); issue=next((TMP/'issue').rglob('*.webp'))
    files['issue119']=[issue]

    records={}
    for label,ps in files.items():
        cp=subprocess.run([str(exe),*[str(x) for x in ps]],cwd=root,text=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,check=True)
        records[label]=parse(cp.stderr)

    L=['# VP8L Huffman tree-shape analysis','',f'- candidate lineage: `{BASE}`','- each stream decoded once; Huffman build histograms instrumented','', '| workload | trees | median symbols | max code len | median >9-symbol share | max>=10 | max>=11 | >9 share >=12.5% |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for label in files: L += summarize(label,records[label])
    L += ['','## High-entropy candidate selectors','', '| workload | long>=1/16 | long>=1/8 | long>=1/4 | long>=1/2 | max>=12 | max>=13 |','|---|---:|---:|---:|---:|---:|---:|']
    for label,rows in records.items():
        def c(d): return sum(1 for r in rows if sum(r[3:])*d>=r[0])
        L.append(f'| {label} | {c(16)} | {c(8)} | {c(4)} | {c(2)} | {sum(r[1]>=12 for r in rows)} | {sum(r[1]>=13 for r in rows)} |')
    L += ['','## Size + long-code selectors','', '| workload | n>=64 & long>=1/8 | n>=128 & long>=1/8 | n>=192 & long>=1/8 | n>=256 & long>=1/8 | n>=128 & long>=1/4 | n>=192 & long>=1/4 |','|---|---:|---:|---:|---:|---:|---:|']
    for label,rows in records.items():
        def sel(n,d): return sum(1 for r in rows if r[0]>=n and sum(r[3:])*d>=r[0])
        L.append(f'| {label} | {sel(64,8)} | {sel(128,8)} | {sel(192,8)} | {sel(256,8)} | {sel(128,4)} | {sel(192,4)} |')
    L += ['','## Detailed trees for targeted high-entropy streams','']
    for label in ('noise-z9','noise-z0','corr-z9'):
        L += [f'### {label}','', '| symbols | max | h9 | h10 | h11 | h12 | h13 | h14 | h15 |','|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
        for r in sorted(records[label], reverse=True):
            if r[1]>=10: L.append('| '+' | '.join(map(str,r))+' |')
        L.append('')
    Path('analysis-vp8l-root-shapes-final.md').write_text('\n'.join(L)+'\n')
    print('\n'.join(L))
if __name__=='__main__': main()
