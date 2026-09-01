#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path

BASE='c52de05b9c902a6743941b998c96d5e4d3ba3609'
TMP=Path('/tmp/vp8l-code-length-arena-current')
VS=('base','arena','arena-fixed')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''

SPEC=r'''#[derive(Debug)]
enum HuffmanCodeSpec {
    Single(u16),
    Two(u16, u16),
    Implicit { start: usize, len: usize },
}

impl HuffmanCodeSpec {
    fn implicit_lengths<'a>(&self, arena: &'a [u16]) -> Option<&'a [u16]> {
        let Self::Implicit { start, len } = *self else {
            return None;
        };
        Some(&arena[start..start + len])
    }

    fn prefers_wide_root(&self, arena: &[u16]) -> bool {
        let Some(code_lengths) = self.implicit_lengths(arena) else {
            return false;
        };
        let mut symbols = 0usize;
        let mut long_symbols = 0usize;
        for &length in code_lengths {
            if length != 0 {
                symbols += 1;
                if length > 9 {
                    long_symbols += 1;
                }
            }
        }
        symbols >= 256 && long_symbols * 8 >= symbols
    }

    fn build<const TABLE_BITS: u8>(
        self,
        arena: &[u16],
    ) -> Result<HuffmanTree<TABLE_BITS>, DecodingError> {
        match self {
            Self::Single(symbol) => Ok(HuffmanTree::build_single_node(symbol)),
            Self::Two(zero, one) => Ok(HuffmanTree::build_two_node(zero, one)),
            Self::Implicit { start, len } => {
                HuffmanTree::build_implicit(&arena[start..start + len])
            }
        }
    }
}

'''

GROUP_ARENA=r'''        let mut hufftree_groups = Vec::new();
        let code_lengths_capacity = ALPHABET_SIZE
            .iter()
            .map(|&size| usize::from(size))
            .sum::<usize>()
            + color_cache
                .as_ref()
                .map(|cache| 1usize << cache.color_cache_bits)
                .unwrap_or(0);
        let mut code_lengths_arena = Vec::with_capacity(code_lengths_capacity);

        for _i in 0..num_huff_groups {
            code_lengths_arena.clear();
            let mut specs = Vec::with_capacity(HUFFMAN_CODES_PER_META_CODE);
            for (j, &base_alphabet_size) in ALPHABET_SIZE.iter().enumerate() {
                let mut alphabet_size = base_alphabet_size;
                if j == 0 {
                    if let Some(color_cache) = color_cache.as_ref() {
                        alphabet_size += 1 << color_cache.color_cache_bits;
                    }
                }
                specs.push(self.read_huffman_code_spec(alphabet_size, &mut code_lengths_arena)?);
            }

            let use_wide_root = specs
                .iter()
                .any(|spec| spec.prefers_wide_root(&code_lengths_arena));
            if use_wide_root {
                let trees: Vec<HuffmanTree11> = specs
                    .into_iter()
                    .map(|spec| spec.build::<11>(&code_lengths_arena))
                    .collect::<Result<_, _>>()?;
                let group: HuffmanCodeGroup11 =
                    trees.try_into().map_err(|_| DecodingError::HuffmanError)?;
                hufftree_groups.push(HuffmanCodeGroup::Wide(group));
            } else {
                let trees: Vec<HuffmanTree9> = specs
                    .into_iter()
                    .map(|spec| spec.build::<9>(&code_lengths_arena))
                    .collect::<Result<_, _>>()?;
                let group: HuffmanCodeGroup9 =
                    trees.try_into().map_err(|_| DecodingError::HuffmanError)?;
                hufftree_groups.push(HuffmanCodeGroup::Normal(group));
            }
        }
'''

GROUP_FIXED=r'''        let mut hufftree_groups = Vec::with_capacity(num_huff_groups as usize);
        let code_lengths_capacity = ALPHABET_SIZE
            .iter()
            .map(|&size| usize::from(size))
            .sum::<usize>()
            + color_cache
                .as_ref()
                .map(|cache| 1usize << cache.color_cache_bits)
                .unwrap_or(0);
        let mut code_lengths_arena = Vec::with_capacity(code_lengths_capacity);

        for _i in 0..num_huff_groups {
            code_lengths_arena.clear();
            let mut specs: [Option<HuffmanCodeSpec>; HUFFMAN_CODES_PER_META_CODE] =
                [None, None, None, None, None];
            for (j, &base_alphabet_size) in ALPHABET_SIZE.iter().enumerate() {
                let mut alphabet_size = base_alphabet_size;
                if j == 0 {
                    if let Some(color_cache) = color_cache.as_ref() {
                        alphabet_size += 1 << color_cache.color_cache_bits;
                    }
                }
                specs[j] = Some(
                    self.read_huffman_code_spec(alphabet_size, &mut code_lengths_arena)?,
                );
            }

            let use_wide_root = specs
                .iter()
                .filter_map(Option::as_ref)
                .any(|spec| spec.prefers_wide_root(&code_lengths_arena));
            if use_wide_root {
                let group: HuffmanCodeGroup11 = [
                    specs[0].take().unwrap().build::<11>(&code_lengths_arena)?,
                    specs[1].take().unwrap().build::<11>(&code_lengths_arena)?,
                    specs[2].take().unwrap().build::<11>(&code_lengths_arena)?,
                    specs[3].take().unwrap().build::<11>(&code_lengths_arena)?,
                    specs[4].take().unwrap().build::<11>(&code_lengths_arena)?,
                ];
                hufftree_groups.push(HuffmanCodeGroup::Wide(group));
            } else {
                let group: HuffmanCodeGroup9 = [
                    specs[0].take().unwrap().build::<9>(&code_lengths_arena)?,
                    specs[1].take().unwrap().build::<9>(&code_lengths_arena)?,
                    specs[2].take().unwrap().build::<9>(&code_lengths_arena)?,
                    specs[3].take().unwrap().build::<9>(&code_lengths_arena)?,
                    specs[4].take().unwrap().build::<9>(&code_lengths_arena)?,
                ];
                hufftree_groups.push(HuffmanCodeGroup::Normal(group));
            }
        }
'''

READ_SPEC=r'''    /// Parses a final-image Huffman tree before choosing a group root width.
    fn read_huffman_code_spec(
        &mut self,
        alphabet_size: u16,
        code_lengths_arena: &mut Vec<u16>,
    ) -> Result<HuffmanCodeSpec, DecodingError> {
        let simple = self.bit_reader.read_bits::<u8>(1)? == 1;
        if simple {
            let num_symbols = self.bit_reader.read_bits::<u8>(1)? + 1;
            let is_first_8bits = self.bit_reader.read_bits::<u8>(1)?;
            let zero_symbol = self.bit_reader.read_bits::<u16>(1 + 7 * is_first_8bits)?;
            if zero_symbol >= alphabet_size {
                return Err(DecodingError::BitStreamError);
            }
            if num_symbols == 1 {
                Ok(HuffmanCodeSpec::Single(zero_symbol))
            } else {
                let one_symbol = self.bit_reader.read_bits::<u16>(8)?;
                if one_symbol >= alphabet_size {
                    return Err(DecodingError::BitStreamError);
                }
                Ok(HuffmanCodeSpec::Two(zero_symbol, one_symbol))
            }
        } else {
            let mut code_length_code_lengths = vec![0; CODE_LENGTH_CODES];
            let num_code_lengths = 4 + self.bit_reader.read_bits::<usize>(4)?;
            for i in 0..num_code_lengths {
                code_length_code_lengths[CODE_LENGTH_CODE_ORDER[i]] =
                    self.bit_reader.read_bits(3)?;
            }
            let (start, len) = self.read_huffman_code_lengths(
                code_length_code_lengths,
                alphabet_size,
                code_lengths_arena,
            )?;
            Ok(HuffmanCodeSpec::Implicit { start, len })
        }
    }

'''

READ_LENGTHS=r'''    /// Reads huffman code lengths
    fn read_huffman_code_lengths(
        &mut self,
        code_length_code_lengths: Vec<u16>,
        num_symbols: u16,
        code_lengths: &mut Vec<u16>,
    ) -> Result<(usize, usize), DecodingError> {
        let table = HuffmanTree9::build_implicit(code_length_code_lengths)?;

        let mut max_symbol = if self.bit_reader.read_bits::<u8>(1)? == 1 {
            let length_nbits = 2 + 2 * self.bit_reader.read_bits::<u8>(3)?;
            let max_minus_two = self.bit_reader.read_bits::<u16>(length_nbits)?;
            if max_minus_two > num_symbols - 2 {
                return Err(DecodingError::BitStreamError);
            }
            2 + max_minus_two
        } else {
            num_symbols
        };

        let start = code_lengths.len();
        let len = usize::from(num_symbols);
        code_lengths.resize(start + len, 0);
        let mut prev_code_len = 8;

        let mut symbol = 0;
        while symbol < num_symbols {
            if max_symbol == 0 {
                break;
            }
            max_symbol -= 1;

            self.bit_reader.fill()?;
            let code_len = table.read_symbol(&mut self.bit_reader)?;

            if code_len < 16 {
                code_lengths[start + usize::from(symbol)] = code_len;
                symbol += 1;
                if code_len != 0 {
                    prev_code_len = code_len;
                }
            } else {
                let use_prev = code_len == 16;
                let slot = code_len - 16;
                let extra_bits = match slot {
                    0 => 2,
                    1 => 3,
                    2 => 7,
                    _ => return Err(DecodingError::BitStreamError),
                };
                let repeat_offset = match slot {
                    0 | 1 => 3,
                    2 => 11,
                    _ => return Err(DecodingError::BitStreamError),
                };

                let mut repeat = self.bit_reader.read_bits::<u16>(extra_bits)? + repeat_offset;
                if symbol + repeat > num_symbols {
                    return Err(DecodingError::BitStreamError);
                }
                let length = if use_prev { prev_code_len } else { 0 };
                while repeat > 0 {
                    repeat -= 1;
                    code_lengths[start + usize::from(symbol)] = length;
                    symbol += 1;
                }
            }
        }

        Ok((start, len))
    }

'''

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

def patch(root,variant):
    hp=root/'src/lossless/decoder/huffman.rs';mp=root/'src/lossless/decoder/mod.rs'
    h=hp.read_text();m=mp.read_text()
    old='pub(crate) fn build_implicit(code_lengths: Vec<u16>) -> Result<Self, DecodingError> {'
    assert old in h
    h=h.replace(old,'pub(crate) fn build_implicit(code_lengths: impl AsRef<[u16]>) -> Result<Self, DecodingError> {\n        let code_lengths = code_lengths.as_ref();',1)

    a=m.index('#[derive(Debug)]\nenum HuffmanCodeSpec')
    b=m.index('const ALPHABET_SIZE:',a)
    m=m[:a]+SPEC+m[b:]

    a=m.index('        let mut hufftree_groups = Vec::new();')
    b=m.index('\n        let info = HuffmanInfo {',a)
    m=m[:a]+(GROUP_FIXED if variant=='arena-fixed' else GROUP_ARENA)+m[b:]

    a=m.index('    /// Parses a final-image Huffman tree before choosing a group root width.')
    b=m.index('    /// Reads huffman code lengths',a)
    m=m[:a]+READ_SPEC+m[b:]
    a=m.index('    /// Reads huffman code lengths')
    b=m.index('    /// Decodes the image data using the huffman trees',a)
    m=m[:a]+READ_LENGTHS+m[b:]
    hp.write_text(h);mp.write_text(m)

def invoke(exe,mode,n,files):
    return run(['taskset','-c','0',str(exe),mode,str(n),*map(str,files)],cap=True)

def main():
    if TMP.exists():shutil.rmtree(TMP)
    TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
    for v in VS:
        r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
        if v!='base':
            patch(r,v);run(['cargo','fmt'],cwd=r)
            for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
        (r/'examples').mkdir(exist_ok=True);(r/'examples/clarena.rs').write_text(BENCH);run(['cargo','build','--release','--example','clarena','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/clarena'
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
    cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
    lines=['# VP8L code-length arena current-final matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
    for name,rows in results.items():
        for v in VS[1:]:
            q=[z['base']/z[v] for z in rows]
            lines.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
    Path('benchmark-vp8l-code-length-arena-current.md').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))

if __name__=='__main__':main()
