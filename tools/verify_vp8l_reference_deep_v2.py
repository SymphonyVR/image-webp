#!/usr/bin/env python3
import importlib.util, hashlib, os, shutil
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v1', HERE/'verify_vp8l_reference_deep.py')
v1=importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)
BASE=v1.BASE; TMP=Path('/tmp/vp8l-ref-deep-v2')

def source_semantic_equal(decoded, original):
    if len(decoded)!=len(original): return False
    for i in range(0,len(decoded),4):
        da=decoded[i+3]; oa=original[i+3]
        if da!=oa: return False
        if oa!=0 and decoded[i:i+3]!=original[i:i+3]: return False
    return True

def main():
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir(); root=TMP/'tree'
    v1.run(['git','worktree','add','--detach',str(root),BASE])
    (root/'examples').mkdir(exist_ok=True); (root/'examples/ref_rgba.rs').write_text(v1.RUST)
    v1.run(['cargo','test','-q'],cwd=root); v1.run(['cargo','+1.80.1','build','-q'],cwd=root)
    env=os.environ.copy(); env['RUSTFLAGS']='-C target-cpu=native'
    v1.run(['cargo','build','--release','--example','ref_rgba','-q'],cwd=root,env=env)
    binp=root/'target/release/examples/ref_rgba'; cases=[]
    for p in sorted((root/'tests/images').rglob('*.webp')):
        c=v1.chunks(p.read_bytes())
        if b'VP8L' in c and b'ANIM' not in c: cases.append(('repo/'+str(p.relative_to(root)),p,None))
    dims=[(1,1),(1,7),(2,2),(3,5),(7,3),(15,17),(16,16),(17,15),(31,33),(32,32),(33,31),(63,65),(64,64),(65,63),(127,129),(128,128),(129,127),(257,193)]
    patterns=['solid','gradient','checker','palette','corr','anticorr','stripes','noise']; alphas=[None,'binary','gradient','noise']; specs=[]
    for i,(w,h) in enumerate(dims):
        specs += [(w,h,patterns[i%len(patterns)],alphas[i%len(alphas)]),(w,h,patterns[(i+3)%len(patterns)],alphas[(i+1)%len(alphas)])]
    for k in patterns:
        for a in alphas: specs.append((73,59,k,a))
    generated=0
    for ci,(w,h,k,a) in enumerate(specs):
        png=TMP/f'in-{ci}.png'; raw=v1.make_png(png,w,h,k,a)
        for z in (0,3,6,9):
            webp=TMP/f'gen-{ci}-z{z}.webp'
            cmd=['cwebp','-quiet','-lossless','-exact','-z',str(z),str(png),'-o',str(webp)]
            v1.run(cmd); cases.append((f'gen/{w}x{h}/{k}/{a}/z{z}',webp,raw)); generated+=1
    oracle_bad=[]; source_bad=[]; rows=[]
    for label,p,expected in cases:
        rust=v1.run([str(binp),str(p)],cap=True)
        out=TMP/'ref.pam'; v1.run(['dwebp','-quiet',str(p),'-pam','-o',str(out)])
        w,h,ref=v1.parse_pam(out.read_bytes())
        oracle_ok=(rust==ref)
        source_ok=(expected is None or source_semantic_equal(rust,expected))
        if not oracle_ok: oracle_bad.append(label)
        if not source_ok: source_bad.append(label)
        rows.append((label,w,h,len(rust),hashlib.sha256(rust).hexdigest()[:16],oracle_ok,source_ok))
    L=['# Deep VP8L libwebp differential verification v2','',f'- baseline: `{BASE}`',f'- total streams: **{len(cases)}**',f'- generated streams: **{generated}**','- generated streams use `cwebp -lossless -exact` at z0/z3/z6/z9','- hard oracle: Rust RGBA output must equal libwebp `dwebp` RGBA output byte-for-byte','- source fidelity: alpha must match; RGB must match wherever alpha != 0','','## Result','',f'- Rust vs libwebp mismatches: **{len(oracle_bad)}**',f'- generated-source semantic mismatches: **{len(source_bad)}**']
    if oracle_bad: L+=['','### Rust vs libwebp mismatches']+[f'- {x}' for x in oracle_bad]
    if source_bad: L+=['','### Source semantic mismatches']+[f'- {x}' for x in source_bad]
    L+=['','## Sample records','','| stream | size | bytes | sha256 prefix | libwebp | source |','|---|---:|---:|---|---|---|']
    for label,w,h,n,sha,o,s in rows[:40]: L.append(f'| {label} | {w}x{h} | {n} | `{sha}` | {o} | {s} |')
    Path('verification-vp8l-reference-deep-v2.md').write_text('\n'.join(L)+'\n'); print('\n'.join(L))
    if oracle_bad or source_bad: raise SystemExit(f'oracle={len(oracle_bad)} source={len(source_bad)}')
if __name__=='__main__': main()
