#!/usr/bin/env python3
from pathlib import Path
p=Path('src/lossless/decoder/reverse_transform.rs');s=p.read_text()
a=s.index('pub(crate) fn apply_color_transform(');b=s.index('pub(crate) fn apply_subtract_green_transform(',a)
helper=r'''#[inline(always)]
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
body=r'''pub(crate) fn apply_color_transform(
    image_data: &mut [u8],
    width: u16,
    size_bits: u8,
    transform_data: &[u8],
) {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);

    for (y, row) in image_data.chunks_exact_mut(width * 4).enumerate() {
        let row_transform_data_start = (y >> size_bits) * block_xsize * 4;
        let row_tf_data = &transform_data[row_transform_data_start..];

        for (block, transform) in row
            .chunks_mut(4 << size_bits)
            .zip(row_tf_data.chunks_exact(4))
        {
            let red_to_blue = transform[0];
            let green_to_blue = transform[1];
            let green_to_red = transform[2];

            for pixel in block.chunks_exact_mut(4) {
                inverse_color_pixel_packed(pixel, red_to_blue, green_to_blue, green_to_red);
            }
        }
    }
}

'''
p.write_text(s[:a]+helper+body+s[b:])
