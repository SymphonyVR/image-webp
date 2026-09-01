#!/usr/bin/env python3
import math, os, shutil, statistics, subprocess
from pathlib import Path

BASE='4cd194935d100a09acf24eb24d8c1343c7844844'
TMP=Path('/tmp/vp8l-adaptive-root-final')
VARIANTS=[
 ('r9',None),
 ('dyn9','9u8'),
 ('m15r11','if max_length >= 15 { 11 } else { 9 }'),
 ('m14r11','if max_length >= 14 { 11 } else { 9 }'),
 ('m13r11','if max_length >= 13 { 11 } else { 9 }'),
 ('m14r10','if max_length >= 14 { 10 } else { 9 }'),
 ('q25r11','if max_length >= 13 && num_symbols >= 128 && long_symbols * 4 >= num_symbols { 11 } else { 9 }'),
 ('q50r11','if max_length >= 13 && num_symbols >= 128 && long_symbols * 2 >= num_symbols { 11 } else { 9 }'),
]
BENCH=r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn one(d:&[u8])->u64{let mut q=WebPDecoder::new(Cursor::new(d)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();let mut h=0xcbf29ce484222325u64;for &z in&b{h=(h^z as u64).wrapping_mul(1099511628211)}black_box(h)}fn main(){let a:Vec<_>=std::env::args().skip(1).collect();let m=&a[0];let n:usize=a[1].parse().unwrap();let ds:Vec<Vec<u8>>=a[2..].iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for d in&ds{println!("{:016x}",one(d))}return}for d in&ds{black_box(one(d));}let t=Instant::now();for _ in 0..n{for d in&ds{black_box(one(d));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''

def run(c,cwd=None,cap=False,env=None):
 print('+',' '.join(map(str,c)),flush=True)
 if cap:return subprocess.check_output(c,cwd=cwd,text=True,env=env).strip()
 subprocess.run(c,cwd=cwd,check=True,env=env)

def chunks(p):
 d=p.read_bytes();o=[]
 if len(d)<12 or d[:4]!=b'RIFF' or d[8:12]!=b'WEBP':return o
 q=12
 while q+8<=len(d):t=d[q:q+4];n=int.from_bytes(d[q+4:q+8],'little');o.append(t);q+=8+n+(n&1)
 return o

def ppm(path,w,h,k):
 with path.open('wb')as f:
  f.write(f'P6\n{w} {h}\n255\n'.encode())
  for y in range(h):
   row=bytearray()
   for x in range(w):
    if k=='gradient':r=x*255//max(1,w-1);g=y*255//max(1,h-1);b=(x+y)*255//max(1,w+h-2)
    elif k=='corr':g=(x*7+y*11+((x*y)>>7))&255;r=(g+((x>>3)&15))&255;b=(g-((y>>3)&15))&255
    elif k=='color':r=(x*11+y*3)&255;g=(x*5+y*13)&255;b=(r+g*3)&255
    elif k=='structured':q=((x>>5)+3*(y>>5))&15;r=q*17;g=(q*53+(x&31)*3)&255;b=(q*91+(y&31)*5)&255
    else:z=(x*1103515245+y*12345+(x*y)*2654435761+0x9e3779b9)&0xffffffff;r=(z>>8)&255;g=(z>>16)&255;b=(z>>24)&255
    row+=bytes((r,g,b))
   f.write(row)

def patch_dynamic(root,selector):
 p=root/'src/lossless/decoder/huffman.rs';s=p.read_text()
 reps=[
 ('    Tree {\n        table_mask: u16,\n        primary_table: Vec<u16>,\n        secondary_table: Vec<u16>,\n    },','    Tree {\n        table_bits: u8,\n        table_mask: u16,\n        primary_table: Vec<u16>,\n        secondary_table: Vec<u16>,\n    },'),
 ('        let table_bits = (max_length as u16).min(u16::from(MAX_TABLE_BITS));','        let long_symbols: usize = histogram[10..=MAX_ALLOWED_CODE_LENGTH].iter().sum();\n        let max_table_bits: u8 = '+selector+';\n        let table_bits = (max_length as u16).min(u16::from(max_table_bits));'),
 ('        Ok(Self(HuffmanTreeInner::Tree {\n            table_mask,','        Ok(Self(HuffmanTreeInner::Tree {\n            table_bits: table_bits as u8,\n            table_mask,'),
 ('        Self(HuffmanTreeInner::Tree {\n            primary_table: vec![(1 << 12) | zero, (1 << 12) | one],','        Self(HuffmanTreeInner::Tree {\n            table_bits: 1,\n            primary_table: vec![(1 << 12) | zero, (1 << 12) | one],'),
 ('        primary_table_entry: u16,\n        bit_reader: &mut BitReader<R>,','        primary_table_entry: u16,\n        table_bits: u8,\n        bit_reader: &mut BitReader<R>,'),
 ('        let mask = (1 << (length - MAX_TABLE_BITS as u16)) - 1;','        let mask = (1 << (length - u16::from(table_bits))) - 1;'),
 ('            + ((v >> MAX_TABLE_BITS) as usize & mask as usize);','            + ((v >> table_bits) as usize & mask as usize);'),
 ('                primary_table,\n                secondary_table,\n                table_mask,','                primary_table,\n                secondary_table,\n                table_mask,\n                table_bits,'),
 ('                if (entry >> 12) <= MAX_TABLE_BITS as u16 {','                if (entry >> 12) <= u16::from(*table_bits) {'),
 ('                Self::read_symbol_slowpath(secondary_table, v, entry, bit_reader)','                Self::read_symbol_slowpath(secondary_table, v, entry, *table_bits, bit_reader)'),
 ('                primary_table,\n                table_mask,\n                ..','                primary_table,\n                table_mask,\n                table_bits,\n                ..'),
 ]
 for a,b in reps:
  if a not in s:raise SystemExit('patch anchor missing: '+a[:60])
  s=s.replace(a,b,1)
 # second root-width comparison is in peek_symbol after the first replacement above.
 old='                if (entry >> 12) <= MAX_TABLE_BITS as u16 {'
 if old not in s:raise SystemExit('peek comparison anchor missing')
 s=s.replace(old,'                if (entry >> 12) <= u16::from(*table_bits) {',1)
 p.write_text(s)

def prep(name,selector):
 r=TMP/name;run(['git','worktree','add','--detach',str(r),BASE])
 if selector is not None:patch_dynamic(r,selector)
 (r/'examples').mkdir(exist_ok=True);(r/'examples/adaptive_root.rs').write_text(BENCH)
 run(['cargo','fmt'],cwd=r);run(['cargo','test','-q'],cwd=r);run(['cargo','+1.80.1','build','-q'],cwd=r)
 e=os.environ.copy();e['RUSTFLAGS']='-C target-cpu=native';run(['cargo','build','--release','--example','adaptive_root','-q'],cwd=r,env=e)
 return r,r/'target/release/examples/adaptive_root'

def invoke(exe,m,n,ps):return run(['taskset','-c','0',str(exe),m,str(n),*[str(x)for x in ps]],cap=True)

def main():
 if TMP.exists():shutil.rmtree(TMP)
 TMP.mkdir();roots={};exes={}
 for n,s in VARIANTS:roots[n],exes[n]=prep(n,s)
 generated={}
 for k in ('structured','gradient','corr','color','noise'):
  src=TMP/f'{k}.ppm';ppm(src,1536,1536,k)
  for z in(0,9):
   w=TMP/f'{k}-z{z}.webp';run(['cwebp','-quiet','-lossless','-z',str(z),str(src),'-o',str(w)]);generated[f'{k}-z{z}']=w
 rels=[p.relative_to(roots['r9'])for p in sorted((roots['r9']/'tests/images').rglob('*.webp'))if b'VP8L'in chunks(p)and b'ANIM'not in chunks(p)]
 h0={label:invoke(exes['r9'],'h',1,[p]) for label,p in generated.items()}
 for n,_ in VARIANTS:
  for label,p in generated.items():
   if invoke(exes[n],'h',1,[p])!=h0[label]:raise SystemExit(f'hash mismatch {n} {label}')
  ps=[roots[n]/r for r in rels]
  if invoke(exes[n],'h',1,ps)!=invoke(exes['r9'],'h',1,[roots['r9']/r for r in rels]):raise SystemExit('corpus hash mismatch '+n)
 workloads={
  'corpus':('repo',70),
  'z0':([generated[f'{k}-z0']for k in ('structured','gradient','corr','color','noise')],5),
  'z9':([generated[f'{k}-z9']for k in ('structured','gradient','corr','color','noise')],5),
  'noise-z0':([generated['noise-z0']],4),'noise-z9':([generated['noise-z9']],4),
  'corr-z9':([generated['corr-z9']],5),'structured-z9':([generated['structured-z9']],5),
 }
 rows=[];names=[n for n,_ in VARIANTS]
 for rnd in range(11):
  order=names if rnd%2==0 else list(reversed(names))
  for w,(items,iters) in workloads.items():
   for n in order:
    ps=[roots[n]/r for r in rels] if items=='repo' else items
    rows.append((w,rnd,n,float(invoke(exes[n],'t',iters,ps))))
 vals={};pairs={}
 for w,r,n,x in rows:vals.setdefault((w,n),[]).append(x);pairs.setdefault((w,r),{})[n]=x
 cpu=run(['bash','-lc',"lscpu|sed -n 's/^Model name:[[:space:]]*//p'"],cap=True)
 L=['# VP8L adaptive Huffman root matrix','',f'- base: `{BASE}`',f'- CPU: `{cpu}`','- 11 alternating/reversed paired rounds; hashes/tests/MSRV passed','- `dyn9` measures the cost of storing/reading a per-tree root width while always selecting 9 bits.','', '| workload | variant | median us | speedup vs r9 | positive rounds |','|---|---|---:|---:|---:|']
 for w in workloads:
  for n in names:
   q=[z['r9']/z[n]for(ww,_),z in sorted(pairs.items())if ww==w];L.append(f'| {w} | {n} | {statistics.median(vals[w,n]):.3f} | {statistics.median(q):.4f}x | {sum(x>1 for x in q)}/{len(q)} |')
 L+=['','## Selectors','']+[f'- `{n}`: `{s or "unmodified static 9"}`'for n,s in VARIANTS]
 Path('benchmark-vp8l-adaptive-root-final.md').write_text('\n'.join(L)+'\n');print('\n'.join(L))
if __name__=='__main__':main()
