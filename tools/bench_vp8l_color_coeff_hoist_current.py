#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path

BASE='4f322d44fb38747659451db3d7f1dac7ff8ff21f'
TMP=Path('/tmp/vp8l-color-coeff-hoist')
VS=('base','coeff','green','both')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''

def run(cmd,cwd=None,cap=False,env=None):
    print('+',' '.join(map(str,cmd)),flush=True)
    if cap:return subprocess.check_output(cmd,cwd=cwd,text=True,env=env).strip()
    subprocess.run(cmd,cwd=cwd,check=True,env=env)

def chunks(path):
    d=path.read_bytes();out=[];p=12
    if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP':return out
    while p+8<=len(d):tag=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');out.append(tag);p+=8+n+(n&1)
    return out

def patch(root,v):
    p=root/'src/lossless/decoder/reverse_transform.rs';s=p.read_text()
    if v in ('coeff','both'):
        old='''fn inverse_color_pixel_packed(\n    pixel: &mut [u8],\n    red_to_blue: u8,\n    green_to_blue: u8,\n    green_to_red: u8,\n) {'''
        new='''fn inverse_color_pixel_packed(\n    pixel: &mut [u8],\n    red_to_blue: i8,\n    green_to_blue: i8,\n    green_to_red: i8,\n) {'''
        assert old in s;s=s.replace(old,new,1)
        s=s.replace('color_transform_delta(green_to_red as i8, green as i8)','color_transform_delta(green_to_red, green as i8)',1)
        s=s.replace('color_transform_delta(green_to_blue as i8, green as i8)','color_transform_delta(green_to_blue, green as i8)',1)
        s=s.replace('color_transform_delta(red_to_blue as i8, red as u8 as i8)','color_transform_delta(red_to_blue, red as u8 as i8)',1)
        s=s.replace('''            let red_to_blue = transform[0];\n            let green_to_blue = transform[1];\n            let green_to_red = transform[2];''','''            let red_to_blue = transform[0] as i8;\n            let green_to_blue = transform[1] as i8;\n            let green_to_red = transform[2] as i8;''',1)
    if v in ('green','both'):
        needle='''    let green = ((argb >> 8) & 0xff) as u8;\n    let mut red = argb & 0xff;'''
        repl='''    let green = ((argb >> 8) & 0xff) as u8;\n    let green_i8 = green as i8;\n    let mut red = argb & 0xff;'''
        assert needle in s;s=s.replace(needle,repl,1)
        if v=='green':
            s=s.replace('color_transform_delta(green_to_red as i8, green as i8)','color_transform_delta(green_to_red as i8, green_i8)',1)
            s=s.replace('color_transform_delta(green_to_blue as i8, green as i8)','color_transform_delta(green_to_blue as i8, green_i8)',1)
        else:
            s=s.replace('color_transform_delta(green_to_red, green as i8)','color_transform_delta(green_to_red, green_i8)',1)
            s=s.replace('color_transform_delta(green_to_blue, green as i8)','color_transform_delta(green_to_blue, green_i8)',1)
    p.write_text(s)

def invoke(exe,mode,n,paths):return run(['taskset','-c','0',str(exe),mode,str(n),*map(str,paths)],cap=True)

def main():
    if TMP.exists():shutil.rmtree(TMP)
    TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
    for v in VS:
        root=TMP/v;roots[v]=root;run(['git','worktree','add','--detach',str(root),BASE])
        if v!='base':
            patch(root,v);run(['cargo','fmt'],cwd=root)
            for cmd in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(cmd,cwd=root)
        (root/'examples').mkdir(exist_ok=True);(root/'examples/color_hoist.rs').write_text(BENCH);run(['cargo','build','--release','--example','color_hoist','-q'],cwd=root,env=env);exes[v]=root/'target/release/examples/color_hoist'
    rels=[p.relative_to(roots['base']) for p in sorted((roots['base']/'tests/images').rglob('*.webp')) if b'VP8L' in chunks(p) and b'ANIM' not in chunks(p)]
    corpus={v:[roots[v]/r for r in rels] for v in VS}
    hotrel=Path('tests/images/gallery2/3_webp_ll.webp');hot={v:[roots[v]/hotrel] for v in VS}
    base_hash=invoke(exes['base'],'h',1,corpus['base'])
    for v in VS[1:]:assert base_hash==invoke(exes[v],'h',1,corpus[v])
    results={}
    for name,files,iters in [('corpus',corpus,70),('colorhot',hot,45)]:
        rows=[]
        for n in range(17):
            order=VS if n%2==0 else tuple(reversed(VS));z={}
            for v in order:z[v]=float(invoke(exes[v],'t',iters,files[v]))
            rows.append(z)
        results[name]=rows
    cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
    lines=['# VP8L color coefficient-hoist current-tree matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- coeff converts transform coefficients to i8 once per block; green hoists green signed conversion once per pixel; hashes + full verification passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
    for name,rows in results.items():
        for v in VS[1:]:
            q=[z['base']/z[v] for z in rows]
            lines.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
    Path('benchmark-vp8l-color-coeff-hoist-current.md').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))

if __name__=='__main__':main()
