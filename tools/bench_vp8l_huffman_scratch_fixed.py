#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path
BASE = '509d11c2bf102929ded4be05d3c54b06032fdc44'
TMP = Path('/tmp/vp8l-huff-scratch-fixed')
VS = ['reuse', 'reuse_sorted', 'all']

def run(cmd, cwd=None, capture=False, env=None):
    print('+', ' '.join(map(str, cmd)), flush=True)
    if capture:
        return subprocess.check_output(cmd, cwd=cwd, text=True, env=env).strip()
    subprocess.run(cmd, cwd=cwd, check=True, env=env)

def rep(s, old, new, label):
    if old not in s:
        raise SystemExit('missing marker: ' + label)
    return s.replace(old, new, 1)

def apply_reuse(h, m):
    h = rep(h,
        'pub(crate) fn build_implicit(code_lengths: Vec<u16>) -> Result<Self, DecodingError> {',
        'pub(crate) fn build_implicit(code_lengths: &[u16]) -> Result<Self, DecodingError> {', 'slice build')
    m = rep(m, 'let mut hufftree_groups = Vec::new();',
        'let mut hufftree_groups = Vec::new();\n        let mut code_lengths_scratch = Vec::new();', 'scratch declaration')
    m = rep(m, 'let tree = self.read_huffman_code(alphabet_size)?;',
        'let tree = self.read_huffman_code(alphabet_size, &mut code_lengths_scratch)?;', 'read tree call')
    m = rep(m,
        'fn read_huffman_code(&mut self, alphabet_size: u16) -> Result<HuffmanTree, DecodingError> {',
        'fn read_huffman_code(&mut self, alphabet_size: u16, code_lengths_scratch: &mut Vec<u16>) -> Result<HuffmanTree, DecodingError> {', 'read tree signature')
    m = rep(m, 'let mut code_length_code_lengths = vec![0; CODE_LENGTH_CODES];',
        'let mut code_length_code_lengths = [0u16; CODE_LENGTH_CODES];', 'small stack lengths')
    m = rep(m,
'''            let new_code_lengths =
                self.read_huffman_code_lengths(code_length_code_lengths, alphabet_size)?;

            HuffmanTree::build_implicit(new_code_lengths)
''',
'''            self.read_huffman_code_lengths(
                &code_length_code_lengths,
                alphabet_size,
                code_lengths_scratch,
            )?;
            HuffmanTree::build_implicit(code_lengths_scratch.as_slice())
''', 'read lengths call')
    m = rep(m,
'''        code_length_code_lengths: Vec<u16>,
        num_symbols: u16,
    ) -> Result<Vec<u16>, DecodingError> {
        let table = HuffmanTree::build_implicit(code_length_code_lengths)?;
''',
'''        code_length_code_lengths: &[u16],
        num_symbols: u16,
        code_lengths: &mut Vec<u16>,
    ) -> Result<(), DecodingError> {
        let table = HuffmanTree::build_implicit(code_length_code_lengths)?;
''', 'read lengths signature')
    m = rep(m,
'''        let mut code_lengths = vec![0; usize::from(num_symbols)];
        let mut prev_code_len = 8; //default code length
''',
'''        code_lengths.clear();
        code_lengths.resize(usize::from(num_symbols), 0);
        let mut prev_code_len = 8; //default code length
''', 'scratch resize')
    m = rep(m,
'''        Ok(code_lengths)
    }

    /// Decodes the image data''',
'''        Ok(())
    }

    /// Decodes the image data''', 'unit return')
    return h, m

def apply_sorted(h):
    return rep(h,
'''        let mut next_index = offsets;
        let mut sorted_symbols = vec![0u16; code_lengths.len()];
        for symbol in 0..code_lengths.len() {
''',
'''        let mut next_index = offsets;
        let mut sorted_stack = [0u16; 512];
        let mut sorted_heap = Vec::new();
        let sorted_symbols: &mut [u16] = if code_lengths.len() <= sorted_stack.len() {
            &mut sorted_stack[..code_lengths.len()]
        } else {
            sorted_heap.resize(code_lengths.len(), 0);
            sorted_heap.as_mut_slice()
        };
        for symbol in 0..code_lengths.len() {
''', 'sorted scratch')

def patch(name, root):
    hp = root/'src/lossless/decoder/huffman.rs'; mp = root/'src/lossless/decoder/mod.rs'
    h, m = hp.read_text(), mp.read_text()
    h, m = apply_reuse(h, m)
    if name in ('reuse_sorted', 'all'):
        h = apply_sorted(h)
    if name == 'all':
        m = rep(m, 'let mut hufftree_groups = Vec::new();',
            'let mut hufftree_groups = Vec::with_capacity(num_huff_groups as usize);', 'group reserve')
    hp.write_text(h); mp.write_text(m)

def prepare(name):
    root = TMP/name
    run(['git','worktree','add','--detach',str(root),BASE])
    if name != 'base':
        patch(name, root)
        run(['cargo','fmt'], cwd=root)
        run(['cargo','test','-q'], cwd=root)
        run(['cargo','+1.80.1','build','-q'], cwd=root)
    return root

def chunks(d):
    if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP': return []
    out=[]; p=12
    while p+8<=len(d):
        f=d[p:p+4]; n=int.from_bytes(d[p+4:p+8],'little'); out.append(f); p+=8+n+(n&1)
    return out

def corpus(root):
    return [p.relative_to(root) for p in sorted((root/'tests/images').rglob('*.webp'))
            if b'VP8L' in chunks(p.read_bytes()) and b'ANIM' not in chunks(p.read_bytes())]
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def build(root):
    (root/'examples').mkdir(exist_ok=True); (root/'examples/hsfix.rs').write_text(BENCH)
    env=os.environ.copy(); env['RUSTFLAGS']='-C target-cpu=native'
    run(['cargo','build','--release','--example','hsfix','-q'],cwd=root,env=env)
    return root/'target/release/examples/hsfix'
def invoke(binary, mode, n, paths):
    return run(['taskset','-c','0',str(binary),mode,str(n),*[str(x) for x in paths]],capture=True)
def main():
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir()
    roots={n:prepare(n) for n in ['base',*VS]}; rels=corpus(roots['base'])
    ppm=TMP/'large.ppm'; w=h=1536
    with ppm.open('wb') as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode()); row=bytearray(w*3)
        for y in range(h):
            for x in range(w):
                i=x*3; row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255; row[i+1]=(x*2+y*7+((x*y)>>10))&255; row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
            f.write(row)
    webp=TMP/'large.webp'; run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)])
    bins={n:build(r) for n,r in roots.items()}
    bh=invoke(bins['base'],'h',1,[*[roots['base']/r for r in rels],webp])
    for n in VS:
        if invoke(bins[n],'h',1,[*[roots[n]/r for r in rels],webp]) != bh: raise SystemExit('hash '+n)
    rows=[]
    for rnd in range(1,12):
        order=['base',*VS] if rnd%2 else [*reversed(VS),'base']
        for n in order:
            rows.append(('corpus',rnd,n,float(invoke(bins[n],'bench',50,[roots[n]/r for r in rels]))))
            rows.append(('large',rnd,n,float(invoke(bins[n],'bench',3,[webp]))))
    rr={}
    for w,r,n,x in rows: rr.setdefault((w,r),{})[n]=x
    cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],capture=True)
    lines=['# VP8L Huffman scratch closure v2','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + MSRV passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
    for w in ('corpus','large'):
        for n in VS:
            q=[z['base']/z[n] for (ww,_),z in sorted(rr.items()) if ww==w]
            lines.append(f'| {w} | {n} | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
    Path('benchmark-vp8l-huffman-scratch-v2.md').write_text('\n'.join(lines)+'\n'); print('\n'.join(lines))
if __name__=='__main__': main()
