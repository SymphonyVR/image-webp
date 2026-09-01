#!/usr/bin/env python3
import hashlib
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image

BASE = '4cd194935d100a09acf24eb24d8c1343c7844844'
TMP = Path('/tmp/vp8l-group-root-deep')
HERE = Path(__file__).resolve().parent
MATERIALIZERS = (
    HERE / 'materialize_vp8l_group_huffman.py',
    HERE / 'materialize_vp8l_group_parse.py',
    HERE / 'materialize_vp8l_group_decode.py',
)


def run(cmd, cwd=None, cap=False, env=None):
    print('+', ' '.join(map(str, cmd)), flush=True)
    if cap:
        return subprocess.check_output(cmd, cwd=cwd, env=env)
    subprocess.run(cmd, cwd=cwd, check=True, env=env)


def chunks(data):
    if len(data) < 12 or data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        return []
    out = []
    pos = 12
    while pos + 8 <= len(data):
        tag = data[pos:pos + 4]
        size = int.from_bytes(data[pos + 4:pos + 8], 'little')
        out.append(tag)
        pos += 8 + size + (size & 1)
    return out


def parse_pam(data):
    if not data.startswith(b'P7\n'):
        raise RuntimeError('expected PAM from dwebp')
    end = data.index(b'ENDHDR\n') + len(b'ENDHDR\n')
    values = {}
    for line in data[:end].decode('ascii').splitlines()[1:]:
        if ' ' in line:
            key, value = line.split(' ', 1)
            values[key] = value
    width = int(values['WIDTH'])
    height = int(values['HEIGHT'])
    depth = int(values['DEPTH'])
    raw = data[end:]
    if len(raw) != width * height * depth:
        raise RuntimeError('bad PAM size')
    if depth == 4:
        return width, height, raw
    if depth == 3:
        out = bytearray(width * height * 4)
        for i in range(width * height):
            out[4 * i:4 * i + 4] = raw[3 * i:3 * i + 3] + b'\xff'
        return width, height, bytes(out)
    raise RuntimeError(f'unsupported PAM depth {depth}')


def pixel(kind, x, y, width, height, alpha):
    if kind == 'solid':
        r, g, b = 37, 149, 233
    elif kind == 'gradient':
        r = x * 255 // max(1, width - 1)
        g = y * 255 // max(1, height - 1)
        b = (x + y) * 255 // max(1, width + height - 2)
    elif kind == 'checker':
        q = ((x >> 2) ^ (y >> 2)) & 1
        r, g, b = 255 * q, 63 + 128 * (1 - q), 17 + 211 * q
    elif kind == 'palette':
        palette = [
            (0, 0, 0), (255, 255, 255), (255, 0, 80), (20, 220, 70),
            (30, 90, 250), (230, 190, 20), (170, 40, 220), (20, 210, 210),
            (110, 100, 90), (5, 150, 240), (245, 80, 30), (80, 230, 170),
            (130, 30, 70), (70, 120, 10), (200, 200, 240), (44, 55, 66),
        ]
        r, g, b = palette[((x >> 1) + 3 * (y >> 1)) & 15]
    elif kind == 'corr':
        g = (x * 7 + y * 11 + ((x * y) >> 4)) & 255
        r = (g + ((x >> 2) & 31)) & 255
        b = (g - ((y >> 2) & 31)) & 255
    elif kind == 'anticorr':
        g = (x * 5 + y * 3) & 255
        r = (255 - g + ((x >> 3) & 15)) & 255
        b = g ^ 255
    elif kind == 'stripes':
        r = (x * 17) & 255
        g = ((x // 3) * 53 + y) & 255
        b = ((x // 7) * 91 + y * 3) & 255
    elif kind == 'tiles':
        q = ((x >> 4) + 3 * (y >> 4)) & 15
        r = q * 17
        g = (q * 53 + (x & 15) * 7) & 255
        b = (q * 91 + (y & 15) * 11) & 255
    else:
        z = (x * 1103515245 + y * 12345 + (x * y) * 2654435761 + 0x9e3779b9) & 0xffffffff
        r, g, b = (z >> 8) & 255, (z >> 16) & 255, (z >> 24) & 255

    if alpha is None:
        return r, g, b, 255
    if alpha == 'binary':
        a = 255 if ((x >> 2) ^ (y >> 2)) & 1 else 0
    elif alpha == 'gradient':
        a = (x * 13 + y * 29) & 255
    elif alpha == 'sparse':
        a = 255 if ((x * 17 + y * 31) % 19) == 0 else 0
    else:
        a = ((x * 17 + y * 31 + (x * y)) >> 2) & 255
    return r, g, b, a


def make_png(path, width, height, kind, alpha):
    image = Image.new('RGBA', (width, height))
    values = [
        pixel(kind, x, y, width, height, alpha)
        for y in range(height)
        for x in range(width)
    ]
    image.putdata(values)
    image.save(path)
    return b''.join(bytes(value) for value in values)


RUST = r'''use image_webp::WebPDecoder;use std::io::{Cursor,Write};fn main(){let p=std::env::args().nth(1).unwrap();let d=std::fs::read(p).unwrap();let mut q=WebPDecoder::new(Cursor::new(d)).unwrap();let(w,h)=q.dimensions();let alpha=q.has_alpha();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();let mut out=Vec::with_capacity(w as usize*h as usize*4);if alpha{out.extend_from_slice(&b)}else{for p in b.chunks_exact(3){out.extend_from_slice(p);out.push(255)}}std::io::stdout().write_all(&out).unwrap();}'''


def main():
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir()
    root = TMP / 'candidate'
    run(['git', 'worktree', 'add', '--detach', str(root), BASE])
    for script in MATERIALIZERS:
        run(['python3', str(script)], cwd=root)
    run(['cargo', 'fmt'], cwd=root)
    run(['git', 'diff', '--check'], cwd=root)
    run(['cargo', 'test', '-q'], cwd=root)
    run(['cargo', '+1.80.1', 'build', '-q'], cwd=root)

    (root / 'examples').mkdir(exist_ok=True)
    (root / 'examples/ref_rgba.rs').write_text(RUST)
    env = os.environ.copy()
    env['RUSTFLAGS'] = '-C target-cpu=native'
    run(['cargo', 'build', '--release', '--example', 'ref_rgba', '-q'], cwd=root, env=env)
    rustbin = root / 'target/release/examples/ref_rgba'

    cases = []
    for path in sorted((root / 'tests/images').rglob('*.webp')):
        tags = chunks(path.read_bytes())
        if b'VP8L' in tags and b'ANIM' not in tags:
            cases.append(('repo/' + str(path.relative_to(root)), path, None))

    dims = [
        (1, 1), (1, 7), (2, 2), (3, 5), (4, 4), (7, 3),
        (15, 17), (16, 16), (17, 15), (31, 33), (32, 32), (33, 31),
        (63, 65), (64, 64), (65, 63), (127, 129), (128, 128), (129, 127),
        (255, 257), (256, 256), (257, 255), (511, 513), (512, 512), (513, 511),
    ]
    patterns = ['solid', 'gradient', 'checker', 'palette', 'corr', 'anticorr', 'stripes', 'tiles', 'noise']
    alphas = [None, 'binary', 'gradient', 'sparse', 'noise']
    specs = []
    for i, (width, height) in enumerate(dims):
        specs.append((width, height, patterns[i % len(patterns)], alphas[i % len(alphas)]))
        specs.append((width, height, patterns[(i + 4) % len(patterns)], alphas[(i + 2) % len(alphas)]))
    for kind in patterns:
        for alpha in alphas:
            specs.append((73, 59, kind, alpha))
    for kind in ('gradient', 'corr', 'anticorr', 'stripes', 'tiles', 'noise'):
        for alpha in alphas:
            specs.append((193, 131, kind, alpha))

    generated = 0
    for case_index, (width, height, kind, alpha) in enumerate(specs):
        png = TMP / f'in-{case_index}.png'
        expected = make_png(png, width, height, kind, alpha)
        for level in (0, 3, 6, 9):
            webp = TMP / f'gen-{case_index}-z{level}.webp'
            run(['cwebp', '-quiet', '-lossless', '-exact', '-z', str(level), str(png), '-o', str(webp)])
            cases.append((f'gen/{width}x{height}/{kind}/{alpha}/z{level}', webp, expected))
            generated += 1

    oracle_mismatch = []
    source_mismatch = []
    rows = []
    for label, path, expected in cases:
        rust = run([str(rustbin), str(path)], cap=True)
        ref_path = TMP / 'ref.pam'
        run(['dwebp', '-quiet', str(path), '-pam', '-o', str(ref_path)])
        width, height, reference = parse_pam(ref_path.read_bytes())
        oracle_ok = rust == reference
        source_ok = expected is None or rust == expected
        if not oracle_ok:
            oracle_mismatch.append(label)
        if not source_ok:
            source_mismatch.append(label)
        rows.append((label, width, height, len(rust), hashlib.sha256(rust).hexdigest()[:16], oracle_ok, source_ok))

    lines = [
        '# Deep VP8L group-static root differential verification',
        '',
        f'- composed base: `{BASE}`',
        '- candidate: base materialized with group-static 9/11-bit Huffman roots',
        f'- total streams: **{len(cases)}**',
        f'- generated streams: **{generated}**',
        '- hard oracle: candidate Rust decoder output must equal libwebp `dwebp` byte-for-byte',
        '- generated fidelity: `cwebp -lossless -exact` output must round-trip to original RGBA bytes',
        '- coverage: tiny/odd/power-of-two boundaries through 513px; palette/correlated/anti-correlated/stripes/tiles/noise; opaque/binary/gradient/sparse/noisy alpha; z0/z3/z6/z9',
        '',
        f'- Rust vs libwebp mismatches: **{len(oracle_mismatch)}**',
        f'- generated source-fidelity mismatches: **{len(source_mismatch)}**',
    ]
    if oracle_mismatch:
        lines += ['', '## Oracle mismatches'] + [f'- {item}' for item in oracle_mismatch]
    if source_mismatch:
        lines += ['', '## Source-fidelity mismatches'] + [f'- {item}' for item in source_mismatch]
    lines += [
        '', '## Sample records', '',
        '| stream | size | bytes | sha256 prefix | oracle | source |',
        '|---|---:|---:|---|---|---|',
    ]
    for label, width, height, size, digest, oracle_ok, source_ok in rows[:60]:
        lines.append(f'| {label} | {width}x{height} | {size} | `{digest}` | {oracle_ok} | {source_ok} |')

    output = '\n'.join(lines) + '\n'
    Path('verification-vp8l-group-root-deep.md').write_text(output)
    print(output)
    if oracle_mismatch or source_mismatch:
        raise SystemExit(f'oracle={len(oracle_mismatch)} source={len(source_mismatch)}')


if __name__ == '__main__':
    main()
