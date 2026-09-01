#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path

BASE='6f8f7d994e2f747d46621812e01c27a29ff4be4a'
TMP=Path('/tmp/vp8l-huffman-alloc-current')
VS=('base','fixedgroup','stack19','sort512','all')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''

def run(cmd,cwd=None,cap=False,env=None):
    print('+',' '.join(map(str,cmd)),flush=True)
    if cap:return subprocess.check_output(cmd,cwd=cwd,text=True,env=env).strip()
    subprocess.run(cmd,cwd=cwd,check=True,env=env)

def chunks(p):
    d=p.read_bytes();o=[];q=12
    if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP':return o
    while q+8<=len(d):
        t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
    return o

def patch(root,v):
    hp=root/'src/lossless/decoder/huffman.rs';mp=root/'src/lossless/decoder/mod.rs';h=hp.read_text();m=mp.read_text()
    if v in ('stack19','all'):
        h=h.replace('pub(crate) fn build_implicit(code_lengths: Vec<u16>) -> Result<Self, DecodingError> {','pub(crate) fn build_implicit(code_lengths: impl AsRef<[u16]>) -> Result<Self, DecodingError> {\n        let code_lengths = code_lengths.as_ref();',1)
        old='''            let mut code_length_code_lengths = vec![0; CODE_LENGTH_CODES];
            let num_code_lengths = 4 + self.bit_reader.read_bits::<usize>(4)?;
'''
        new='''            let mut code_length_code_lengths = [0u16; CODE_LENGTH_CODES];
            let num_code_lengths = 4 + self.bit_reader.read_bits::<usize>(4)?;
'''
        assert old in m;m=m.replace(old,new,1)
    if v in ('sort512','all'):
        old='''        let mut next_index = offsets;
        let mut sorted_symbols = vec![0u16; code_lengths.len()];
        for symbol in 0..code_lengths.len() {
'''
        new='''        let mut next_index = offsets;
        let mut sorted_stack = [0u16; 512];
        let mut sorted_heap = Vec::new();
        let sorted_symbols: &mut [u16] = if code_lengths.len() <= sorted_stack.len() {
            &mut sorted_stack[..code_lengths.len()]
        } else {
            sorted_heap.resize(code_lengths.len(), 0);
            sorted_heap.as_mut_slice()
        };
        for symbol in 0..code_lengths.len() {
'''
        assert old in h;h=h.replace(old,new,1)
    if v in ('fixedgroup','all'):
        m=m.replace('let mut hufftree_groups = Vec::new();','let mut hufftree_groups = Vec::with_capacity(num_huff_groups as usize);',1)
        old='''        for _i in 0..num_huff_groups {
            let mut specs = Vec::with_capacity(HUFFMAN_CODES_PER_META_CODE);
            for (j, &base_alphabet_size) in ALPHABET_SIZE.iter().enumerate() {
                let mut alphabet_size = base_alphabet_size;
                if j == 0 {
                    if let Some(color_cache) = color_cache.as_ref() {
                        alphabet_size += 1 << color_cache.color_cache_bits;
                    }
                }
                specs.push(self.read_huffman_code_spec(alphabet_size)?);
            }

            let use_wide_root = specs.iter().any(HuffmanCodeSpec::prefers_wide_root);
            if use_wide_root {
                let trees: Vec<HuffmanTree11> = specs
                    .into_iter()
                    .map(HuffmanCodeSpec::build::<11>)
                    .collect::<Result<_, _>>()?;
                let group: HuffmanCodeGroup11 =
                    trees.try_into().map_err(|_| DecodingError::HuffmanError)?;
                hufftree_groups.push(HuffmanCodeGroup::Wide(group));
            } else {
                let trees: Vec<HuffmanTree9> = specs
                    .into_iter()
                    .map(HuffmanCodeSpec::build::<9>)
                    .collect::<Result<_, _>>()?;
                let group: HuffmanCodeGroup9 =
                    trees.try_into().map_err(|_| DecodingError::HuffmanError)?;
                hufftree_groups.push(HuffmanCodeGroup::Normal(group));
            }
        }
'''
        new='''        for _i in 0..num_huff_groups {
            let mut specs: [Option<HuffmanCodeSpec>; HUFFMAN_CODES_PER_META_CODE] =
                [None, None, None, None, None];
            for (j, &base_alphabet_size) in ALPHABET_SIZE.iter().enumerate() {
                let mut alphabet_size = base_alphabet_size;
                if j == 0 {
                    if let Some(color_cache) = color_cache.as_ref() {
                        alphabet_size += 1 << color_cache.color_cache_bits;
                    }
                }
                specs[j] = Some(self.read_huffman_code_spec(alphabet_size)?);
            }

            let use_wide_root = specs
                .iter()
                .filter_map(Option::as_ref)
                .any(HuffmanCodeSpec::prefers_wide_root);
            if use_wide_root {
                let group: HuffmanCodeGroup11 = [
                    specs[0].take().unwrap().build::<11>()?,
                    specs[1].take().unwrap().build::<11>()?,
                    specs[2].take().unwrap().build::<11>()?,
                    specs[3].take().unwrap().build::<11>()?,
                    specs[4].take().unwrap().build::<11>()?,
                ];
                hufftree_groups.push(HuffmanCodeGroup::Wide(group));
            } else {
                let group: HuffmanCodeGroup9 = [
                    specs[0].take().unwrap().build::<9>()?,
                    specs[1].take().unwrap().build::<9>()?,
                    specs[2].take().unwrap().build::<9>()?,
                    specs[3].take().unwrap().build::<9>()?,
                    specs[4].take().unwrap().build::<9>()?,
                ];
                hufftree_groups.push(HuffmanCodeGroup::Normal(group));
            }
        }
'''
        assert old in m;m=m.replace(old,new,1)
    hp.write_text(h);mp.write_text(m)

def invoke(exe,mode,n,files):return run(['taskset','-c','0',str(exe),mode,str(n),*map(str,files)],cap=True)

def main():
    if TMP.exists():shutil.rmtree(TMP)
    TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
    for v in VS:
        r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
        if v!='base':
            patch(r,v);run(['cargo','fmt'],cwd=r)
            for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
        (r/'examples').mkdir(exist_ok=True);(r/'examples/halloc.rs').write_text(BENCH);run(['cargo','build','--release','--example','halloc','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/halloc'
    rels=[p.relative_to(roots['base']) for p in sorted((roots['base']/'tests/images').rglob('*.webp')) if b'VP8L' in chunks(p) and b'ANIM' not in chunks(p)]
    ppm=TMP/'large.ppm';w=h=2048
    with ppm.open('wb') as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
        for y in range(h):
            for x in range(w):
                i=x*3;row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
            f.write(row)
    large=TMP/'large.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(large)])
    corpus={v:[roots[v]/x for x in rels] for v in VS};base_hash=invoke(exes['base'],'h',1,corpus['base']+[large])
    for v in VS[1:]:assert base_hash==invoke(exes[v],'h',1,corpus[v]+[large])
    workloads={'corpus':(corpus,70),'large':({v:[large] for v in VS},4)};results={}
    for name,(files,it) in workloads.items():
        rows=[]
        for n in range(17):
            order=VS if n%2==0 else tuple(reversed(VS));z={}
            for v in order:z[v]=float(invoke(exes[v],'t',it,files[v]))
            rows.append(z)
        results[name]=rows
    cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L Huffman allocation current-final matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
    for name,rows in results.items():
        for v in VS[1:]:
            q=[z['base']/z[v] for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
    Path('benchmark-vp8l-huffman-alloc-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
