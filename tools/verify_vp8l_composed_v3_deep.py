#!/usr/bin/env python3
import hashlib, os, shutil, subprocess
from pathlib import Path
from PIL import Image

CAND='4cd194935d100a09acf24eb24d8c1343c7844844'
TMP=Path('/tmp/vp8l-composed-v3-deep')

def run(cmd,cwd=None,cap=False,env=None):
    print('+',' '.join(map(str,cmd)),flush=True)
    if cap:
        return subprocess.check_output(cmd,cwd=cwd,env=env)
    subprocess.run(cmd,cwd=cwd,check=True,env=env)

def chunks(data):
    if len(data)<12 or data[:4]!=b'RIFF' or data[8:12]!=b'WEBP': return []
    out=[]; p=12
    while p+8<=len(data):
        tag=data[p:p+4]; n=int.from_bytes(data[p+4:p+8],'little'); out.append(tag); p+=8+n+(n&1)
    return out

def parse_pam(data):
    if not data.startswith(b'P7\n'):
        raise RuntimeError('expected PAM from dwebp')
    end=data.index(b'ENDHDR\n')+len(b'ENDHDR\n')
    vals={}
    for line in data[:end].decode('ascii').splitlines()[1:]:
        if ' ' in line:
            k,v=line.split(' ',1); vals[k]=v
    w=int(vals['WIDTH']); h=int(vals['HEIGHT']); depth=int(vals['DEPTH']); raw=data[end:]
    if len(raw)!=w*h*depth: raise RuntimeError('bad PAM size')
    if depth==4: return w,h,raw
    if depth==3:
        out=bytearray(w*h*4)
        for i in range(w*h): out[4*i:4*i+4]=raw[3*i:3*i+3]+b'\xff'
        return w,h,bytes(out)
    raise RuntimeError(f'unsupported PAM depth {depth}')

def pixel(kind,x,y,w,h,alpha):
    if kind=='solid': r,g,b=37,149,233
    elif kind=='gradient': r=x*255//max(1,w-1); g=y*255//max(1,h-1); b=(x+y)*255//max(1,w+h-2)
    elif kind=='checker': q=((x>>2)^(y>>2))&1; r=255*q; g=63+128*(1-q); b=17+211*q
    elif kind=='palette':
        pal=[(0,0,0),(255,255,255),(255,0,80),(20,220,70),(30,90,250),(230,190,20),(170,40,220),(20,210,210),(110,100,90),(5,150,240),(245,80,30),(80,230,170),(130,30,70),(70,120,10),(200,200,240),(44,55,66)]
        r,g,b=pal[((x>>1)+3*(y>>1))&15]
    elif kind=='corr': g=(x*7+y*11+((x*y)>>4))&255; r=(g+((x>>2)&31))&255; b=(g-((y>>2)&31))&255
    elif kind=='anticorr': g=(x*5+y*3)&255; r=(255-g+((x>>3)&15))&255; b=g^255
    elif kind=='stripes': r=(x*17)&255; g=((x//3)*53+y)&255; b=((x//7)*91+y*3)&255
    elif kind=='tiles': q=((x>>4)+3*(y>>4))&15; r=q*17; g=(q*53+(x&15)*7)&255; b=(q*91+(y&15)*11)&255
    else:
        z=(x*1103515245+y*12345+(x*y)*2654435761+0x9e3779b9)&0xffffffff; r=(z>>8)&255; g=(z>>16)&255; b=(z>>24)&255
    if alpha is None: return r,g,b,255
    if alpha=='binary': a=255 if ((x>>2)^(y>>2))&1 else 0
    elif alpha=='gradient': a=(x*13+y*29)&255
    elif alpha=='sparse': a=255 if ((x*17+y*31)%19)==0 else 0
    else: a=((x*17+y*31+(x*y))>>2)&255
    return r,g,b,a

def make_png(path,w,h,kind,alpha):
    img=Image.new('RGBA',(w,h)); vals=[]
    for y in range(h):
        for x in range(w): vals.append(pixel(kind,x,y,w,h,alpha))
    img.putdata(vals); img.save(path)
    return b''.join(bytes(p) for p in vals)

RUST=r'''use image_webp::WebPDecoder;use std::io::{Cursor,Write};fn main(){let p=std::env::args().nth(1).unwrap();let d=std::fs::read(p).unwrap();let mut q=WebPDecoder::new(Cursor::new(d)).unwrap();let(w,h)=q.dimensions();let alpha=q.has_alpha();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();let mut out=Vec::with_capacity(w as usize*h as usize*4);if alpha{out.extend_from_slice(&b)}else{for p in b.chunks_exact(3){out.extend_from_slice(p);out.push(255)}}std::io::stdout().write_all(&out).unwrap();}'''

def main():
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir(); root=TMP/'tree'; run(['git','worktree','add','--detach',str(root),CAND])
    run(['cargo','test','-q'],cwd=root); run(['cargo','doc','--no-deps','-q'],cwd=root); run(['cargo','clippy','--','-D','warnings'],cwd=root); run(['cargo','fmt','--','--check'],cwd=root); run(['cargo','+1.80.1','build','-q'],cwd=root)
    (root/'examples').mkdir(exist_ok=True); (root/'examples/ref_rgba.rs').write_text(RUST)
    env=os.environ.copy(); env['RUSTFLAGS']='-C target-cpu=native'; run(['cargo','build','--release','--example','ref_rgba','-q'],cwd=root,env=env); rustbin=root/'target/release/examples/ref_rgba'

    cases=[]
    for p in sorted((root/'tests/images').rglob('*.webp')):
        c=chunks(p.read_bytes())
        if b'VP8L' in c and b'ANIM' not in c: cases.append(('repo/'+str(p.relative_to(root)),p,None))

    dims=[(1,1),(1,7),(2,2),(3,5),(4,4),(7,3),(15,17),(16,16),(17,15),(31,33),(32,32),(33,31),(63,65),(64,64),(65,63),(127,129),(128,128),(129,127),(255,257),(256,256),(257,255)]
    patterns=['solid','gradient','checker','palette','corr','anticorr','stripes','tiles','noise']
    alphas=[None,'binary','gradient','sparse','noise']
    specs=[]
    for i,(w,h) in enumerate(dims):
        specs.append((w,h,patterns[i%len(patterns)],alphas[i%len(alphas)]))
        specs.append((w,h,patterns[(i+4)%len(patterns)],alphas[(i+2)%len(alphas)]))
    for k in patterns:
        for a in alphas: specs.append((73,59,k,a))
    for k in ('gradient','corr','stripes','tiles','noise'):
        for a in (None,'binary','gradient','sparse','noise'): specs.append((193,131,k,a))

    generated=0
    for ci,(w,h,k,a) in enumerate(specs):
        png=TMP/f'in-{ci}.png'; expected=make_png(png,w,h,k,a)
        for z in (0,3,6,9):
            webp=TMP/f'gen-{ci}-z{z}.webp'
            run(['cwebp','-quiet','-lossless','-exact','-z',str(z),str(png),'-o',str(webp)])
            cases.append((f'gen/{w}x{h}/{k}/{a}/z{z}',webp,expected)); generated+=1

    oracle_mismatch=[]; source_mismatch=[]; rows=[]
    for label,p,expected in cases:
        rust=run([str(rustbin),str(p)],cap=True)
        out=TMP/'ref.pam'; run(['dwebp','-quiet',str(p),'-pam','-o',str(out)]); w,h,ref=parse_pam(out.read_bytes())
        oracle_ok=rust==ref
        source_ok=expected is None or rust==expected
        if not oracle_ok: oracle_mismatch.append(label)
        if not source_ok: source_mismatch.append(label)
        rows.append((label,w,h,len(rust),hashlib.sha256(rust).hexdigest()[:16],oracle_ok,source_ok))

    L=['# Deep VP8L composed-v3 differential verification','',f'- candidate: `{CAND}`',f'- total streams: **{len(cases)}**',f'- generated streams: **{generated}**','- hard oracle: candidate Rust decoder output must equal libwebp `dwebp` byte-for-byte','- generated fidelity: `cwebp -lossless -exact` output must round-trip to original RGBA bytes','- coverage: tiny/odd/block-boundary dimensions; palette/correlated/anti-correlated/stripes/tiles/noise; opaque/binary/gradient/sparse/noisy alpha; z0/z3/z6/z9','',f'- Rust vs libwebp mismatches: **{len(oracle_mismatch)}**',f'- generated source-fidelity mismatches: **{len(source_mismatch)}**']
    if oracle_mismatch: L+=['','## Oracle mismatches']+[f'- {x}' for x in oracle_mismatch]
    if source_mismatch: L+=['','## Source-fidelity mismatches']+[f'- {x}' for x in source_mismatch]
    L+=['','## Sample records','','| stream | size | bytes | sha256 prefix | oracle | source |','|---|---:|---:|---|---|---|']
    for label,w,h,n,sha,ok,src in rows[:50]: L.append(f'| {label} | {w}x{h} | {n} | `{sha}` | {ok} | {src} |')
    Path('verification-vp8l-composed-v3-deep.md').write_text('\n'.join(L)+'\n'); print('\n'.join(L))
    if oracle_mismatch or source_mismatch: raise SystemExit(f'oracle={len(oracle_mismatch)} source={len(source_mismatch)}')

if __name__=='__main__': main()
