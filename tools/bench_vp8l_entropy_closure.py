#!/usr/bin/env python3
import csv
import os
import shutil
import statistics
import subprocess
from pathlib import Path

BASE = "509d11c2bf102929ded4be05d3c54b06032fdc44"
ROOT = Path.cwd()
TMP = Path("/tmp/vp8l-entropy-closure")
VARIANTS = ["repeat", "prealloc", "literal", "prefix", "all"]


def run(cmd, cwd=None, capture=False):
    print("+", " ".join(map(str, cmd)), flush=True)
    if capture:
        return subprocess.check_output(cmd, cwd=cwd, text=True).strip()
    subprocess.run(cmd, cwd=cwd, check=True)


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"missing patch marker: {label}")
    return text.replace(old, new, 1)


def patch_variant(name, root):
    p = root / "src/lossless/decoder/mod.rs"
    s = p.read_text()

    if name in ("repeat", "all"):
        old = '''                let length = if use_prev { prev_code_len } else { 0 };\n                while repeat > 0 {\n                    repeat -= 1;\n                    code_lengths[usize::from(symbol)] = length;\n                    symbol += 1;\n                }\n'''
        new = '''                let length = if use_prev { prev_code_len } else { 0 };\n                let end = symbol + repeat;\n                code_lengths[usize::from(symbol)..usize::from(end)].fill(length);\n                symbol = end;\n'''
        s = replace_once(s, old, new, "repeat fill")

    if name in ("prealloc", "all"):
        s = replace_once(
            s,
            "        let mut hufftree_groups = Vec::new();\n",
            "        let mut hufftree_groups = Vec::with_capacity(num_huff_groups as usize);\n",
            "huffman group preallocation",
        )

    if name in ("literal", "all"):
        old = '''                data[index * 4] = red;\n                data[index * 4 + 1] = green;\n                data[index * 4 + 2] = blue;\n                data[index * 4 + 3] = alpha;\n\n                if let Some(color_cache) = huffman_info.color_cache.as_mut() {\n                    color_cache.insert([red, green, blue, alpha]);\n                }\n'''
        new = '''                let value = [red, green, blue, alpha];\n                data[index * 4..][..4].copy_from_slice(&value);\n\n                if let Some(color_cache) = huffman_info.color_cache.as_mut() {\n                    color_cache.insert(value);\n                }\n'''
        s = replace_once(s, old, new, "literal packed store")

    if name in ("prefix", "all"):
        marker = "const ALPHABET_SIZE: [u16; HUFFMAN_CODES_PER_META_CODE] = [256 + 24, 256, 256, 256, 40];\n"
        consts = '''const COPY_EXTRA_BITS: [u8; 40] = [\n    0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10,\n    11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18,\n];\nconst COPY_BASE: [usize; 40] = [\n    1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193, 257, 385, 513, 769,\n    1025, 1537, 2049, 3073, 4097, 6145, 8193, 12289, 16385, 24577, 32769, 49153,\n    65537, 98305, 131073, 196609, 262145, 393217, 524289, 786433,\n];\n'''
        s = replace_once(s, marker, marker + consts, "prefix constants")
        old = '''        if prefix_code < 4 {\n            return Ok(usize::from(prefix_code + 1));\n        }\n        let extra_bits: u8 = ((prefix_code - 2) >> 1).try_into().unwrap();\n        let offset = (2 + (usize::from(prefix_code) & 1)) << extra_bits;\n\n        let bits = bit_reader.peek(extra_bits) as usize;\n        bit_reader.consume(extra_bits)?;\n\n        Ok(offset + bits + 1)\n'''
        new = '''        let prefix = usize::from(prefix_code);\n        debug_assert!(prefix < COPY_EXTRA_BITS.len());\n        let extra_bits = COPY_EXTRA_BITS[prefix];\n        let bits = bit_reader.peek(extra_bits) as usize;\n        bit_reader.consume(extra_bits)?;\n        Ok(COPY_BASE[prefix] + bits)\n'''
        s = replace_once(s, old, new, "prefix decode")

    p.write_text(s)


def prepare_tree(name):
    root = TMP / name
    if root.exists():
        shutil.rmtree(root)
    run(["git", "worktree", "add", "--detach", str(root), BASE])
    if name != "base":
        patch_variant(name, root)
        run(["cargo", "fmt"], cwd=root)
        run(["cargo", "test", "-q"], cwd=root)
        run(["cargo", "+1.80.1", "build", "-q"], cwd=root)
    return root


def make_large_fixture():
    ppm = TMP / "large.ppm"
    webp = TMP / "large.webp"
    w = h = 2048
    with ppm.open("wb") as f:
        f.write(f"P6\n{w} {h}\n255\n".encode())
        row = bytearray(w * 3)
        for y in range(h):
            for x in range(w):
                i = x * 3
                row[i] = (x * 3 + y * 5 + ((x >> 5) ^ (y >> 4)) * 17) & 255
                row[i + 1] = (x * 2 + y * 7 + ((x * y) >> 10)) & 255
                row[i + 2] = (x * 11 + y * 3 + ((x + y) >> 3) * 9) & 255
            f.write(row)
    run(["cwebp", "-quiet", "-lossless", "-z", "9", str(ppm), "-o", str(webp)])
    return webp


def vp8l_files(base_root):
    out = []
    for p in sorted((base_root / "tests/images").rglob("*.webp")):
        d = p.read_bytes()
        if len(d) < 12 or d[:4] != b"RIFF" or d[8:12] != b"WEBP":
            continue
        pos = 12
        chunks = []
        while pos + 8 <= len(d):
            fourcc = d[pos:pos+4]
            n = int.from_bytes(d[pos+4:pos+8], "little")
            chunks.append(fourcc)
            pos += 8 + n + (n & 1)
        if b"VP8L" in chunks and b"ANIM" not in chunks:
            out.append(p.relative_to(base_root))
    if not out:
        raise SystemExit("no VP8L fixtures")
    return out


BENCH_RS = r'''use image_webp::WebPDecoder;
use std::{hint::black_box, io::Cursor, time::Instant};
fn decode(d: &[u8]) -> Vec<u8> {
    let mut x = WebPDecoder::new(Cursor::new(d)).unwrap();
    let mut b = vec![0; x.output_buffer_size().unwrap()];
    x.read_image(&mut b).unwrap();
    b
}
fn hash(d: &[u8]) -> u64 {
    decode(d).iter().fold(1469598103934665603u64, |h, &b| (h ^ u64::from(b)).wrapping_mul(1099511628211))
}
fn main() {
    let mut a = std::env::args().skip(1);
    let mode = a.next().unwrap();
    let n: usize = a.next().unwrap().parse().unwrap();
    let paths: Vec<_> = a.collect();
    let data: Vec<Vec<u8>> = paths.iter().map(std::fs::read).collect::<Result<_, _>>().unwrap();
    if mode == "hash" {
        for d in &data { println!("{:016x}", hash(d)); }
        return;
    }
    for d in &data { black_box(decode(d)); }
    let t = Instant::now();
    for _ in 0..n { for d in &data { black_box(decode(d)); } }
    println!("{:.3}", t.elapsed().as_secs_f64() * 1e6 / (n * data.len()) as f64);
}
'''


def build_bench(root):
    ex = root / "examples"
    ex.mkdir(exist_ok=True)
    (ex / "vp8l_entropy_closure.rs").write_text(BENCH_RS)
    env = os.environ.copy()
    env["RUSTFLAGS"] = "-C target-cpu=native"
    print("+ cargo build --release --example vp8l_entropy_closure", flush=True)
    subprocess.run(["cargo", "build", "--release", "--example", "vp8l_entropy_closure", "-q"], cwd=root, env=env, check=True)
    return root / "target/release/examples/vp8l_entropy_closure"


def timed(binary, root, mode, repeats, rels, large):
    files = [str(root / r) for r in rels] if mode == "corpus" else [str(large)]
    return float(run(["taskset", "-c", "0", str(binary), "bench", str(repeats), *files], capture=True))


def main():
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    roots = {name: prepare_tree(name) for name in ["base", *VARIANTS]}
    rels = vp8l_files(roots["base"])
    large = make_large_fixture()
    bins = {name: build_bench(root) for name, root in roots.items()}

    base_hash = run([str(bins["base"]), "hash", "1", *[str(roots["base"] / r) for r in rels], str(large)], capture=True)
    for name in VARIANTS:
        cand_hash = run([str(bins[name]), "hash", "1", *[str(roots[name] / r) for r in rels], str(large)], capture=True)
        if cand_hash != base_hash:
            raise SystemExit(f"hash mismatch: {name}")

    rows = []
    rounds = 15
    for rnd in range(1, rounds + 1):
        order = ["base", *VARIANTS] if rnd % 2 else [*reversed(VARIANTS), "base"]
        for name in order:
            rows.append(("corpus", rnd, name, timed(bins[name], roots[name], "corpus", 60, rels, large)))
            rows.append(("large", rnd, name, timed(bins[name], roots[name], "large", 3, rels, large)))

    rr = {}
    vals = {}
    for workload, rnd, name, value in rows:
        rr.setdefault((workload, rnd), {})[name] = value
        vals.setdefault((workload, name), []).append(value)

    cpu = run(["bash", "-lc", "lscpu | sed -n 's/^Model name:[[:space:]]*//p'"], capture=True)
    lines = [
        "# VP8L entropy closure matrix",
        "",
        f"- baseline: `{BASE}`",
        f"- CPU: `{cpu}`",
        f"- static VP8L fixtures: `{len(rels)}`",
        "- all candidates: decoded hashes match; cargo test and Rust 1.80.1 build pass",
        "",
        "| workload | candidate | base median | candidate median | paired median | positive | range |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for workload in ("corpus", "large"):
        for name in VARIANTS:
            ratios = [z["base"] / z[name] for (w, _), z in sorted(rr.items()) if w == workload]
            lines.append(
                f"| {workload} | {name} | {statistics.median(vals[workload, 'base']):.3f} us | "
                f"{statistics.median(vals[workload, name]):.3f} us | {statistics.median(ratios):.4f}x | "
                f"{sum(x > 1 for x in ratios)}/{len(ratios)} | {min(ratios):.4f}–{max(ratios):.4f}x |"
            )
    Path("benchmark-vp8l-entropy-closure-v2.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
