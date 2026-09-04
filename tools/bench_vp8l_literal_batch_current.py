#!/usr/bin/env python3
import os,shutil,statistics,subprocess
from pathlib import Path
BASE='4f322d44fb38747659451db3d7f1dac7ff8ff21f';TMP=Path('/tmp/vp8l-literal-batch-current');VS=('base','rgb','rgba')
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
PEEK=r'''    pub(crate) fn peek_symbol_bits(&self, v: u64) -> Option<(u8, u16)> {
        match &self.0 {
            HuffmanTreeInner::Tree { primary_table, table_mask, .. } => {
                let entry = primary_table[(v as u16 & table_mask) as usize];
                if (entry >> 12) <= TABLE_BITS as u16 {
                    Some(((entry >> 12) as u8, entry & 0xfff))
                } else {
                    None
                }
            }
            HuffmanTreeInner::Single(symbol) => Some((0, *symbol)),
        }
    }

'''
RGB_OLD=r'''            if code < 256 {
                let green = code as u8;
                let red = tree[RED].read_symbol(&mut self.bit_reader)? as u8;
                let blue = tree[BLUE].read_symbol(&mut self.bit_reader)? as u8;
                if self.bit_reader.nbits < 15 {
                    self.bit_reader.fill()?;
                }
                let alpha = tree[ALPHA].read_symbol(&mut self.bit_reader)? as u8;

                data[*index * 4] = red;
                data[*index * 4 + 1] = green;
                data[*index * 4 + 2] = blue;
                data[*index * 4 + 3] = alpha;

                if let Some(color_cache) = color_cache.as_mut() {
                    color_cache.insert([red, green, blue, alpha]);
                }
                *index += 1;
'''
RGB_NEW=r'''            if code < 256 {
                let green = code as u8;
                let bits = self.bit_reader.peek_full();
                let fast = tree[RED].peek_symbol_bits(bits).and_then(|(rb, red)| {
                    tree[BLUE].peek_symbol_bits(bits >> rb).and_then(|(bb, blue)| {
                        tree[ALPHA].peek_symbol_bits(bits >> (rb + bb)).and_then(|(ab, alpha)| {
                            let total = rb + bb + ab;
                            (total <= self.bit_reader.nbits).then_some((total, red as u8, blue as u8, alpha as u8))
                        })
                    })
                });
                let (red, blue, alpha) = if let Some((total, red, blue, alpha)) = fast {
                    self.bit_reader.consume(total)?;
                    (red, blue, alpha)
                } else {
                    let red = tree[RED].read_symbol(&mut self.bit_reader)? as u8;
                    let blue = tree[BLUE].read_symbol(&mut self.bit_reader)? as u8;
                    if self.bit_reader.nbits < 15 { self.bit_reader.fill()?; }
                    let alpha = tree[ALPHA].read_symbol(&mut self.bit_reader)? as u8;
                    (red, blue, alpha)
                };

                data[*index * 4] = red;
                data[*index * 4 + 1] = green;
                data[*index * 4 + 2] = blue;
                data[*index * 4 + 3] = alpha;

                if let Some(color_cache) = color_cache.as_mut() {
                    color_cache.insert([red, green, blue, alpha]);
                }
                *index += 1;
'''
RGBA_INSERT=r'''            let packed_bits = self.bit_reader.peek_full();
            if let Some((gb, green)) = tree[GREEN].peek_symbol_bits(packed_bits) {
                if green < 256 {
                    if let Some((rb, red)) = tree[RED].peek_symbol_bits(packed_bits >> gb) {
                        if let Some((bb, blue)) = tree[BLUE].peek_symbol_bits(packed_bits >> (gb + rb)) {
                            if let Some((ab, alpha)) = tree[ALPHA].peek_symbol_bits(packed_bits >> (gb + rb + bb)) {
                                let total = gb + rb + bb + ab;
                                if total <= self.bit_reader.nbits {
                                    self.bit_reader.consume(total)?;
                                    let value = [red as u8, green as u8, blue as u8, alpha as u8];
                                    data[*index * 4..][..4].copy_from_slice(&value);
                                    if let Some(color_cache) = color_cache.as_mut() { color_cache.insert(value); }
                                    *index += 1;
                                    continue;
                                }
                            }
                        }
                    }
                }
            }
'''
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(p):
 d=p.read_bytes();o=[];q=12
 if len(d)<12 or d[:4]!=b'RIFF'or d[8:12]!=b'WEBP':return o
 while q+8<=len(d):t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
 return o
def patch(r,v):
 hp=r/'src/lossless/decoder/huffman.rs';h=hp.read_text();anchor='    /// Peek at the next symbol in the bitstream';i=h.index(anchor);h=h[:i]+PEEK+h[i:];hp.write_text(h)
 mp=r/'src/lossless/decoder/mod.rs';m=mp.read_text()
 if v=='rgb':
  assert RGB_OLD in m;m=m.replace(RGB_OLD,RGB_NEW,1)
 else:
  needle='''        while *index < num_values && *index < block_end {\n            self.bit_reader.fill()?;\n            let code = tree[GREEN].read_symbol(&mut self.bit_reader)?;\n''';repl='''        while *index < num_values && *index < block_end {\n            self.bit_reader.fill()?;\n'''+RGBA_INSERT+'''            let code = tree[GREEN].read_symbol(&mut self.bit_reader)?;\n''';assert needle in m;m=m.replace(needle,repl,1)
 mp.write_text(m)
def inv(e,m,n,ps):return run(['taskset','-c','0',str(e),m,str(n),*map(str,ps)],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={};env=os.environ.copy();env['RUSTFLAGS']='-C target-cpu=native'
 for v in VS:
  r=TMP/v;roots[v]=r;run(['git','worktree','add','--detach',str(r),BASE])
  if v!='base':
   patch(r,v);run(['cargo','fmt'],cwd=r)
   for c in (['cargo','test','-q'],['cargo','test','--release','-q'],['cargo','doc','--no-deps','-q'],['cargo','clippy','--','-D','warnings'],['cargo','fmt','--','--check'],['cargo','+1.80.1','build','-q'],['cargo','+1.80.1','build','--release','-q']):run(c,cwd=r)
  (r/'examples').mkdir(exist_ok=True);(r/'examples/litbatch.rs').write_text(BENCH);run(['cargo','build','--release','--example','litbatch','-q'],cwd=r,env=env);exes[v]=r/'target/release/examples/litbatch'
 rels=[p.relative_to(roots['base'])for p in sorted((roots['base']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
 ppm=TMP/'large.ppm';w=h=2048
 with ppm.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):i=x*3;row[i]=(x*3+y*5+((x>>5)^(y>>4))*17)&255;row[i+1]=(x*2+y*7+((x*y)>>10))&255;row[i+2]=(x*11+y*3+((x+y)>>3)*9)&255
   f.write(row)
 large=TMP/'large.webp';run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(large)])
 corpus={v:[roots[v]/x for x in rels]for v in VS};bh=inv(exes['base'],'h',1,corpus['base']+[large])
 for v in VS[1:]:assert bh==inv(exes[v],'h',1,corpus[v]+[large])
 results={}
 for name,files,it in [('corpus',corpus,70),('large',{v:[large]for v in VS},4)]:
  rows=[]
  for n in range(17):
   order=VS if n%2==0 else tuple(reversed(VS));z={}
   for v in order:z[v]=float(inv(exes[v],'t',it,files[v]))
   rows.append(z)
  results[name]=rows
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True);L=['# VP8L batched literal Huffman current-tree matrix','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- primary-table peeks decode multiple literal channels with one bit consume; hashes + full verification passed','','| workload | candidate | paired median | positive | range |','|---|---|---:|---:|---:|']
 for name,rows in results.items():
  for v in VS[1:]:q=[z['base']/z[v]for z in rows];L.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-literal-batch-current.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
