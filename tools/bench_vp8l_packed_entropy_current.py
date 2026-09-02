#!/usr/bin/env python3
import os, shutil, statistics, subprocess
from pathlib import Path

BASE='84d8d20753fce0a9972e8a244fdf929b5a55671c'
TMP=Path('/tmp/vp8l-packed-entropy-current')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''

NEW=r'''    /// Decodes image entropy into pixel-sized lanes, then emits the byte buffer once.
    fn decode_image_data(
        &mut self,
        width: u16,
        height: u16,
        mut huffman_info: HuffmanInfo,
        data: &mut [u8],
    ) -> Result<(), DecodingError> {
        let num_values = usize::from(width) * usize::from(height);
        let width_usize = usize::from(width);
        let mut pixels = vec![[0u8; 4]; num_values];
        let mut index = 0usize;

        while index < num_values {
            let (huff_index, block_end) = if huffman_info.bits == 0 {
                (0usize, num_values)
            } else {
                let y = index / width_usize;
                let x = index - y * width_usize;
                let meta_width = usize::from(huffman_info.xsize);
                let meta_x = x >> huffman_info.bits;
                let meta_y = y >> huffman_info.bits;
                let pos = meta_y * meta_width + meta_x;
                let huff_index = usize::from(huffman_info.image[pos]);
                let row_end = (meta_y + 1) * meta_width;
                let mut end_pos = pos + 1;
                while end_pos < row_end && usize::from(huffman_info.image[end_pos]) == huff_index {
                    end_pos += 1;
                }
                let run_end_meta = end_pos - meta_y * meta_width;
                let run_end_x = (run_end_meta << huffman_info.bits).min(width_usize);
                (huff_index, y * width_usize + run_end_x)
            };

            let groups = &huffman_info.huffman_code_groups;
            let color_cache = &mut huffman_info.color_cache;
            match &groups[huff_index] {
                HuffmanCodeGroup::Normal(tree) => self.decode_image_data_block::<9>(
                    width,
                    &mut pixels,
                    tree,
                    color_cache,
                    &mut index,
                    block_end,
                )?,
                HuffmanCodeGroup::Wide(tree) => self.decode_image_data_block::<11>(
                    width,
                    &mut pixels,
                    tree,
                    color_cache,
                    &mut index,
                    block_end,
                )?,
            }
        }

        for (dst, pixel) in data.chunks_exact_mut(4).zip(pixels) {
            dst.copy_from_slice(&pixel);
        }
        Ok(())
    }

    #[inline]
    fn decode_image_data_block<const TABLE_BITS: u8>(
        &mut self,
        width: u16,
        data: &mut [[u8; 4]],
        tree: &[HuffmanTree<TABLE_BITS>; HUFFMAN_CODES_PER_META_CODE],
        color_cache: &mut Option<ColorCache>,
        index: &mut usize,
        block_end: usize,
    ) -> Result<(), DecodingError> {
        let num_values = data.len();
        debug_assert!(*index < block_end);

        if tree[..4].iter().all(|t| t.is_single_node()) {
            self.bit_reader.fill()?;
            let code = tree[GREEN].read_symbol(&mut self.bit_reader)?;
            if code < 256 {
                let n = block_end - *index;
                let red = tree[RED].read_symbol(&mut self.bit_reader)?;
                let blue = tree[BLUE].read_symbol(&mut self.bit_reader)?;
                let alpha = tree[ALPHA].read_symbol(&mut self.bit_reader)?;
                let value = [red as u8, code as u8, blue as u8, alpha as u8];
                data[*index..*index + n].fill(value);
                if let Some(color_cache) = color_cache.as_mut() {
                    color_cache.insert(value);
                }
                *index += n;
                return Ok(());
            }
        }

        while *index < num_values && *index < block_end {
            self.bit_reader.fill()?;
            let code = tree[GREEN].read_symbol(&mut self.bit_reader)?;

            if code < 256 {
                let green = code as u8;
                let red = tree[RED].read_symbol(&mut self.bit_reader)? as u8;
                let blue = tree[BLUE].read_symbol(&mut self.bit_reader)? as u8;
                if self.bit_reader.nbits < 15 {
                    self.bit_reader.fill()?;
                }
                let alpha = tree[ALPHA].read_symbol(&mut self.bit_reader)? as u8;
                let value = [red, green, blue, alpha];
                data[*index] = value;
                if let Some(color_cache) = color_cache.as_mut() {
                    color_cache.insert(value);
                }
                *index += 1;
            } else if code < 256 + 24 {
                let length_symbol = code - 256;
                let length = Self::get_copy_distance(&mut self.bit_reader, length_symbol)?;
                let dist_symbol = tree[DIST].read_symbol(&mut self.bit_reader)?;
                let dist_code = Self::get_copy_distance(&mut self.bit_reader, dist_symbol)?;
                let dist = Self::plane_code_to_distance(width, dist_code);

                if *index < dist || num_values - *index < length {
                    return Err(DecodingError::BitStreamError);
                }

                if dist == 1 {
                    let value = data[*index - 1];
                    data[*index..*index + length].fill(value);
                } else {
                    if *index + length + 3 <= num_values {
                        let start = *index - dist;
                        data.copy_within(start..start + 4, *index);
                        if length > 4 || dist < 4 {
                            for i in (0..length).step_by(dist.min(4)).skip(1) {
                                data.copy_within(start + i..start + i + 4, *index + i);
                            }
                        }
                    } else {
                        for i in 0..length {
                            data[*index + i] = data[*index + i - dist];
                        }
                    }

                    if let Some(color_cache) = color_cache.as_mut() {
                        let cache_pixels = length.min(dist);
                        let cache_start = *index + length - cache_pixels;
                        for &pixel in &data[cache_start..cache_start + cache_pixels] {
                            color_cache.insert(pixel);
                        }
                    }
                }
                *index += length;
            } else {
                let color_cache = color_cache.as_mut().ok_or(DecodingError::BitStreamError)?;
                data[*index] = color_cache.lookup((code - 280).into());
                *index += 1;

                if *index < block_end {
                    if let Some((bits, code)) = tree[GREEN].peek_symbol(&self.bit_reader) {
                        if code >= 280 {
                            self.bit_reader.consume(bits)?;
                            data[*index] = color_cache.lookup((code - 280).into());
                            *index += 1;
                        }
                    }
                }
            }
        }

        Ok(())
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

def invoke(exe,mode,n,files):return run(['taskset','-c','0',str(exe),mode,str(n),*map(str,files)],cap=True)

def main():
    if TMP.exists():shutil.rmtree(TMP)
    TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
    for v in ('base','cand'):
        r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
        if v=='cand':
            p=r/'src/lossless/decoder/mod.rs';s=p.read_text();a=s.index('    /// Decodes the image data using the huffman trees');b=s.index('    /// Reads color cache data from the bitstream',a);p.write_text(s[:a]+NEW+'\n'+s[b:]);run(['cargo','fmt'],cwd=r)
            for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
        (r/'examples').mkdir(exist_ok=True);(r/'examples/pec.rs').write_text(BENCH);run(['cargo','build','--release','--example','pec','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/pec'
    rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
    w=h=2048
    for kind in ('large','repeat'):
        ppm=TMP/f'{kind}.ppm'
        with ppm.open('wb')as f:
            f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
            for y in range(h):
                for x in range(w):
                    i=x*3
                    if kind=='repeat':
                        q=((x>>4)+(y>>4)*3)&15;c=((q*37)&255,(q*73)&255,(q*109)&255);row[i:i+3]=bytes(c)
                    else:
                        row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
                f.write(row)
        run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(TMP/f'{kind}.webp')])
    corpus={v:[roots[v]/x for x in rels]for v in ('base','cand')};extras=[TMP/'large.webp',TMP/'repeat.webp'];assert invoke(exes['base'],'h',1,corpus['base']+extras)==invoke(exes['cand'],'h',1,corpus['cand']+extras)
    results={}
    for name,files,it in [('corpus',corpus,60),('large',{'base':[extras[0]],'cand':[extras[0]]},3),('repeat',{'base':[extras[1]],'cand':[extras[1]]},3)]:
        q=[]
        for n in range(17):
            order=('base','cand')if n%2==0 else('cand','base');z={}
            for v in order:z[v]=float(invoke(exes[v],'t',it,files[v]))
            q.append(z['base']/z['cand'])
        results[name]=q
    cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L packed entropy-buffer current-tree benchmark','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- safe `[u8; 4]` pixel lanes during entropy/LZ decode, one final byte-buffer copy','- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed','','| workload | paired median | positive | range |','|---|---:|---:|---:|']
    for name,q in results.items():L.append(f'| {name} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
    Path('benchmark-vp8l-packed-entropy-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
