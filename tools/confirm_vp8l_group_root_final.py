#!/usr/bin/env python3
import math
import os
import shutil
import statistics
import subprocess
from pathlib import Path

MAIN = 'f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f'
BASE = '4cd194935d100a09acf24eb24d8c1343c7844844'
TMP = Path('/tmp/confirm-vp8l-group-root-final')
HERE = Path(__file__).resolve().parent
ROUNDS = 21
VERSIONS = ('main', 'base', 'candidate')
MATERIALIZERS = (
    HERE / 'materialize_vp8l_group_huffman.py',
    HERE / 'materialize_vp8l_group_parse.py',
    HERE / 'materialize_vp8l_group_decode.py',
)

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
    return run(
        ['taskset', '-c', '0', str(exe), mode, str(iterations), *map(str, paths)],
        cap=True,
    )


def prepare(name, sha, candidate=False):
    root = TMP / name
    run(['git', 'worktree', 'add', '--detach', str(root), sha])
    if candidate:
        for script in MATERIALIZERS:
            run(['python3', str(script)], cwd=root)
        run(['cargo', 'fmt'], cwd=root)
        run(['git', 'diff', '--check'], cwd=root)
    (root / 'examples').mkdir(exist_ok=True)
    (root / 'examples/group_root_confirm.rs').write_text(BENCH)
    env = os.environ.copy()
    env['RUSTFLAGS'] = '-C target-cpu=native'
    run(['cargo', 'build', '--release', '--example', 'group_root_confirm', '-q'], cwd=root, env=env)
    return root, root / 'target/release/examples/group_root_confirm'


def paired(exes, files, iterations):
    samples = {name: [] for name in VERSIONS}
    rounds = {}
    for rnd in range(ROUNDS):
        order = VERSIONS if rnd % 2 == 0 else tuple(reversed(VERSIONS))
        current = {}
        for name in order:
            current[name] = float(invoke(exes[name], 't', iterations, files[name]))
            samples[name].append(current[name])
        rounds[rnd] = current
    return {name: statistics.median(values) for name, values in samples.items()}, rounds


def choose_iterations(exe, paths, target_us=180_000, cap=80):
    probe = float(invoke(exe, 't', 1, paths))
    total = probe * len(paths)
    return max(1, min(cap, math.ceil(target_us / max(total, 1.0))))


def main():
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir()

    roots = {}
    exes = {}
    roots['main'], exes['main'] = prepare('main', MAIN)
    roots['base'], exes['base'] = prepare('base', BASE)
    roots['candidate'], exes['candidate'] = prepare('candidate', BASE, candidate=True)

    generated = {}
    for kind in ('structured', 'gradient', 'corr', 'color', 'noise'):
        source = TMP / f'{kind}.ppm'
        ppm(source, 2048, 2048, kind)
        for level in (0, 9):
            target = TMP / f'{kind}-z{level}.webp'
            run(['cwebp', '-quiet', '-lossless', '-z', str(level), str(source), '-o', str(target)])
            generated[f'{kind}-z{level}'] = target

    rels = [
        path.relative_to(roots['base'])
        for path in sorted((roots['base'] / 'tests/images').rglob('*.webp'))
        if b'VP8L' in chunks(path) and b'ANIM' not in chunks(path)
    ]
    repo_files = {
        name: [roots[name] / rel for rel in rels]
        for name in VERSIONS
    }

    base_repo_hash = invoke(exes['base'], 'h', 1, repo_files['base'])
    cand_repo_hash = invoke(exes['candidate'], 'h', 1, repo_files['candidate'])
    if base_repo_hash != cand_repo_hash:
        raise SystemExit('repository VP8L corpus hash mismatch')

    generated_paths = list(generated.values())
    if invoke(exes['base'], 'h', 1, generated_paths) != invoke(exes['candidate'], 'h', 1, generated_paths):
        raise SystemExit('generated VP8L hash mismatch')

    issue = None
    try:
        archive = TMP / 'sample.zip'
        run([
            'curl', '-L', '--fail', '--retry', '3', '-o', str(archive),
            'https://github.com/user-attachments/files/17482915/sample.zip',
        ])
        issue_dir = TMP / 'issue119'
        issue_dir.mkdir()
        run(['unzip', '-q', str(archive), '-d', str(issue_dir)])
        issue = next(issue_dir.rglob('*.webp'))
        if invoke(exes['base'], 'h', 1, [issue]) != invoke(exes['candidate'], 'h', 1, [issue]):
            raise SystemExit('issue119 hash mismatch')
    except (subprocess.CalledProcessError, StopIteration):
        print('issue119 fixture unavailable; continuing without it', flush=True)
        issue = None

    workloads = []

    repo_iters = choose_iterations(exes['base'], repo_files['base'], target_us=220_000, cap=120)
    med, rounds = paired(exes, repo_files, repo_iters)
    workloads.append(('repo-vp8l-corpus', med, rounds))

    for label, path in generated.items():
        files = {name: [path] for name in VERSIONS}
        iterations = choose_iterations(exes['base'], [path], target_us=180_000, cap=20)
        med, rounds = paired(exes, files, iterations)
        workloads.append((label, med, rounds))

    for level in (0, 9):
        paths = [generated[f'{kind}-z{level}'] for kind in ('structured', 'gradient', 'corr', 'color', 'noise')]
        files = {name: paths for name in VERSIONS}
        iterations = choose_iterations(exes['base'], paths, target_us=240_000, cap=12)
        med, rounds = paired(exes, files, iterations)
        workloads.append((f'generated-z{level}-aggregate', med, rounds))

    if issue is not None:
        files = {name: [issue] for name in VERSIONS}
        iterations = choose_iterations(exes['base'], [issue], target_us=220_000, cap=12)
        med, rounds = paired(exes, files, iterations)
        workloads.append(('issue119', med, rounds))

    cpu = run(['bash', '-lc', "lscpu|sed -n 's/^Model name:[[:space:]]*//p'"], cap=True)
    lines = [
        '# Final VP8L group-static Huffman root confirmation',
        '',
        f'- main: `{MAIN}`',
        f'- composed base: `{BASE}`',
        '- candidate: exact composed base materialized with group-static 9/11-bit Huffman roots',
        f'- CPU: `{cpu}`',
        f'- release native, CPU 0 pinned, {ROUNDS} alternating/reversed 3-way rounds',
        '- candidate hashes == composed-base hashes on repository VP8L corpus, every generated stream, and issue119 when available',
        '- selector: 11-bit group when any implicit tree has >=256 non-zero symbols and >=1/8 have code length >9; otherwise 9-bit',
        '',
        '| workload | main us | base us | candidate us | candidate/main | candidate/base | cand>main | cand>base |',
        '|---|---:|---:|---:|---:|---:|---:|---:|',
    ]
    for label, med, rounds in workloads:
        ordered = [rounds[i] for i in sorted(rounds)]
        vs_main = [sample['main'] / sample['candidate'] for sample in ordered]
        vs_base = [sample['base'] / sample['candidate'] for sample in ordered]
        lines.append(
            f"| {label} | {med['main']:.3f} | {med['base']:.3f} | {med['candidate']:.3f} | "
            f"**{statistics.median(vs_main):.4f}x** | **{statistics.median(vs_base):.4f}x** | "
            f"{sum(x > 1 for x in vs_main)}/{ROUNDS} | {sum(x > 1 for x in vs_base)}/{ROUNDS} |"
        )

    output = '\n'.join(lines) + '\n'
    Path('benchmark-vp8l-group-root-confirm-final.md').write_text(output)
    print(output)


if __name__ == '__main__':
    main()
