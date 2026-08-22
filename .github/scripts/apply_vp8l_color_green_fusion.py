from pathlib import Path

p = Path("src/lossless/decoder/reverse_transform.rs")
s = p.read_text()

old = '''pub(crate) fn apply_color_transform(
    image_data: &mut [u8],
    width: u16,
    size_bits: u8,
    transform_data: &[u8],
) {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);

    for (y, row) in image_data.chunks_exact_mut(width * 4).enumerate() {
        let row_transform_data_start = (y >> size_bits) * block_xsize * 4;
        // the length of block_tf_data should be `block_xsize * 4`, so we could slice it with [..block_xsize * 4]
        // but there is no point - `.zip()` runs until either of the iterators is consumed,
        // so the extra slicing operation would be doing more work for no reason
        let row_tf_data = &transform_data[row_transform_data_start..];

        for (block, transform) in row
            .chunks_mut(4 << size_bits)
            .zip(row_tf_data.chunks_exact(4))
        {
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
    }
}

pub(crate) fn apply_subtract_green_transform(image_data: &mut [u8]) {
    for pixel in image_data.chunks_exact_mut(4) {
        pixel[0] = pixel[0].wrapping_add(pixel[1]);
        pixel[2] = pixel[2].wrapping_add(pixel[1]);
    }
}
'''
new = '''#[inline]
fn apply_color_transform_pixel(pixel: &mut [u8], red_to_blue: i8, green_to_blue: i8, green_to_red: i8) {
    let green = u32::from(pixel[1]);
    let mut temp_red = u32::from(pixel[0]);
    let mut temp_blue = u32::from(pixel[2]);

    temp_red += color_transform_delta(green_to_red, green as i8);
    temp_blue += color_transform_delta(green_to_blue, green as i8);
    temp_blue += color_transform_delta(red_to_blue, temp_red as i8);

    pixel[0] = (temp_red & 0xff) as u8;
    pixel[2] = (temp_blue & 0xff) as u8;
}

#[inline]
fn apply_subtract_green_pixel(pixel: &mut [u8]) {
    pixel[0] = pixel[0].wrapping_add(pixel[1]);
    pixel[2] = pixel[2].wrapping_add(pixel[1]);
}

fn apply_color_transform_impl<const SUBTRACT_BEFORE_COLOR: bool, const SUBTRACT_AFTER_COLOR: bool>(
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
            let red_to_blue = transform[0] as i8;
            let green_to_blue = transform[1] as i8;
            let green_to_red = transform[2] as i8;

            for pixel in block.chunks_exact_mut(4) {
                if SUBTRACT_BEFORE_COLOR {
                    apply_subtract_green_pixel(pixel);
                }
                apply_color_transform_pixel(pixel, red_to_blue, green_to_blue, green_to_red);
                if SUBTRACT_AFTER_COLOR {
                    apply_subtract_green_pixel(pixel);
                }
            }
        }
    }
}

pub(crate) fn apply_color_transform(
    image_data: &mut [u8],
    width: u16,
    size_bits: u8,
    transform_data: &[u8],
) {
    apply_color_transform_impl::<false, false>(image_data, width, size_bits, transform_data);
}

/// Applies adjacent color and subtract-green inverse transforms in one image walk.
pub(crate) fn apply_color_transform_and_subtract_green<const SUBTRACT_BEFORE_COLOR: bool>(
    image_data: &mut [u8],
    width: u16,
    size_bits: u8,
    transform_data: &[u8],
) {
    apply_color_transform_impl::<SUBTRACT_BEFORE_COLOR, { !SUBTRACT_BEFORE_COLOR }>(
        image_data,
        width,
        size_bits,
        transform_data,
    );
}

pub(crate) fn apply_subtract_green_transform(image_data: &mut [u8]) {
    for pixel in image_data.chunks_exact_mut(4) {
        apply_subtract_green_pixel(pixel);
    }
}
'''
if old not in s:
    raise SystemExit("color/subtract transform block marker missing")
s = s.replace(old, new, 1)

marker = '''#[cfg(all(test, feature = "_benchmarks"))]
mod benches {
'''
tests = '''#[cfg(test)]
mod fusion_tests {
    use super::*;

    fn data(len: usize, seed: &mut u32) -> Vec<u8> {
        (0..len)
            .map(|_| {
                *seed = seed.wrapping_mul(1664525).wrapping_add(1013904223);
                (*seed >> 24) as u8
            })
            .collect()
    }

    #[test]
    fn fused_color_and_subtract_green_matches_sequential_orders() {
        let width = 37u16;
        let height = 19usize;
        let size_bits = 3u8;
        let block_xsize = usize::from(subsample_size(width, size_bits));
        let block_ysize = height.div_ceil(1usize << size_bits);
        let mut seed = 0x72c4_19a5;
        let source = data(usize::from(width) * height * 4, &mut seed);
        let transform_data = data(block_xsize * block_ysize * 4, &mut seed);

        let mut expected = source.clone();
        apply_subtract_green_transform(&mut expected);
        apply_color_transform(&mut expected, width, size_bits, &transform_data);
        let mut fused = source.clone();
        apply_color_transform_and_subtract_green::<true>(
            &mut fused,
            width,
            size_bits,
            &transform_data,
        );
        assert_eq!(expected, fused);

        let mut expected = source.clone();
        apply_color_transform(&mut expected, width, size_bits, &transform_data);
        apply_subtract_green_transform(&mut expected);
        let mut fused = source;
        apply_color_transform_and_subtract_green::<false>(
            &mut fused,
            width,
            size_bits,
            &transform_data,
        );
        assert_eq!(expected, fused);
    }
}

''' + marker
if marker not in s:
    raise SystemExit("benchmark module marker missing")
s = s.replace(marker, tests, 1)
p.write_text(s)

p = Path("src/lossless/decoder/mod.rs")
s = p.read_text()
old = '''use reverse_transform::{
    apply_color_indexing_transform, apply_color_transform, apply_predictor_transform,
    apply_subtract_green_transform, TransformType,
};
'''
new = '''use reverse_transform::{
    apply_color_indexing_transform, apply_color_transform,
    apply_color_transform_and_subtract_green, apply_predictor_transform,
    apply_subtract_green_transform, TransformType,
};
'''
if old not in s:
    raise SystemExit("reverse_transform import marker missing")
s = s.replace(old, new, 1)

old = '''        let mut image_size = transformed_size;
        let mut width = transformed_width;
        for &trans_index in self.transform_order.iter().rev() {
            let transform = self.transforms[usize::from(trans_index)].as_ref().unwrap();
            match transform {
                TransformType::PredictorTransform {
                    size_bits,
                    predictor_data,
                } => apply_predictor_transform(
                    &mut buf[..image_size],
                    width,
                    self.height,
                    *size_bits,
                    predictor_data,
                )?,
                TransformType::ColorTransform {
                    size_bits,
                    transform_data,
                } => {
                    apply_color_transform(
                        &mut buf[..image_size],
                        width,
                        *size_bits,
                        transform_data,
                    );
                }
                TransformType::SubtractGreen => {
                    apply_subtract_green_transform(&mut buf[..image_size]);
                }
                TransformType::ColorIndexingTransform {
                    table_size,
                    table_data,
                } => {
                    width = self.width;
                    image_size = usize::from(width) * usize::from(self.height) * 4;
                    apply_color_indexing_transform(
                        buf,
                        width,
                        self.height,
                        *table_size,
                        table_data,
                    );
                }
            }
        }
'''
new = '''        let mut image_size = transformed_size;
        let mut width = transformed_width;
        let mut transforms = self.transform_order.iter().rev().copied().peekable();
        while let Some(trans_index) = transforms.next() {
            let transform = self.transforms[usize::from(trans_index)].as_ref().unwrap();
            match transform {
                TransformType::PredictorTransform {
                    size_bits,
                    predictor_data,
                } => apply_predictor_transform(
                    &mut buf[..image_size],
                    width,
                    self.height,
                    *size_bits,
                    predictor_data,
                )?,
                TransformType::ColorTransform {
                    size_bits,
                    transform_data,
                } => {
                    let subtract_after = transforms.peek().is_some_and(|&next_index| {
                        matches!(
                            self.transforms[usize::from(*next_index)].as_ref(),
                            Some(TransformType::SubtractGreen)
                        )
                    });
                    if subtract_after {
                        apply_color_transform_and_subtract_green::<false>(
                            &mut buf[..image_size],
                            width,
                            *size_bits,
                            transform_data,
                        );
                        transforms.next();
                    } else {
                        apply_color_transform(
                            &mut buf[..image_size],
                            width,
                            *size_bits,
                            transform_data,
                        );
                    }
                }
                TransformType::SubtractGreen => {
                    let next_color = transforms.peek().and_then(|&next_index| {
                        match self.transforms[usize::from(*next_index)].as_ref() {
                            Some(TransformType::ColorTransform {
                                size_bits,
                                transform_data,
                            }) => Some((*size_bits, transform_data.as_slice())),
                            _ => None,
                        }
                    });
                    if let Some((size_bits, transform_data)) = next_color {
                        apply_color_transform_and_subtract_green::<true>(
                            &mut buf[..image_size],
                            width,
                            size_bits,
                            transform_data,
                        );
                        transforms.next();
                    } else {
                        apply_subtract_green_transform(&mut buf[..image_size]);
                    }
                }
                TransformType::ColorIndexingTransform {
                    table_size,
                    table_data,
                } => {
                    width = self.width;
                    image_size = usize::from(width) * usize::from(self.height) * 4;
                    apply_color_indexing_transform(
                        buf,
                        width,
                        self.height,
                        *table_size,
                        table_data,
                    );
                }
            }
        }
'''
if old not in s:
    raise SystemExit("decode transform loop marker missing")
s = s.replace(old, new, 1)
p.write_text(s)
