#!/usr/bin/env python3
import csv, os, shutil, statistics, subprocess
from pathlib import Path
BASE='509d11c2bf102929ded4be05d3c54b06032fdc44'; TMP=Path('/tmp/vp8l-meta-run-coalesce')
def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)
def chunks(d):
 if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP':return[]
 out=[];p=12
 while p+8<=len(d):f=d[p:p+4];n=int.from_bytes(d[p+4:p+8],'little');out.append(f);p+=8+n+(n&1)
 return out
def patch(root):
 p=root/'src/lossless/decoder/mod.rs';s=p.read_text()
 old='''                    let x = index % usize::from(width);\n                    let y = index / usize::from(width);\n                    next_block_start = (x | usize::from(huffman_info.mask))\n                        .min(usize::from(width - 1))\n                        + y * usize::from(width)\n                        + 1;\n                    huffman_info.get_huff_index(x as u16, y as u16)\n'''
 new='''                    let width = usize::from(width);\n                    let x = index % width;\n                    let y = index / width;\n                    let block_x = x >> huffman_info.bits;\n                    let block_y = y >> huffman_info.bits;\n                    let huff_xsize = usize::from(huffman_info.xsize);\n                    let row_start = block_y * huff_xsize;\n                    let huff_index = usize::from(huffman_info.image[row_start + block_x]);\n                    let mut run_end = block_x + 1;\n                    while run_end < huff_xsize\n                        && usize::from(huffman_info.image[row_start + run_end]) == huff_index\n                    {\n                        run_end += 1;\n                    }\n                    next_block_start = (y * width + (run_end << huffman_info.bits).min(width))\n                        .min(num_values);\n                    huff_index\n'''
 if old not in s:raise SystemExit('dispatch marker missing')
 s=s.replace(old,new,1)
 s=s.replace('''    mask: u16,\n''','',1)
 s=s.replace('''            mask: huffman_mask,\n''','',1)
 s=s.replace('''        let huffman_mask = if huffman_bits == 0 {\n            !0\n        } else {\n            (1 << huffman_bits) - 1\n        };\n\n''','',1)
 p.write_text(s)
def prep(name):
 r=TMP/name;run(['git','worktree','add','--detach',str(r),BASE])
 if name=='cand':patch(r);run(['cargo','fmt'],cwd=r);run(['cargo','test','-q'],cwd=r);run(['cargo','doc','-q'],cwd=r);run(['cargo','clippy','--all-features','--','-D','warnings'],cwd=r);run(['cargo','fmt','--','--check'],cwd=r);run(['cargo','+1.80.1','build','-q'],cwd=r)
 return r
def make_ppm(path,w,h,kind):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode());row=bytearray(w*3)
  for y in range(h):
   for x in range(w):
    i=x*3
    if kind=='structured': a=(x*5+y*3+((x>>4)^(y>>3))*29)&255;b=(x*13+y*7+((x*y)>>8))&255;c=(x*2+y*17+((x+y)>>2)*11)&255
    elif kind=='tiles': q=((x>>5)+3*(y>>5))&15;a=(q*17)&255;b=((q*53)+(x&31)*3)&255;c=((q*91)+(y&31)*5)&255
    else: z=(x*1103515245+y*12345+((x*y)*2654435761))&0xffffffff;a=(z>>8)&255;b=(z>>16)&255;c=(z>>24)&255
    row[i:i+3]=bytes((a,b,c))
   f.write(row)
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''
def build(r):
 (r/'examples').mkdir(exist_ok=True);(r/'examples/mrc.rs').write_text(BENCH);e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','mrc','-q'],cwd=r,env=e);return r/'target/release/examples/mrc'
def invoke(b,m,n,ps):return run(['taskset','-c','0',str(b),m,str(n),*[str(p)for p in ps]],cap=True)
def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();base=prep('base');cand=prep('cand');rels=[p.relative_to(base) for p in sorted((base/'tests/images').rglob('*.webp')) if b'VP8L'in chunks(p.read_bytes()) and b'ANIM'not in chunks(p.read_bytes())]
 generated=[]
 for kind in('structured','tiles','noise'):
  ppm=TMP/f'{kind}.ppm';webp=TMP/f'{kind}.webp';make_ppm(ppm,1536,1152,kind);run(['cwebp','-quiet','-lossless','-z','9',str(ppm),'-o',str(webp)]);generated.append(webp)
 bb=build(base);cb=build(cand);bf=[base/r for r in rels];cf=[cand/r for r in rels]
 if invoke(bb,'h',1,bf+generated)!=invoke(cb,'h',1,cf+generated):raise SystemExit('hash mismatch')
 multi_names={'1_webp_ll.webp','2_webp_ll.webp','3_webp_ll.webp','4_webp_ll.webp','5_webp_ll.webp','lossless_indexed_4bit_palette.webp'}
 bm=[p for p in bf if p.name in multi_names];cm=[p for p in cf if p.name in multi_names]
 workloads={'corpus':(bf,cf,80),'multi':(bm,cm,100),'structured':([generated[0]],[generated[0]],18),'tiles':([generated[1]],[generated[1]],20),'noise':([generated[2]],[generated[2]],12)}
 rows=[]
 for rnd in range(1,16):
  order=('base','cand') if rnd%2 else ('cand','base')
  for w,(bps,cps,n) in workloads.items():
   for v in order:
    b=bb if v=='base' else cb;ps=bps if v=='base' else cps
    rows.append((w,rnd,v,float(invoke(b,'t',n,ps))))
 groups={};pairs={}
 for w,r,v,x in rows:groups.setdefault((w,v),[]).append(x);pairs.setdefault((w,r),{})[v]=x
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
 L=['# VP8L meta-Huffman run coalescing','',f'- baseline: `{BASE}`',f'- CPU: `{cpu}`','- horizontal identical entropy groups are coalesced; 15 alternating paired rounds','- hashes + tests/docs/Clippy/fmt/MSRV passed','','| workload | baseline | candidate | paired median | positive | range |','|---|---:|---:|---:|---:|---:|']
 for w in workloads:
  q=[z['base']/z['cand'] for (ww,_),z in sorted(pairs.items()) if ww==w];L.append(f'| {w} | {statistics.median(groups[w,"base"]):.3f} us | {statistics.median(groups[w,"cand"]):.3f} us | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
 Path('benchmark-vp8l-meta-run-coalesce.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
