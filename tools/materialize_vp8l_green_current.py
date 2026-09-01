#!/usr/bin/env python3
from pathlib import Path

p = Path('src/lossless/decoder/reverse_transform.rs')
s = p.read_text()
a = s.index('pub(crate) fn apply_subtract_green_transform(')
b = s.index('\npub(crate) fn apply_color_indexing_transform(', a)
new = '''pub(crate) fn apply_subtract_green_transform(image_data: &mut [u8]) {
    for pixel in image_data.chunks_exact_mut(4) {
        let value = u32::from_le_bytes(pixel.try_into().unwrap());
        let green = (value >> 8) & 0xff;
        let red_blue =
            ((value & 0x00ff_00ff).wrapping_add(green | (green << 16))) & 0x00ff_00ff;
        pixel.copy_from_slice(&((value & 0xff00_ff00) | red_blue).to_le_bytes());
    }
}
'''
p.write_text(s[:a] + new + s[b:])
