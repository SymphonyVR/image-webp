#!/usr/bin/env python3
import math
import os
import shutil
import statistics
import subprocess
from pathlib import Path

BASE = '4cd194935d100a09acf24eb24d8c1343c7844844'
TMP = Path('/tmp/vp8l-group-root-impl')
HERE = Path(__file__).resolve().parent
MATERIALIZERS = [
    HERE / 'materialize_vp8l_group_huffman.py',
    HERE / 'materialize_vp8l_group_parse.py',
    HERE / 'materialize_vp8l_group_decode.py',
]
ROUNDS = 13

BENCH = r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};fn one(d:&[u8])->u64{let mut q=WebPDecoder::new(Cursor::new(d)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();let mut h=0xcbf29ce484222325u64;for &z in&b{h=(h^z as u64).wrapping_mul(1099511628211)}black_box(h)}fn main(){let a:Vec<_>=std::env::args().skip(1).collect();let m=&a[0];let n:usize=a[1].parse().unwrap();let ds:Vec<Vec<u8>>=a[2..].iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for d in&ds{println!("{:016x}",one(d))}return}for d in&ds{black_box(one(d));}let t=Instant::now();for _ in 0..n{for d in&ds{black_box(one(d));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}'''

def run(cmd, cwd=None, cap=False, env=None):
    print('+', ' '.join(map(str, cmd)), flush=True)
    if cap:
        return subprocess.check_output(cmd, cwd=cwd, text=True, env=env).strip()
    subprocess.run(cmd, cwd=cwd, check=True, env=env)

def chunks(path):
    data = path.read_bytes()
    out = []
    if len(data) < 12 or data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        return out
    pos = 12
    while pos + 8 <= len(data):
        tag = data[pos:pos + 4]
        size = int.from_bytes(data[pos + 4:pos + 8], 'little')
        out.append(tag)
        pos += 8 + size + (size & 1)
    return out

def ppm(path, width, height, kind):
    with path.open('wb') as f:
        f.write(f'P6\n{width} {height}\n255\n'.encode())
        for y in range(height):
            row = bytearray()
            for x in range(width):
                if kind == 'gradient':
                    r = x * 255 // max(1, width - 1)
                    g = y * 255 // max(1, height - 1)
                    b = (x + y) * 255 // max(1, width + height - 2)
                elif kind == 'corr':
                    g = (x * 7 + y * 11 + ((x * y) >> 7)) & 255
                    r = (g + ((x >> 3) & 15)) & 255
                    b = (g - ((y >> 3) & 15)) & 255
                elif kind == 'color':
                    r = (x * 11 + y * 3) & 255
                    g = (x * 5 + y * 13) & 255
                    b = (r + g * 3) & 255
                elif kind == 'structured':
                    q = ((x >> 5) + 3 * (y >> 5)) & 15
                    r = q * 17
                    g = (q * 53 + (x & 31) * 3) & 255
                    b = (q * 91 + (y & 31) * 5) & 255
                else:
                    z = (x * 1103515245 + y * 12345 + (x * y) * 2654435761 + 0x9e3779b9) & 0xffffffff
                    r = (z >> 8) & 255
                    g = (z >> 16) & 255
                    b = (z >> 24) & 255
                row += bytes((r, g, b))
            f.write(row)

def invoke(exe, mode, iterations, paths):
    return run(['taskset', '-c', '0', str(exe), mode, str(iterations), *map(str, paths)], cap=True)

def prepare(name, candidate):
    root = TMP / name
    run(['git', 'worktree', 'add', '--detach', str(root), BASE])
    if candidate:
        for script in MATERIALIZERS:
            run(['python3', str(script)], cwd=root)
        run(['cargo', 'fmt'], cwd=root)
        run(['git', 'diff', '--check'], cwd=root)
    (root / 'examples').mkdir(exist_ok=True)
    (root / 'examples/group_root_bench.rs').write_text(BENCH)
    env = os.environ.copy()
    env['RUSTFLAGS'] = '-C target-cpu=native'
    run(['cargo', 'build', '--release', '--example', 'group_root_bench', '-q'], cwd=root, env=env)
    return root, root / 'target/release/examples/group_root_bench'

def paired(exes, files, iterations):
    values = {'base': [], 'candidate': []}
    ratios = []
    for rnd in range(ROUNDS):
        order = ('base', 'candidate') if rnd % 2 == 0 else ('candidate', 'base')
        sample = {}
        for name in order:
            sample[name] = float(invoke(exes[name], 't', iterations, files[name]))
            values[name].append(sample[name])
        ratios.append(sample['base'] / sample['candidate'])
    return values, ratios

def choose_iterations(exe, paths, target_us=140000, cap=100):
    probe = float(invoke(exe, 't', 1, paths))
    total_per_iteration = probe * len(paths)
    return max(1, min(cap, math.ceil(target_us / max(total_per_iteration, 1.0))))

def main():
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir()
    roots = {}
    exes = {}
    roots['base'], exes['base'] = prepare('base', False)
    roots['candidate'], exes['candidate'] = prepare('candidate', True)

    generated = {}
    for kind in ('structured', 'gradient', 'corr', 'color', 'noise'):
        source = TMP / f'{kind}.ppm'
        ppm(source, 1536, 1536, kind)
        for level in (0, 9):
            target = TMP / f'{kind}-z{level}.webp'
            run(['cwebp', '-quiet', '-lossless', '-z', str(level), str(source), '-o', str(target)])
            generated[f'{kind}-z{level}'] = target

    rels = [
        path.relative_to(roots['base'])
        for path in sorted((roots['base'] / 'tests/images').rglob('*.webp'))
        if b'VP8L' in chunks(path) and b'ANIM' not in chunks(path)
    ]
    base_corpus = [roots['base'] / rel for rel in rels]
    cand_corpus = [roots['candidate'] / rel for rel in rels]

    if invoke(exes['base'], 'h', 1, base_corpus) != invoke(exes['candidate'], 'h', 1, cand_corpus):
        raise SystemExit('repository VP8L corpus hash mismatch')
    generated_paths = list(generated.values())
    if invoke(exes['base'], 'h', 1, generated_paths) != invoke(exes['candidate'], 'h', 1, generated_paths):
        raise SystemExit('generated VP8L hash mismatch')

    workloads = []
    corpus_files = {'base': base_corpus, 'candidate': cand_corpus}
    corpus_iters = choose_iterations(exes['base'], base_corpus, cap=120)
    workloads.append(('repo-vp8l-corpus', corpus_files, corpus_iters))

    for label, path in generated.items():
        files = {'base': [path], 'candidate': [path]}
        iterations = choose_iterations(exes['base'], [path], cap=20)
        workloads.append((label, files, iterations))

    for level in (0, 9):
        paths = [generated[f'{kind}-z{level}'] for kind in ('structured', 'gradient', 'corr', 'color', 'noise')]
        files = {'base': paths, 'candidate': paths}
        iterations = choose_iterations(exes['base'], paths, target_us=180000, cap=12)
        workloads.append((f'generated-z{level}-aggregate', files, iterations))

    cpu = run(['bash', '-lc', "lscpu|sed -n 's/^Model name:[[:space:]]*//p'"], cap=True)
    lines = [
        '# VP8L group-static Huffman root benchmark',
        '',
        f'- base: `{BASE}`',
        f'- CPU: `{cpu}`',
        f'- {ROUNDS} alternating/reversed paired rounds; candidate hashes equal base',
        '- group selector: 11-bit root when any group tree has >=256 symbols and >=1/8 of non-zero symbols longer than 9 bits; otherwise 9-bit',
        '- group width is dispatched once per meta-Huffman run; symbol decode remains const-generic/monomorphic',
        '',
        '| workload | base median us | candidate median us | paired speedup | positive rounds |',
        '|---|---:|---:|---:|---:|',
    ]
    all_ratios = []
    for label, files, iterations in workloads:
        values, ratios = paired(exes, files, iterations)
        all_ratios.extend(ratios if label == 'repo-vp8l-corpus' else [])
        lines.append(
            f'| {label} | {statistics.median(values["base"]):.3f} | '
            f'{statistics.median(values["candidate"]):.3f} | **{statistics.median(ratios):.4f}x** | '
            f'{sum(r > 1 for r in ratios)}/{len(ratios)} |'
        )
    text = '\n'.join(lines) + '\n'
    Path('benchmark-vp8l-group-root-impl.md').write_text(text)
    print(text)

if __name__ == '__main__':
    main()
