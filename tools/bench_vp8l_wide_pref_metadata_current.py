#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path

BASE='84d8d20753fce0a9972e8a244fdf929b5a55671c'
TMP=Path('/tmp/vp8l-wide-pref-meta')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''

def run(c,cwd=None,cap=False,env=None):
    print('+',' '.join(map(str,c)),flush=True)
    if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
    subprocess.run(c,cwd=cwd,check=True,env=env)

def chunks(p):
    d=p.read_bytes();o=[];q=12
    if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP':return o
    while q+8<=len(d):t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
    return o

def patch(r):
    p=r/'src/lossless/decoder/mod.rs';s=p.read_text()
    old='''enum HuffmanCodeSpec {\n    Single(u16),\n    Two(u16, u16),\n    Implicit(Vec<u16>),\n}\n'''
    new='''enum HuffmanCodeSpec {\n    Single(u16),\n    Two(u16, u16),\n    Implicit {\n        code_lengths: Vec<u16>,\n        prefers_wide: bool,\n    },\n}\n'''
    assert old in s;s=s.replace(old,new,1)
    a=s.index('impl HuffmanCodeSpec {');b=s.index('\n}\n\nconst ALPHABET_SIZE:',a)+2
    new_impl='''impl HuffmanCodeSpec {
    fn prefers_wide_root(&self) -> bool {
        match self {
            Self::Implicit { prefers_wide, .. } => *prefers_wide,
            _ => false,
        }
    }

    fn build<const TABLE_BITS: u8>(self) -> Result<HuffmanTree<TABLE_BITS>, DecodingError> {
        match self {
            Self::Single(symbol) => Ok(HuffmanTree::build_single_node(symbol)),
            Self::Two(zero, one) => Ok(HuffmanTree::build_two_node(zero, one)),
            Self::Implicit { code_lengths, .. } => HuffmanTree::build_implicit(code_lengths),
        }
    }
}'''
    s=s[:a]+new_impl+s[b:]
    old='''            let code_lengths =\n                self.read_huffman_code_lengths(&code_length_code_lengths, alphabet_size)?;\n            Ok(HuffmanCodeSpec::Implicit(code_lengths))\n'''
    new='''            let (code_lengths, prefers_wide) =\n                self.read_huffman_code_lengths(&code_length_code_lengths, alphabet_size)?;\n            Ok(HuffmanCodeSpec::Implicit {\n                code_lengths,\n                prefers_wide,\n            })\n'''
    assert old in s;s=s.replace(old,new,1)
    old=''') -> Result<Vec<u16>, DecodingError> {\n        let table = HuffmanTree9::build_implicit(code_length_code_lengths)?;\n'''
    new=''') -> Result<(Vec<u16>, bool), DecodingError> {\n        let table = HuffmanTree9::build_implicit(code_length_code_lengths)?;\n'''
    assert old in s;s=s.replace(old,new,1)
    old='''        let mut code_lengths = vec![0; usize::from(num_symbols)];\n        let mut prev_code_len = 8; //default code length\n'''
    new='''        let mut code_lengths = vec![0; usize::from(num_symbols)];\n        let mut nonzero_symbols = 0usize;\n        let mut long_symbols = 0usize;\n        let mut prev_code_len = 8; //default code length\n'''
    assert old in s;s=s.replace(old,new,1)
    old='''                if code_len != 0 {\n                    prev_code_len = code_len;\n                }\n'''
    new='''                if code_len != 0 {\n                    nonzero_symbols += 1;\n                    if code_len > 9 {\n                        long_symbols += 1;\n                    }\n                    prev_code_len = code_len;\n                }\n'''
    assert old in s;s=s.replace(old,new,1)
    old='''                let length = if use_prev { prev_code_len } else { 0 };\n                while repeat > 0 {\n'''
    new='''                let length = if use_prev { prev_code_len } else { 0 };\n                if length != 0 {\n                    nonzero_symbols += usize::from(repeat);\n                    if length > 9 {\n                        long_symbols += usize::from(repeat);\n                    }\n                }\n                while repeat > 0 {\n'''
    assert old in s;s=s.replace(old,new,1)
    old='''        Ok(code_lengths)\n    }\n\n    /// Decodes the image data using the huffman trees'''
    new='''        let prefers_wide = nonzero_symbols >= 256 && long_symbols * 8 >= nonzero_symbols;\n        Ok((code_lengths, prefers_wide))\n    }\n\n    /// Decodes the image data using the huffman trees'''
    assert old in s;s=s.replace(old,new,1)
    p.write_text(s)

def inv(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)

def main():
    if TMP.exists():shutil.rmtree(TMP)
    TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
    for v in ('base','cand'):
        r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
        if v=='cand':
            patch(r);run(['cargo','fmt'],cwd=r)
            for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
        (r/'examples').mkdir(exist_ok=True);(r/'examples/wpref.rs').write_text(BENCH);run(['cargo','build','--release','--example','wpref','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/wpref'
    rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
    ppm=TMP/'large.ppm';w=h=2048
    with ppm.open('wb')as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
        for y in range(h):
            for x in range(w):i=x*3;row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
            f.write(row)
    large=TMP/'large.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(large)])
    corpus={v:[roots[v]/x for x in rels]for v in ('base','cand')};assert inv(exes['base'],'h',1,corpus['base']+[large])==inv(exes['cand'],'h',1,corpus['cand']+[large])
    results={}
    for name,files,it in [('corpus',corpus,70),('large',{'base':[large],'cand':[large]},4)]:
        q=[]
        for n in range(17):
            order=('base','cand')if n%2==0 else('cand','base');z={}
            for v in order:z[v]=float(inv(exes[v],'t',it,files[v]))
            q.append(z['base']/z['cand'])
        results[name]=q
    cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L wide-root preference metadata benchmark','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed','- avoids rescanning implicit code lengths solely to select 9/11-bit root width','','| workload | paired median | positive | range |','|---|---:|---:|---:|']
    for name,q in results.items():L.append(f'| {name} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
    Path('benchmark-vp8l-wide-pref-metadata-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
