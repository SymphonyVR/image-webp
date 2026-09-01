#!/usr/bin/env python3
import csv, os, shutil, statistics, subprocess
from pathlib import Path

BASE = '0881ec1a66f09e11b766c309cf6e651077775bd9'
TMP = Path('/tmp/vp8l-prefix-current-final')
VARIANTS = ('base', 'table', 'pair')

TABLE_FN = r'''    fn get_copy_distance(
        bit_reader: &mut BitReader<R>,
        prefix_code: u16,
    ) -> Result<usize, DecodingError> {
        const EXTRA: [u8; 40] = [
            0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8,
            9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18,
        ];
        const BASES: [usize; 40] = [
            1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193, 257, 385, 513,
            769, 1025, 1537, 2049, 3073, 4097, 6145, 8193, 12289, 16385, 24577, 32769,
            49153, 65537, 98305, 131073, 196609, 262145, 393217, 524289, 786433,
        ];
        let i = usize::from(prefix_code);
        let extra = EXTRA[i];
        let bits = bit_reader.peek(extra) as usize;
        bit_reader.consume(extra)?;
        Ok(BASES[i] + bits)
    }

'''

PAIR_FN = r'''    fn get_copy_distance(
        bit_reader: &mut BitReader<R>,
        prefix_code: u16,
    ) -> Result<usize, DecodingError> {
        if prefix_code < 4 {
            return Ok(usize::from(prefix_code + 1));
        }
        const EXTRA: [u8; 36] = [
            1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10,
            11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18,
        ];
        const BASES: [usize; 36] = [
            5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193, 257, 385, 513, 769, 1025,
            1537, 2049, 3073, 4097, 6145, 8193, 12289, 16385, 24577, 32769, 49153,
            65537, 98305, 131073, 196609, 262145, 393217, 524289, 786433,
        ];
        let i = usize::from(prefix_code - 4);
        let extra = EXTRA[i];
        let bits = bit_reader.peek(extra) as usize;
        bit_reader.consume(extra)?;
        Ok(BASES[i] + bits)
    }

'''

BENCH = r'''use image_webp::WebPDecoder;
use std::{hint::black_box, io::Cursor, time::Instant};
fn decode(x: &[u8]) -> Vec<u8> {
    let mut q = WebPDecoder::new(Cursor::new(x)).unwrap();
    let mut b = vec![0; q.output_buffer_size().unwrap()];
    q.read_image(&mut b).unwrap();
    b
}
fn hash(x: &[u8]) -> u64 {
    decode(x).iter().fold(0xcbf29ce484222325u64, |a, &z| (a ^ z as u64).wrapping_mul(1099511628211))
}
fn main() {
    let mut a = std::env::args().skip(1);
    let mode = a.next().unwrap();
    let n: usize = a.next().unwrap().parse().unwrap();
    let paths: Vec<_> = a.collect();
    let data: Vec<Vec<u8>> = paths.iter().map(std::fs::read).collect::<Result<_, _>>().unwrap();
    if mode == "h" {
        for x in &data { println!("{:016x}", hash(x)); }
        return;
    }
    for x in &data { black_box(decode(x)); }
    let t = Instant::now();
    for _ in 0..n { for x in &data { black_box(decode(x)); } }
    println!("{:.3}", t.elapsed().as_secs_f64() * 1e6 / (n * data.len()) as f64);
}
'''

def run(cmd, cwd=None, capture=False, env=None):
    print('+', ' '.join(map(str, cmd)), flush=True)
    if capture:
        return subprocess.check_output(cmd, cwd=cwd, text=True, env=env).strip()
    subprocess.run(cmd, cwd=cwd, check=True, env=env)

def chunks(path):
    d = path.read_bytes(); out = []; p = 12
    if len(d) < 12 or d[:4] != b'RIFF' or d[8:12] != b'WEBP': return out
    while p + 8 <= len(d):
        tag = d[p:p+4]; n = int.from_bytes(d[p+4:p+8], 'little'); out.append(tag); p += 8 + n + (n & 1)
    return out

def patch(root, body):
    p = root / 'src/lossless/decoder/mod.rs'; s = p.read_text()
    a = s.index('    fn get_copy_distance('); b = s.index('    /// Gets distance to pixel', a)
    p.write_text(s[:a] + body + s[b:])

def invoke(exe, mode, n, files):
    return run(['taskset', '-c', '0', str(exe), mode, str(n), *map(str, files)], capture=True)

def paired(exes, files, iterations, rounds=17):
    rows = {}
    for r in range(rounds):
        order = VARIANTS if r % 2 == 0 else tuple(reversed(VARIANTS))
        z = {}
        for v in order: z[v] = float(invoke(exes[v], 't', iterations, files[v]))
        rows[r] = z
    return rows

def main():
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir()
    roots = {}; exes = {}; env = os.environ.copy(); env['RUSTFLAGS'] = '-C target-cpu=native'
    for v in VARIANTS:
        root = TMP / v; roots[v] = root
        run(['git', 'worktree', 'add', '--detach', str(root), BASE])
        if v == 'table': patch(root, TABLE_FN)
        elif v == 'pair': patch(root, PAIR_FN)
        if v != 'base':
            run(['cargo', 'fmt'], cwd=root)
            run(['cargo', 'test', '-q'], cwd=root)
            run(['cargo', 'test', '--release', '-q'], cwd=root)
            run(['cargo', 'doc', '--no-deps', '-q'], cwd=root)
            run(['cargo', 'clippy', '--', '-D', 'warnings'], cwd=root)
            run(['cargo', 'fmt', '--', '--check'], cwd=root)
            run(['cargo', '+1.80.1', 'build', '-q'], cwd=root)
        (root / 'examples').mkdir(exist_ok=True)
        (root / 'examples/prefix_current.rs').write_text(BENCH)
        run(['cargo', 'build', '--release', '--example', 'prefix_current', '-q'], cwd=root, env=env)
        exes[v] = root / 'target/release/examples/prefix_current'

    rels = [p.relative_to(roots['base']) for p in sorted((roots['base']/'tests/images').rglob('*.webp')) if b'VP8L' in chunks(p) and b'ANIM' not in chunks(p)]
    large_ppm = TMP / 'large.ppm'; w = h = 2048
    with large_ppm.open('wb') as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode())
        row = bytearray(w * 3)
        for y in range(h):
            for x in range(w):
                i = x * 3
                row[i] = (x*3 + y*5 + ((x>>5) ^ (y>>4))*17) & 255
                row[i+1] = (x*2 + y*7 + ((x*y)>>10)) & 255
                row[i+2] = (x*11 + y*3 + ((x+y)>>3)*9) & 255
            f.write(row)
    large = TMP / 'large.webp'; run(['cwebp', '-quiet', '-lossless', '-z', '9', str(large_ppm), '-o', str(large)])

    corpus = {v: [roots[v]/r for r in rels] for v in VARIANTS}
    for v in ('table', 'pair'):
        assert invoke(exes['base'], 'h', 1, corpus['base'] + [large]) == invoke(exes[v], 'h', 1, corpus[v] + [large])

    workloads = {}
    workloads['corpus'] = paired(exes, corpus, 70)
    same = {v: [large] for v in VARIANTS}
    workloads['large'] = paired(exes, same, 4)
    cpu = run(['bash', '-lc', "lscpu | sed -n 's/^Model name:[[:space:]]*//p'"], capture=True)
    lines = ['# VP8L prefix-decode current-final matrix', '', f'- baseline: `{BASE}`', f'- CPU: `{cpu}`', '- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed', '', '| workload | candidate | paired median | positive | range |', '|---|---|---:|---:|---:|']
    for name, rows in workloads.items():
        for v in ('table', 'pair'):
            q = [z['base']/z[v] for _, z in sorted(rows.items())]
            lines.append(f'| {name} | {v} | **{statistics.median(q):.4f}x** | {sum(x>1 for x in q)}/{len(q)} | {min(q):.4f}–{max(q):.4f}x |')
    Path('benchmark-vp8l-prefix-current-final.md').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))

if __name__ == '__main__': main()
