#!/usr/bin/env python3
import math, os, shutil, statistics, subprocess
from pathlib import Path
BASE='4cd194935d100a09acf24eb24d8c1343c7844844'
CAND='7eeb7200cbee067f2ee66deb708e47be2037314f'
TMP=Path('/tmp/vp8l-pred-direct-composed')
def run(c,cwd=None,cap=False,env=None):
    print('+',' '.join(map(str,c)),flush=True)
    if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
    subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(d):
    if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP':return[]
    out=[];p=12
    while p+8<=len(d):tag=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');out.append(tag);p+=8+n+(n&1)
    return out
def ppm(path,w,h,k):
    with path.open('wb')as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
        for y in range(h):
            for x in range(w):
                if k=='gradient':r=x*255//max(1,w-1);g=y*255//max(1,h-1);b=(x+y)*255//max(1,w+h-2)
                elif k=='corr':g=(x*7+y*11+((x*y)>>7))&255;r=(g+((x>>3)&15))&255;b=(g-((y>>3)&15))&255
                elif k=='stripes':r=(x*13)&255;g=((x//4)*47+y)&255;b=((x//11)*91+y*3)&255
                elif k=='tiles':q=((x>>5)+3*(y>>5))&15;r=q*17;g=(q*53+(x&31)*3)&255;b=(q*91+(y&31)*5)&255
                elif k=='smooth':r=(x//4+y//8)&255;g=(x//6+y//5)&255;b=(x//9+y//3)&255
                else:z=(x*1103515245+y*12345+(x*y)*2654435761)&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
                i=x*3;row[i:i+3]=bytes((r,g,b))
            f.write(row)
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let a:Vec<_>=std::env::args().skip(1).collect();let mode=&a[0];let n:usize=a[1].parse().unwrap();let ps=&a[2..];let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if mode=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def paired(b,c,bf,cf,iters,rounds):
    ratios=[];bs=[];cs=[]
    for r in range(rounds):
        vals={};order=('base','cand') if r%2==0 else ('cand','base')
        for v in order:
            exe=b if v=='base' else c;fs=bf if v=='base' else cf
            vals[v]=float(run(['taskset','-c','0',str(exe),'t',str(iters),*[str(p) for p in fs]],cap=True))
        bs.append(vals['base']);cs.append(vals['cand']);ratios.append(vals['base']/vals['cand'])
    return statistics.median(bs),statistics.median(cs),statistics.median(ratios),sum(x>1 for x in ratios),min(ratios),max(ratios)
def main():
    if TMP.exists():shutil.rmtree(TMP)
    TMP.mkdir();base=TMP/'base';cand=TMP/'cand';run(['git','worktree','add','--detach',str(base),BASE]);run(['git','worktree','add','--detach',str(cand),CAND])
    run(['cargo','test','-q'],cwd=cand);run(['cargo','doc','--no-deps','-q'],cwd=cand);run(['cargo','clippy','--','-D','warnings'],cwd=cand);run(['cargo','fmt','--','--check'],cwd=cand);run(['cargo','+1.80.1','build','-q'],cwd=cand)
    repo=[]
    for p in sorted((base/'tests/images').rglob('*.webp')):
        c=chunks(p.read_bytes())
        if b'VP8L'in c and b'ANIM'not in c:repo.append(p)
    generated=[]
    for k in('gradient','corr','stripes','tiles','smooth','noise'):
        src=TMP/f'{k}.ppm';ppm(src,1536,1024,k)
        for z in(0,3,6,9):
            q=TMP/f'{k}-z{z}.webp';run(['cwebp','-quiet','-lossless','-z',str(z),str(src),'-o',str(q)]);generated.append((f'{k}-z{z}',q))
    for r in(base,cand):
        (r/'examples').mkdir(exist_ok=True);(r/'examples/pred_direct_bench.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','pred_direct_bench','-q'],cwd=r,env=e)
    b=base/'target/release/examples/pred_direct_bench';c=cand/'target/release/examples/pred_direct_bench';crepo=[cand/p.relative_to(base) for p in repo]
    if run([str(b),'h','1',*[str(p)for p in repo]],cap=True)!=run([str(c),'h','1',*[str(p)for p in crepo]],cap=True):raise SystemExit('repo hash mismatch')
    for n,p in generated:
        if run([str(b),'h','1',str(p)],cap=True)!=run([str(c),'h','1',str(p)],cap=True):raise SystemExit('generated hash mismatch '+n)
    agg=[]
    agg.append(('repo-corpus',*paired(b,c,repo,crepo,80,25)))
    stripes=[p for n,p in generated if n.startswith('stripes-')];agg.append(('stripes-all-z',*paired(b,c,stripes,stripes,8,25)))
    tiles=[p for n,p in generated if n.startswith('tiles-')];agg.append(('tiles-all-z',*paired(b,c,tiles,tiles,8,25)))
    normal=[p for n,p in generated if n.endswith('z9')];agg.append(('generated-z9',*paired(b,c,normal,normal,5,25)))
    rows=[]
    for p,cp in zip(repo,crepo):
        t=float(run([str(b),'t','1',str(p)],cap=True));it=max(2,min(500,math.ceil(60000/max(t,1))));rows.append(('repo/'+p.name,*paired(b,c,[p],[cp],it,17)))
    for n,p in generated:
        t=float(run([str(b),'t','1',str(p)],cap=True));it=max(2,min(500,math.ceil(60000/max(t,1))));rows.append(('gen/'+n,*paired(b,c,[p],[p],it,17)))
    cpu=run(['bash','-lc',"lscpu | sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
    L=['# VP8L direct predictors on composed-v3','',f'- baseline: `{BASE}`',f'- candidate: `{CAND}`',f'- CPU: `{cpu}`','- candidate adds only packed direct-neighbor predictor modes 2–4 to composed color+meta tree','- hashes match; tests/docs/Clippy/fmt/MSRV build pass','- aggregate: 25 alternating paired rounds; per-file: 17 rounds','','## Aggregate','','| workload | base us | candidate us | paired median | positive | range |','|---|---:|---:|---:|---:|---:|']
    for x in agg:L.append(f'| {x[0]} | {x[1]:.3f} | {x[2]:.3f} | {x[3]:.4f}x | {x[4]}/25 | {x[5]:.4f}–{x[6]:.4f}x |')
    L+=['','## Per-file','','| file | base us | candidate us | paired median | positive | range |','|---|---:|---:|---:|---:|---:|']
    for x in rows:L.append(f'| {x[0]} | {x[1]:.3f} | {x[2]:.3f} | {x[3]:.4f}x | {x[4]}/17 | {x[5]:.4f}–{x[6]:.4f}x |')
    ratios=[x[3]for x in rows];repo_ratios=[x[3]for x in rows if x[0].startswith('repo/')];gen_ratios=[x[3]for x in rows if x[0].startswith('gen/')]
    L+=['','## Breadth','',f'- repository median: **{statistics.median(repo_ratios):.4f}x**, positive **{sum(x>1 for x in repo_ratios)}/{len(repo_ratios)}**',f'- generated median: **{statistics.median(gen_ratios):.4f}x**, positive **{sum(x>1 for x in gen_ratios)}/{len(gen_ratios)}**',f'- overall median: **{statistics.median(ratios):.4f}x**, positive **{sum(x>1 for x in ratios)}/{len(ratios)}**']
    Path('benchmark-vp8l-predictor-direct-on-composed.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
