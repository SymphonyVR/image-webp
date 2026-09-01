#!/usr/bin/env python3
import math, os, shutil, statistics, subprocess
from pathlib import Path
MAIN='f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f'
FINAL='4cd194935d100a09acf24eb24d8c1343c7844844'
TMP=Path('/tmp/image-webp-scorecard-v2')
def run(c,cwd=None,cap=False,env=None):
    print('+',' '.join(map(str,c)),flush=True)
    if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
    subprocess.run(c,cwd=cwd,check=True,env=env)
def tags(p):
    d=p.read_bytes();out=[]
    if len(d)<12 or d[:4]!=b'RIFF':return out
    q=12
    while q+8<=len(d):
        t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');out.append(t);q+=8+n+(n&1)
    return out
BENCH=r'''use image_webp::{DecodingError,WebPDecoder};use std::{hint::black_box,io::Cursor,time::Instant};fn one(d:&[u8])->u64{let mut q=WebPDecoder::new(Cursor::new(d)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];let mut h=0xcbf29ce484222325u64;if q.is_animated(){loop{match q.read_frame(&mut b){Ok(ms)=>{h=(h^ms as u64).wrapping_mul(1099511628211);for &z in &b{h=(h^z as u64).wrapping_mul(1099511628211)}},Err(DecodingError::NoMoreFrames)=>break,Err(e)=>panic!("{e:?}")}}}else{q.read_image(&mut b).unwrap();for &z in &b{h=(h^z as u64).wrapping_mul(1099511628211)}}black_box(h)}fn main(){let a:Vec<_>=std::env::args().skip(1).collect();let mode=&a[0];let n:usize=a[1].parse().unwrap();let ds:Vec<Vec<u8>>=a[2..].iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if mode=="h"{for d in&ds{println!("{:016x}",one(d))}return}for d in&ds{black_box(one(d));}let t=Instant::now();for _ in 0..n{for d in&ds{black_box(one(d));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def paired(a,b,fa,fb,iters,rounds=25):
    rs=[];aa=[];bb=[]
    for i in range(rounds):
        vals={}
        order=('main','final') if i%2==0 else ('final','main')
        for name in order:
            exe=a if name=='main' else b;fs=fa if name=='main' else fb
            vals[name]=float(run(['taskset','-c','0',str(exe),'t',str(iters),*[str(x) for x in fs]],cap=True))
        aa.append(vals['main']);bb.append(vals['final']);rs.append(vals['main']/vals['final'])
    return statistics.median(aa),statistics.median(bb),statistics.median(rs),sum(x>1 for x in rs),min(rs),max(rs)
def ppm(path,w,h,k):
    with path.open('wb') as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode())
        for y in range(h):
            row=bytearray()
            for x in range(w):
                if k=='gradient':r=x*255//(w-1);g=y*255//(h-1);b=(x+y)*255//(w+h-2)
                elif k=='corr':g=(x*7+y*11+((x*y)>>7))&255;r=(g+((x>>3)&15))&255;b=(g-((y>>3)&15))&255
                elif k=='color':r=(x*11+y*3)&255;g=(x*5+y*13)&255;b=(r+g*3)&255
                else:z=(x*1103515245+y*12345+(x*y)*2654435761)&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
                row+=bytes((r,g,b))
            f.write(row)
def hash_lines(exe,fs):return run([str(exe),'h','1',*[str(x)for x in fs]],cap=True).splitlines()
def main():
    if TMP.exists():shutil.rmtree(TMP)
    TMP.mkdir();m=TMP/'main';f=TMP/'final';run(['git','worktree','add','--detach',str(m),MAIN]);run(['git','worktree','add','--detach',str(f),FINAL])
    for r in(m,f):
        (r/'examples').mkdir(exist_ok=True);(r/'examples/scorecard_decode.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','scorecard_decode','-q'],cwd=r,env=e)
    me=m/'target/release/examples/scorecard_decode';fe=f/'target/release/examples/scorecard_decode'
    rels=[p.relative_to(m) for p in sorted((m/'tests/images').rglob('*.webp'))];mr=[m/x for x in rels];fr=[f/x for x in rels]
    mh=hash_lines(me,mr);fh=hash_lines(fe,fr);mismatch_rels=[str(r) for r,a,b in zip(rels,mh,fh) if a!=b]
    cats={'vp8l-static':[],'vp8-static':[],'animated':[]}
    for rel,mp,fp in zip(rels,mr,fr):
        t=tags(mp)
        if b'ANIM'in t:cats['animated'].append((mp,fp))
        elif b'VP8L'in t:cats['vp8l-static'].append((mp,fp))
        elif b'VP8 'in t:cats['vp8-static'].append((mp,fp))
    generated=[]
    for k in ('gradient','corr','color','noise'):
        src=TMP/f'{k}.ppm';ppm(src,2048,2048,k);q=TMP/f'{k}-z9.webp';run(['cwebp','-quiet','-lossless','-z','9',str(src),'-o',str(q)]);generated.append(q)
    gen_hash_match=hash_lines(me,generated)==hash_lines(fe,generated)
    groups=[]
    for name,pairs in cats.items():
        if not pairs:continue
        ma=[x[0]for x in pairs];fa=[x[1]for x in pairs];probe=float(run([str(me),'t','1',*[str(x)for x in ma]],cap=True));it=max(1,min(100,math.ceil(250000/max(probe*len(ma),1))));groups.append((name,len(ma),*paired(me,fe,ma,fa,it)))
    probe=float(run([str(me),'t','1',*[str(x)for x in generated]],cap=True));it=max(1,min(10,math.ceil(300000/max(probe*len(generated),1))));groups.append(('generated-vp8l-z9',len(generated),*paired(me,fe,generated,generated,it)))
    run(['curl','-L','--fail','--retry','3','-o',str(TMP/'sample.zip'),'https://github.com/user-attachments/files/17482915/sample.zip']);run(['unzip','-q',str(TMP/'sample.zip'),'-d',str(TMP/'issue')]);issue=next((TMP/'issue').rglob('*.webp'))
    issue_hash_match=hash_lines(me,[issue])==hash_lines(fe,[issue]);probe=float(run([str(me),'t','1',str(issue)],cap=True));it=max(1,min(20,math.ceil(250000/max(probe,1))));groups.append(('issue119-large-vp8l',1,*paired(me,fe,[issue],[issue],it)))
    cpu=run(['bash','-lc',"lscpu | sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
    L=['# image-webp final performance scorecard','',f'- main: `{MAIN}`',f'- final candidate: `{FINAL}`',f'- CPU: `{cpu}`','- release builds, `-C target-cpu=native`, CPU 0 pinned','- 25 alternating paired rounds','',f'- repository files whose decoded hash differs between historical main and validated final: **{len(mismatch_rels)}/{len(rels)}**',f'- generated VP8L decoded hashes main==final: **{gen_hash_match}**',f'- issue119 decoded hash main==final: **{issue_hash_match}**','- final candidate correctness is independently established by the 458-stream libwebp byte-for-byte differential; historical-main hash differences are therefore reported rather than treated as a benchmark failure.','', '| workload | files | main us/file | final us/file | speedup | positive | range |','|---|---:|---:|---:|---:|---:|---:|']
    for x in groups:L.append(f'| {x[0]} | {x[1]} | {x[2]:.3f} | {x[3]:.3f} | **{x[4]:.4f}x** | {x[5]}/25 | {x[6]:.4f}–{x[7]:.4f}x |')
    if mismatch_rels:L+=['','## Historical-main output differences','']+[f'- `{x}`' for x in mismatch_rels]
    Path('scorecard-main-vs-composed-v3.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
