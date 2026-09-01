#!/usr/bin/env python3
from pathlib import Path
p=Path('src/lossless/decoder/reverse_transform.rs')
s=p.read_text()

def replace_fn(s,n,nextn,body):
    a=s.index(f'pub fn apply_predictor_transform_{n}(')
    b=s.index(f'pub fn apply_predictor_transform_{nextn}(',a)
    return s[:a]+body+s[b:]

helper='''#[inline(always)]\nfn load_predictor_u32(pixel: &[u8]) -> u32 {\n    u32::from_le_bytes(pixel[..4].try_into().unwrap())\n}\n\n#[inline(always)]\nfn store_predictor_u32(pixel: &mut [u8], value: u32) {\n    pixel[..4].copy_from_slice(&value.to_le_bytes());\n}\n\n#[inline(always)]\nfn add_predictor_u32(a: u32, b: u32) -> u32 {\n    let hi = (a & 0xff00_ff00).wrapping_add(b & 0xff00_ff00);\n    let lo = (a & 0x00ff_00ff).wrapping_add(b & 0x00ff_00ff);\n    (hi & 0xff00_ff00) | (lo & 0x00ff_00ff)\n}\n\n'''
marker='''fn average2_autovec(a: u8, b: u8) -> u8 {\n    (a & b) + ((a ^ b) >> 1)\n}\n'''
if marker not in s:
    raise SystemExit('average2_autovec marker not found')
s=s.replace(marker,marker+'\n'+helper,1)

b2='''pub fn apply_predictor_transform_2(image_data: &mut [u8], range: Range<usize>, width: usize) {\n    let (old, current) = image_data[..range.end].split_at_mut(range.start);\n    let top = &old[range.start - width * 4..];\n    for (pixel, predictor) in current.chunks_exact_mut(4).zip(top.chunks_exact(4)) {\n        store_predictor_u32(\n            pixel,\n            add_predictor_u32(load_predictor_u32(pixel), load_predictor_u32(predictor)),\n        );\n    }\n}\n'''
b3='''pub fn apply_predictor_transform_3(image_data: &mut [u8], range: Range<usize>, width: usize) {\n    let (old, current) = image_data[..range.end].split_at_mut(range.start);\n    let top_right = &old[range.start - width * 4 + 4..];\n    for (pixel, predictor) in current\n        .chunks_exact_mut(4)\n        .zip(top_right.chunks_exact(4))\n    {\n        store_predictor_u32(\n            pixel,\n            add_predictor_u32(load_predictor_u32(pixel), load_predictor_u32(predictor)),\n        );\n    }\n}\n'''
b4='''pub fn apply_predictor_transform_4(image_data: &mut [u8], range: Range<usize>, width: usize) {\n    let (old, current) = image_data[..range.end].split_at_mut(range.start);\n    let top_left = &old[range.start - width * 4 - 4..];\n    for (pixel, predictor) in current.chunks_exact_mut(4).zip(top_left.chunks_exact(4)) {\n        store_predictor_u32(\n            pixel,\n            add_predictor_u32(load_predictor_u32(pixel), load_predictor_u32(predictor)),\n        );\n    }\n}\n'''
s=replace_fn(s,2,3,b2)
s=replace_fn(s,3,4,b3)
s=replace_fn(s,4,5,b4)
p.write_text(s)
