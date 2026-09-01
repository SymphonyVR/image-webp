#!/usr/bin/env python3
import os
import shutil
import statistics
import subprocess
from pathlib import Path

BASE = "509d11c2bf102929ded4be05d3c54b06032fdc44"
TMP = Path("/tmp/vp8l-transform-closure")
VARIANTS = ["color_exact", "color_inc", "color_packed", "green", "palette_stack", "palette_noscratch", "palette_both", "all"]


def run(cmd, cwd=None, capture=False, env=None):
    print("+", " ".join(map(str, cmd)), flush=True)
    if capture:
        return subprocess.check_output(cmd, cwd=cwd, text=True, env=env).strip()
    subprocess.run(cmd, cwd=cwd, check=True, env=env)


def replace_once(s, old, new, label):
    if old not in s:
        raise SystemExit(f"missing marker: {label}")
    return s.replace(old, new, 1)


def replace_color_fn(s, body, helper=""):
    a = s.index("pub(crate) fn apply_color_transform(")
    b = s.index("pub(crate) fn apply_subtract_green_transform(", a)
    return s[:a] + helper + body + s[b:]


COLOR_EXACT = r'''pub(crate) fn apply_color_transform(
    image_data: &mut [u8], width: u16, size_bits: u8, transform_data: &[u8],
) {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);
    let block_bytes = 4usize << size_bits;
    for (y, row) in image_data.chunks_exact_mut(width * 4).enumerate() {
        let row_tf_data = &transform_data[(y >> size_bits) * block_xsize * 4..];
        let mut blocks = row.chunks_exact_mut(block_bytes);
        let mut transforms = row_tf_data.chunks_exact(4);
        for (block, transform) in (&mut blocks).zip(&mut transforms) {
            let red_to_blue = transform[0];
            let green_to_blue = transform[1];
            let green_to_red = transform[2];
            for pixel in block.chunks_exact_mut(4) {
                let green = u32::from(pixel[1]);
                let mut temp_red = u32::from(pixel[0]);
                let mut temp_blue = u32::from(pixel[2]);
                temp_red += color_transform_delta(green_to_red as i8, green as i8);
                temp_blue += color_transform_delta(green_to_blue as i8, green as i8);
                temp_blue += color_transform_delta(red_to_blue as i8, temp_red as i8);
                pixel[0] = (temp_red & 0xff) as u8;
                pixel[2] = (temp_blue & 0xff) as u8;
            }
        }
        let tail = blocks.into_remainder();
        if !tail.is_empty() {
            let transform = transforms.next().unwrap();
            let red_to_blue = transform[0];
            let green_to_blue = transform[1];
            let green_to_red = transform[2];
            for pixel in tail.chunks_exact_mut(4) {
                let green = u32::from(pixel[1]);
                let mut temp_red = u32::from(pixel[0]);
                let mut temp_blue = u32::from(pixel[2]);
                temp_red += color_transform_delta(green_to_red as i8, green as i8);
                temp_blue += color_transform_delta(green_to_blue as i8, green as i8);
                temp_blue += color_transform_delta(red_to_blue as i8, temp_red as i8);
                pixel[0] = (temp_red & 0xff) as u8;
                pixel[2] = (temp_blue & 0xff) as u8;
            }
        }
    }
}

'''

COLOR_INC = r'''pub(crate) fn apply_color_transform(
    image_data: &mut [u8], width: u16, size_bits: u8, transform_data: &[u8],
) {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);
    let block_bytes = 4usize << size_bits;
    let tile_mask = (1usize << size_bits) - 1;
    let mut row_tf_start = 0usize;
    for (y, row) in image_data.chunks_exact_mut(width * 4).enumerate() {
        let row_tf_data = &transform_data[row_tf_start..];
        let mut blocks = row.chunks_exact_mut(block_bytes);
        let mut transforms = row_tf_data.chunks_exact(4);
        for (block, transform) in (&mut blocks).zip(&mut transforms) {
            let red_to_blue = transform[0] as i8;
            let green_to_blue = transform[1] as i8;
            let green_to_red = transform[2] as i8;
            for pixel in block.chunks_exact_mut(4) {
                let green = pixel[1] as i8;
                let mut temp_red = u32::from(pixel[0]);
                let mut temp_blue = u32::from(pixel[2]);
                temp_red += color_transform_delta(green_to_red, green);
                temp_blue += color_transform_delta(green_to_blue, green);
                temp_blue += color_transform_delta(red_to_blue, temp_red as u8 as i8);
                pixel[0] = (temp_red & 0xff) as u8;
                pixel[2] = (temp_blue & 0xff) as u8;
            }
        }
        let tail = blocks.into_remainder();
        if !tail.is_empty() {
            let transform = transforms.next().unwrap();
            let red_to_blue = transform[0] as i8;
            let green_to_blue = transform[1] as i8;
            let green_to_red = transform[2] as i8;
            for pixel in tail.chunks_exact_mut(4) {
                let green = pixel[1] as i8;
                let mut temp_red = u32::from(pixel[0]);
                let mut temp_blue = u32::from(pixel[2]);
                temp_red += color_transform_delta(green_to_red, green);
                temp_blue += color_transform_delta(green_to_blue, green);
                temp_blue += color_transform_delta(red_to_blue, temp_red as u8 as i8);
                pixel[0] = (temp_red & 0xff) as u8;
                pixel[2] = (temp_blue & 0xff) as u8;
            }
        }
        if ((y + 1) & tile_mask) == 0 { row_tf_start += block_xsize * 4; }
    }
}

'''

PACKED_HELPER = r'''#[inline(always)]
fn inverse_color_pixel_packed(pixel: &mut [u8], red_to_blue: u8, green_to_blue: u8, green_to_red: u8) {
    let argb = u32::from_le_bytes(pixel[..4].try_into().unwrap());
    let green = ((argb >> 8) & 0xff) as u8;
    let mut red = argb & 0xff;
    let mut blue = (argb >> 16) & 0xff;
    red += color_transform_delta(green_to_red as i8, green as i8);
    blue += color_transform_delta(green_to_blue as i8, green as i8);
    red &= 0xff;
    blue += color_transform_delta(red_to_blue as i8, red as u8 as i8);
    blue &= 0xff;
    let out = (argb & 0xff00_ff00) | red | (blue << 16);
    pixel[..4].copy_from_slice(&out.to_le_bytes());
}

'''

COLOR_PACKED = r'''pub(crate) fn apply_color_transform(
    image_data: &mut [u8], width: u16, size_bits: u8, transform_data: &[u8],
) {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);
    let tile = 1usize << size_bits;
    let safe = width & !(tile - 1);
    for (y, row) in image_data.chunks_exact_mut(width * 4).enumerate() {
        let row_tf = &transform_data[(y >> size_bits) * block_xsize * 4..];
        let (full, tail) = row.split_at_mut(safe * 4);
        for (block, transform) in full.chunks_exact_mut(tile * 4).zip(row_tf.chunks_exact(4)) {
            let rb = transform[0]; let gb = transform[1]; let gr = transform[2];
            for pixel in block.chunks_exact_mut(4) { inverse_color_pixel_packed(pixel, rb, gb, gr); }
        }
        if !tail.is_empty() {
            let transform = &row_tf[(safe / tile) * 4..][..4];
            let rb = transform[0]; let gb = transform[1]; let gr = transform[2];
            for pixel in tail.chunks_exact_mut(4) { inverse_color_pixel_packed(pixel, rb, gb, gr); }
        }
    }
}

'''

GREEN_PACKED = r'''pub(crate) fn apply_subtract_green_transform(image_data: &mut [u8]) {
    for pixel in image_data.chunks_exact_mut(4) {
        let value = u32::from_le_bytes([pixel[0], pixel[1], pixel[2], pixel[3]]);
        let green = (value >> 8) & 0xff;
        let red_blue = ((value & 0x00ff00ff).wrapping_add(green | (green << 16))) & 0x00ff00ff;
        pixel.copy_from_slice(&((value & 0xff00ff00) | red_blue).to_le_bytes());
    }
}

'''


def patch_palette_stack(s):
    a = s.index("    let expanded_lookup_table_storage: Vec<[u8; EXP_ENTRY_SIZE]>")
    b = s.index("    let packed_image_width_in_blocks", a)
    new = r'''    let mut expanded_lookup_table_array = [[0u8; EXP_ENTRY_SIZE]; 256];
    for (packed_byte_value, entry_pixels_array) in expanded_lookup_table_array.iter_mut().enumerate() {
        let packed_byte_value = packed_byte_value as u8;
        for pixel_sub_index in 0..pixels_per_packed_byte_usize {
            let shift_amount = (pixel_sub_index as u8) * bits_per_entry_u8;
            let k = (packed_byte_value >> shift_amount) & mask_u8;
            let color_source_array: [u8; 4] = if k < table_size {
                let color_data_offset = usize::from(k) * 4;
                table_data[color_data_offset..color_data_offset + 4].try_into().unwrap()
            } else {
                [0u8; 4]
            };
            let array_fill_offset = pixel_sub_index * 4;
            entry_pixels_array[array_fill_offset..array_fill_offset + 4].copy_from_slice(&color_source_array);
        }
    }

'''
    return s[:a] + new + s[b:]


def patch_palette_noscratch(s):
    a = s.index("    let mut packed_indices_for_row: Vec<u8> = vec![0; packed_image_width_in_blocks];")
    b = s.index("\n}\n\n//predictor functions", a)
    new = r'''    for y_rev_idx in 0..height as usize {
        let y = height as usize - 1 - y_rev_idx;
        let packed_row_input_global_offset = y * input_stride_bytes_packed;
        let output_row_global_offset = y * output_stride_bytes_expanded;
        for block_index in (0..packed_image_width_in_blocks).rev() {
            let packed_index = image_data[packed_row_input_global_offset + block_index * 4 + 1];
            let output_offset = output_row_global_offset + block_index * EXP_ENTRY_SIZE;
            let copy_len = if block_index + 1 == packed_image_width_in_blocks {
                final_block_expanded_size_bytes
            } else {
                EXP_ENTRY_SIZE
            };
            image_data[output_offset..output_offset + copy_len]
                .copy_from_slice(&expanded_lookup_table_array[packed_index as usize][..copy_len]);
        }
    }
'''
    return s[:a] + new + s[b:]


def patch_variant(name, root):
    p = root / "src/lossless/decoder/reverse_transform.rs"
    s = p.read_text()
    if name == "color_exact":
        s = replace_color_fn(s, COLOR_EXACT)
    elif name == "color_inc":
        s = replace_color_fn(s, COLOR_INC)
    elif name == "color_packed":
        s = replace_color_fn(s, COLOR_PACKED, PACKED_HELPER)
    elif name == "green":
        a = s.index("pub(crate) fn apply_subtract_green_transform(")
        b = s.index("pub(crate) fn apply_color_indexing_transform(", a)
        s = s[:a] + GREEN_PACKED + s[b:]
    elif name == "palette_stack":
        s = patch_palette_stack(s)
    elif name == "palette_noscratch":
        s = patch_palette_noscratch(s)
    elif name == "palette_both":
        s = patch_palette_stack(s)
        s = patch_palette_noscratch(s)
    elif name == "all":
        s = replace_color_fn(s, COLOR_INC)
        a = s.index("pub(crate) fn apply_subtract_green_transform(")
        b = s.index("pub(crate) fn apply_color_indexing_transform(", a)
        s = s[:a] + GREEN_PACKED + s[b:]
        s = patch_palette_stack(s)
        s = patch_palette_noscratch(s)
    p.write_text(s)


def prepare_tree(name):
    root = TMP / name
    run(["git", "worktree", "add", "--detach", str(root), BASE])
    if name != "base":
        patch_variant(name, root)
        run(["cargo", "fmt"], cwd=root)
        run(["cargo", "test", "-q"], cwd=root)
        run(["cargo", "+1.80.1", "build", "-q"], cwd=root)
    return root


def chunks(d):
    if len(d) < 12 or d[:4] != b"RIFF" or d[8:12] != b"WEBP": return []
    out = []; pos = 12
    while pos + 8 <= len(d):
        f = d[pos:pos+4]; n = int.from_bytes(d[pos+4:pos+8], "little"); out.append(f); pos += 8 + n + (n & 1)
    return out


def corpus(root):
    rels = []
    for p in sorted((root / "tests/images").rglob("*.webp")):
        c = chunks(p.read_bytes())
        if b"VP8L" in c and b"ANIM" not in c: rels.append(p.relative_to(root))
    return rels


def write_ppm(path, w, h, pixel):
    with path.open("wb") as f:
        f.write(f"P6\n{w} {h}\n255\n".encode()); row = bytearray(w * 3)
        for y in range(h):
            for x in range(w):
                r, g, b = pixel(x, y); i = x * 3; row[i:i+3] = bytes((r, g, b))
            f.write(row)


def fixtures():
    w = h = 1536
    generic = TMP / "large.webp"; green = TMP / "green.webp"; palette = TMP / "palette.webp"
    write_ppm(TMP / "large.ppm", w, h, lambda x,y: ((x*3+y*5+((x>>5)^(y>>4))*17)&255, (x*2+y*7+((x*y)>>10))&255, (x*11+y*3+((x+y)>>3)*9)&255))
    write_ppm(TMP / "green.ppm", w, h, lambda x,y: ((g := (x*3+y*5+((x>>4)^(y>>4))*7)&255), g, g))
    colors=[(10,20,30),(230,40,80),(20,220,60),(80,90,240),(240,210,20),(160,30,200),(30,200,210),(245,245,245)]
    write_ppm(TMP / "palette.ppm", w, h, lambda x,y: colors[((x>>5)+(y>>5)*3)&7])
    for src, dst in (("large.ppm", generic),("green.ppm",green),("palette.ppm",palette)):
        run(["cwebp","-quiet","-lossless","-z","9",str(TMP/src),"-o",str(dst)])
    return {"large":generic,"green":green,"palette":palette}


BENCH = r'''use image_webp::WebPDecoder;use std::{hint::black_box,io::Cursor,time::Instant};
fn d(x:&[u8])->Vec<u8>{let mut q=WebPDecoder::new(Cursor::new(x)).unwrap();let mut b=vec![0;q.output_buffer_size().unwrap()];q.read_image(&mut b).unwrap();b}
fn h(x:&[u8])->u64{d(x).iter().fold(0xcbf29ce484222325u64,|a,&z|(a^z as u64).wrapping_mul(1099511628211))}
fn main(){let mut a=std::env::args().skip(1);let m=a.next().unwrap();let n:usize=a.next().unwrap().parse().unwrap();let ps:Vec<_>=a.collect();let ds:Vec<Vec<u8>>=ps.iter().map(std::fs::read).collect::<Result<_,_>>().unwrap();if m=="h"{for x in&ds{println!("{:016x}",h(x))}return}for x in&ds{black_box(d(x));}let t=Instant::now();for _ in 0..n{for x in&ds{black_box(d(x));}}println!("{:.3}",t.elapsed().as_secs_f64()*1e6/(n*ds.len())as f64)}
'''


def build(root):
    (root/"examples").mkdir(exist_ok=True); (root/"examples/vp8l_transform_closure.rs").write_text(BENCH)
    env=os.environ.copy();env["RUSTFLAGS"]="-C target-cpu=native"
    run(["cargo","build","--release","--example","vp8l_transform_closure","-q"],cwd=root,env=env)
    return root/"target/release/examples/vp8l_transform_closure"


def invoke(bin, mode, n, paths):
    return run(["taskset","-c","0",str(bin),mode,str(n),*[str(x) for x in paths]],capture=True)


def main():
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    roots={n:prepare_tree(n) for n in ["base",*VARIANTS]}; rels=corpus(roots["base"]); fx=fixtures(); bins={n:build(r) for n,r in roots.items()}
    base_paths=[roots["base"]/r for r in rels]+list(fx.values()); base_hash=invoke(bins["base"],"h",1,base_paths)
    for n in VARIANTS:
        paths=[roots[n]/r for r in rels]+list(fx.values())
        if invoke(bins[n],"h",1,paths)!=base_hash: raise SystemExit(f"hash mismatch {n}")
    rows=[]; rounds=11
    for rnd in range(1,rounds+1):
        order=["base",*VARIANTS] if rnd%2 else [*reversed(VARIANTS),"base"]
        for n in order:
            rows.append(("corpus",rnd,n,float(invoke(bins[n],"bench",45,[roots[n]/r for r in rels]))))
            rows.append(("large",rnd,n,float(invoke(bins[n],"bench",3,[fx["large"]]))))
        for n in ("base","green","all"):
            rows.append(("green",rnd,n,float(invoke(bins[n],"bench",3,[fx["green"]]))))
        for n in ("base","palette_stack","palette_noscratch","palette_both","all"):
            rows.append(("palette",rnd,n,float(invoke(bins[n],"bench",3,[fx["palette"]]))))
    rr={};vals={}
    for w,r,n,x in rows: rr.setdefault((w,r),{})[n]=x;vals.setdefault((w,n),[]).append(x)
    cpu=run(["bash","-lc","lscpu | sed -n 's/^Model name:[[:space:]]*//p'"],capture=True)
    lines=["# VP8L transform closure matrix","",f"- baseline: `{BASE}`",f"- CPU: `{cpu}`",f"- static VP8L fixtures: `{len(rels)}`","- all candidates: decoded hashes match; cargo test and Rust 1.80.1 build pass","","| workload | candidate | paired median | positive | range |","|---|---|---:|---:|---:|"]
    for w,names in (("corpus",VARIANTS),("large",VARIANTS),("green",["green","all"]),("palette",["palette_stack","palette_noscratch","palette_both","all"])):
        for n in names:
            ratios=[z["base"]/z[n] for (ww,_),z in sorted(rr.items()) if ww==w]
            lines.append(f"| {w} | {n} | {statistics.median(ratios):.4f}x | {sum(x>1 for x in ratios)}/{len(ratios)} | {min(ratios):.4f}–{max(ratios):.4f}x |")
    Path("benchmark-vp8l-transform-closure-v2.md").write_text("\n".join(lines)+"\n");print("\n".join(lines))

if __name__=="__main__": main()
