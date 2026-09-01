#!/usr/bin/env python3
import hashlib, os, shutil, subprocess
from pathlib import Path
from PIL import Image

BASE='509d11c2bf102929ded4be05d3c54b06032fdc44'
TMP=Path('/tmp/vp8l-ref-deep')

def run(c,cwd=None,cap=False,env=None):
    print('+',' '.join(map(str,c)),flush=True)
    if cap:
        return subprocess.check_output(c,cwd=cwd,env=env)
    subprocess.run(c,cwd=cwd,check=True,env=env)

def chunks(d):
    if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP': return []
    out=[];p=12
    while p+8<=len(d):
        f=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');out.append(f);p+=8+n+(n&1)
    return out

def parse_pam(data):
    if data.startswith(b'P7\n'):
        end=data.index(b'ENDHDR\n')+len(b'ENDHDR\n')
        hdr=data[:end].decode('ascii').splitlines(); vals={}
        for line in hdr[1:]:
            if ' ' in line:
                k,v=line.split(' ',1); vals[k]=v
        w=int(vals['WIDTH']);h=int(vals['HEIGHT']);depth=int(vals['DEPTH']);raw=data[end:]
        assert len(raw)==w*h*depth
        if depth==4:return w,h,raw
        if depth==3:
            o=bytearray(w*h*4)
            for i in range(w*h):o[4*i:4*i+4]=raw[3*i:3*i+3]+b'\xff'
            return w,h,bytes(o)
        raise RuntimeError(f'unsupported PAM depth {depth}')
    if data.startswith(b'P6'):
        # minimal binary PPM parser
        p=2; toks=[]
        while len(toks)<3:
            while data[p] in b' \t\r\n':p+=1
            if data[p]==35:
                p=data.index(b'\n',p)+1;continue
            q=p
            while data[q] not in b' \t\r\n':q+=1
            toks.append(int(data[p:q]));p=q
        while data[p] in b' \t\r\n':p+=1
        w,h,m=toks;assert m==255;raw=data[p:];assert len(raw)==w*h*3
        o=bytearray(w*h*4)
        for i in range(w*h):o[4*i:4*i+4]=raw[3*i:3*i+3]+b'\xff'
        return w,h,bytes(o)
    raise RuntimeError('unknown dwebp output')

def pix(kind,x,y,w,h,alpha):
    if kind=='solid': r,g,b=37,149,233
    elif kind=='gradient': r=x*255//max(1,w-1);g=y*255//max(1,h-1);b=(x+y)*255//max(1,w+h-2)
    elif kind=='checker': q=((x>>2)^(y>>2))&1;r=255*q;g=63+128*(1-q);b=17+211*q
    elif kind=='palette':
        pal=[(0,0,0),(255,255,255),(255,0,80),(20,220,70),(30,90,250),(230,190,20),(170,40,220),(20,210,210),(110,100,90),(5,150,240),(245,80,30),(80,230,170),(130,30,70),(70,120,10),(200,200,240),(44,55,66)]
        r,g,b=pal[((x>>1)+3*(y>>1))&15]
    elif kind=='corr': g=(x*7+y*11+((x*y)>>4))&255;r=(g+((x>>2)&31))&255;b=(g-((y>>2)&31))&255
    elif kind=='anticorr': g=(x*5+y*3)&255;r=(255-g+((x>>3)&15))&255;b=g^255
    elif kind=='stripes': r=(x*17)&255;g=((x//3)*53)&255;b=((x//7)*91+y)&255
    else:
        z=(x*1103515245+y*12345+(x*y)*2654435761+0x9e3779b9)&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
    if not alpha:return (r,g,b,255)
    if alpha=='binary':a=255 if ((x>>2)^(y>>2))&1 else 0
    elif alpha=='gradient':a=(x*13+y*29)&255
    else:a=((x*17+y*31+(x*y))>>2)&255
    return r,g,b,a

def make_png(path,w,h,kind,alpha):
    mode='RGBA' if alpha else 'RGB';img=Image.new(mode,(w,h));data=[]
    for y in range(h):
        for x in range(w):
            p=pix(kind,x,y,w,h,alpha);data.append(p if alpha else p[:3])
    img.putdata(data);img.save(path)
    rgba=bytearray(w*h*4)
    for i,p in enumerate(data):
        if alpha:rgba[4*i:4*i+4]=bytes(p)
        else:rgba[4*i:4*i+4]=bytes(p)+b'\xff'
    return bytes(rgba)

RUST=r'''use image_webp::WebPDecoder;use std::io::{Cursor,Write};fn main(){let p=std::env::args().nth(1).unwrap();let d=std::fs::read(p).unwrap();let mut q=WebPDecoder::new(Cursor::new(d)).unwrap();let(w,h)=q.dimensions();let alpha=q.has_alpha();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();let mut out=Vec::with_capacity(w as usize*h as usize*4);if alpha{out.extend_from_slice(&b)}else{for p in b.chunks_exact(3){out.extend_from_slice(p);out.push(255)}}std::io::stdout().write_all(&out).unwrap();}'''

def main():
    if TMP.exists():shutil.rmtree(TMP)
    TMP.mkdir();root=TMP/'tree';run(['git','worktree','add','--detach',str(root),BASE])
    (root/'examples').mkdir(exist_ok=True);(root/'examples/ref_rgba.rs').write_text(RUST)
    run(['cargo','test','--all-features','-q'],cwd=root);run(['cargo','+1.80.1','build','-q'],cwd=root)
    env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','ref_rgba','-q'],cwd=root,env=env);binp=root/'target/release/examples/ref_rgba'
    cases=[]
    for p in sorted((root/'tests/images').rglob('*.webp')):
        c=chunks(p.read_bytes())
        if b'VP8L'in c and b'ANIM'not in c:cases.append(('repo/'+str(p.relative_to(root)),p,None))
    dims=[(1,1),(1,7),(2,2),(3,5),(7,3),(15,17),(16,16),(17,15),(31,33),(32,32),(33,31),(63,65),(64,64),(65,63),(127,129),(128,128),(129,127),(257,193)]
    patterns=['solid','gradient','checker','palette','corr','anticorr','stripes','noise']
    alphas=[None,'binary','gradient','noise']
    generated=0
    # exhaustive small/boundary dimensions with rotating pattern/alpha, plus a broad pattern sweep at representative odd size
    specs=[]
    for i,(w,h) in enumerate(dims):
        specs.append((w,h,patterns[i%len(patterns)],alphas[i%len(alphas)]))
        specs.append((w,h,patterns[(i+3)%len(patterns)],alphas[(i+1)%len(alphas)]))
    for k in patterns:
        for a in alphas:specs.append((73,59,k,a))
    for ci,(w,h,k,a) in enumerate(specs):
        png=TMP/f'in-{ci}.png';raw=make_png(png,w,h,k,a)
        for z in (0,3,6,9):
            webp=TMP/f'gen-{ci}-z{z}.webp';run(['cwebp','-quiet','-lossless','-z',str(z),str(png),'-o',str(webp)]);cases.append((f'gen/{w}x{h}/{k}/{a}/z{z}',webp,raw));generated+=1
    mismatches=[];rows=[]
    for label,p,expected in cases:
        rust=run([str(binp),str(p)],cap=True)
        out=TMP/'ref.pam';run(['dwebp','-quiet',str(p),'-pam','-o',str(out)]);w,h,ref=parse_pam(out.read_bytes())
        ok=(rust==ref) and (expected is None or rust==expected)
        rows.append((label,w,h,len(rust),hashlib.sha256(rust).hexdigest()[:16],ok))
        if not ok:mismatches.append(label)
    L=['# Deep VP8L libwebp differential verification','',f'- baseline: `{BASE}`',f'- total streams: **{len(cases)}**',f'- generated streams: **{generated}**','- oracle: libwebp `dwebp`; generated lossless files are additionally compared to original RGBA pixels','- generated coverage: tiny/odd/block-boundary dimensions, RGB/RGBA, binary/gradient/noisy alpha, solid/gradient/checker/palette/correlated/anti-correlated/stripes/noise, cwebp z0/z3/z6/z9','',f'- mismatches: **{len(mismatches)}**']
    if mismatches:L += ['', '## Mismatches'] + [f'- {x}' for x in mismatches]
    L += ['', '## Sample verification records','', '| stream | size | bytes | sha256 prefix | ok |','|---|---:|---:|---|---|']
    for label,w,h,n,sha,ok in rows[:30]:L.append(f'| {label} | {w}x{h} | {n} | `{sha}` | {ok} |')
    Path('verification-vp8l-reference-deep.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
    if mismatches:raise SystemExit(f'{len(mismatches)} differential mismatches')
if __name__=='__main__':main()
