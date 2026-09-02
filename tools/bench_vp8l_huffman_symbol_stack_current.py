#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path

BASE='4f322d44fb38747659451db3d7f1dac7ff8ff21f'
TMP=Path('/tmp/vp8l-huffman-symbol-stack')
VS=('base','s256','s512')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''

def run(cmd,cwd=None,cap=False,env=None):
    print('+',' '.join(map(str,cmd)),flush=True)
    if cap:return subprocess.check_output(cmd,cwd=cwd,text=True,env=env).strip()
    subprocess.run(cmd,cwd=cwd,check=True,env=env)

def chunks(path):
    d=path.read_bytes();o=[];p=12
    if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return o
    while p+8<=len(d):
        tag=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');o.append(tag);p+=8+n+(n&1)
    return o

def patch(root,n):
    path=root/'src/lossless/decoder/huffman.rs';s=path.read_text()
    old='        let mut sorted_symbols = vec![0u16; code_lengths.len()];\n'
    new=f'''        let mut sorted_symbols_stack = [0u16; {n}];\n        let mut sorted_symbols_heap = Vec::new();\n        let sorted_symbols: &mut [u16] = if code_lengths.len() <= {n} {{\n            &mut sorted_symbols_stack[..code_lengths.len()]\n        }} else {{\n            sorted_symbols_heap.resize(code_lengths.len(), 0);\n            &mut sorted_symbols_heap\n        }};\n'''
    assert old in s
    path.write_text(s.replace(old,new,1))

def invoke(exe,mode,n,paths):
    return run(['taskset','-c','0',str(exe),mode,str(n),*map(str,paths)],cap=True)

def main():
    if TMP.exists():shutil.rmtree(TMP)
    TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
    for v in VS:
        root=TMP/v;roots[v]=root;run(['git','worktree','add','--detach',str(root),BASE])
        if v!='base':
            patch(root,int(v[1:]));run(['cargo','fmt'],cwd=root)
            for cmd in (
                ['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],
                ['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],
                ['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(cmd,cwd=root)
        (root/'examples').mkdir(exist_ok=True);(root/'examples/symstack.rs').write_text(BENCH)
        run(['cargo','build','--release','--example','symstack','-q'],cwd=root,env=env);exes[v]=root/'target/release/examples/symstack'
    rels=[p.relative_to(roots['base']) for p in sorted((roots['base']/'tests/images').rglob('*.webp')) if b'VP8L' in chunks(p) and b'ANIM' not in chunks(p)]
    ppm=TMP/'large.ppm';w=h=2048
    with ppm.open('wb') as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
        for y in range(h):
            for x in range(w):
                i=x*3;row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
            f.write(row)
    large=TMP/'large.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(large)])
    corpus={v:[roots[v]/r for r in rels] for v in VS}
    bh=invoke(exes['base'],'h',1,corpus['base']+[large])
    for v in VS[1:]:assert bh==invoke(exes[v],'h',1,corpus[v]+[large])
    results={}
    for name,files,iters in [('corpus',corpus,70),('large',{v:[large] for v in VS},4)]:
        rows=[]
        for n in range(13):
            order=VS if n%2==0 else tuple(reversed(VS));z={}
            for v in order:z[v]=float(invoke(exes[v],'t',iters,files[v]))
            rows.append(z)
        results[name]=rows
    cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
    lines=['# VP8L Huffman symbol-stack current-tree matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- fixed stack scratch for common Huffman alphabets; hashes + full verification passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
    for name,rows in results.items():
        for v in VS[1:]:
            q=[z['base']/z[v] for z in rows]
            lines.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
    Path('benchmark-vp8l-huffman-symbol-stack-current.md').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))

if __name__=='__main__':main()
