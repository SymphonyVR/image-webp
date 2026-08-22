from pathlib import Path

p = Path("src/lossless/decoder/reverse_transform.rs")
s = p.read_text()

start = s.index("pub(crate) fn apply_predictor_transform(")
end = s.index("pub fn apply_predictor_transform_0", start)
new_predictor = r'''pub(crate) fn apply_predictor_transform(
    image_data: &mut [u8],
    width: u16,
    height: u16,
    size_bits: u8,
    predictor_data: &[u8],
) -> Result<(), DecodingError> {
    apply_predictor_transform_rows(
        image_data,
        width,
        height,
        size_bits,
        predictor_data,
        0,
        height,
    )
}

pub(crate) fn apply_predictor_transform_rows(
    image_data: &mut [u8],
    width: u16,
    height: u16,
    size_bits: u8,
    predictor_data: &[u8],
    start_row: u16,
    end_row: u16,
) -> Result<(), DecodingError> {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);
    let height = usize::from(height);
    let start_row = usize::from(start_row);
    let end_row = usize::from(end_row);

    assert!(start_row <= end_row && end_row <= height);
    if start_row == end_row {
        return Ok(());
    }

    // The first row is reconstructed from the left pixel only.
    if start_row == 0 {
        image_data[3] = image_data[3].wrapping_add(255);
        apply_predictor_transform_1(image_data, 4..width * 4, width);
    }

    let first_predicted_row = start_row.max(1);

    // Reconstruct the left border for this row batch. Previous batches have
    // already reconstructed the row immediately above this batch.
    for y in first_predicted_row..end_row {
        for i in 0..4 {
            image_data[y * width * 4 + i] =
                image_data[y * width * 4 + i].wrapping_add(image_data[(y - 1) * width * 4 + i]);
        }
    }

    for y in first_predicted_row..end_row {
        for block_x in 0..block_xsize {
            let block_index = (y >> size_bits) * block_xsize + block_x;
            let predictor = predictor_data[block_index * 4 + 1];
            let start_index = (y * width + (block_x << size_bits).max(1)) * 4;
            let end_index = (y * width + ((block_x + 1) << size_bits).min(width)) * 4;

            match predictor {
                0 => apply_predictor_transform_0(image_data, start_index..end_index, width),
                1 => apply_predictor_transform_1(image_data, start_index..end_index, width),
                2 => apply_predictor_transform_2(image_data, start_index..end_index, width),
                3 => apply_predictor_transform_3(image_data, start_index..end_index, width),
                4 => apply_predictor_transform_4(image_data, start_index..end_index, width),
                5 => apply_predictor_transform_5(image_data, start_index..end_index, width),
                6 => apply_predictor_transform_6(image_data, start_index..end_index, width),
                7 => apply_predictor_transform_7(image_data, start_index..end_index, width),
                8 => apply_predictor_transform_8(image_data, start_index..end_index, width),
                9 => apply_predictor_transform_9(image_data, start_index..end_index, width),
                10 => apply_predictor_transform_10(image_data, start_index..end_index, width),
                11 => apply_predictor_transform_11(image_data, start_index..end_index, width),
                12 => apply_predictor_transform_12(image_data, start_index..end_index, width),
                13 => apply_predictor_transform_13(image_data, start_index..end_index, width),
                _ => {}
            }
        }
    }

    Ok(())
}
'''
s = s[:start] + new_predictor + s[end:]

start = s.index("pub(crate) fn apply_color_transform(")
end = s.index("pub(crate) fn apply_color_indexing_transform(", start)
new_color = r'''pub(crate) fn apply_color_transform(
    image_data: &mut [u8],
    width: u16,
    size_bits: u8,
    transform_data: &[u8],
) {
    let row_bytes = usize::from(width) * 4;
    let height = image_data.len() / row_bytes;
    apply_color_transform_rows(
        image_data,
        width,
        size_bits,
        transform_data,
        0,
        height as u16,
    );
}

pub(crate) fn apply_color_transform_rows(
    image_data: &mut [u8],
    width: u16,
    size_bits: u8,
    transform_data: &[u8],
    start_row: u16,
    end_row: u16,
) {
    let block_xsize = usize::from(subsample_size(width, size_bits));
    let width = usize::from(width);
    let start_row = usize::from(start_row);
    let end_row = usize::from(end_row);
    let row_bytes = width * 4;

    assert!(start_row <= end_row && end_row * row_bytes <= image_data.len());
    let rows = &mut image_data[start_row * row_bytes..end_row * row_bytes];

    for (row_offset, row) in rows.chunks_exact_mut(row_bytes).enumerate() {
        let y = start_row + row_offset;
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
    apply_subtract_green_transform_rows(image_data, 0, image_data.len() / 4);
}

pub(crate) fn apply_subtract_green_transform_rows(
    image_data: &mut [u8],
    start_pixel: usize,
    end_pixel: usize,
) {
    assert!(start_pixel <= end_pixel && end_pixel * 4 <= image_data.len());
    for pixel in image_data[start_pixel * 4..end_pixel * 4].chunks_exact_mut(4) {
        pixel[0] = pixel[0].wrapping_add(pixel[1]);
        pixel[2] = pixel[2].wrapping_add(pixel[1]);
    }
}

'''
s = s[:start] + new_color + s[end:]

# Add equivalence tests before the existing benchmark module.
marker = '#[cfg(all(test, feature = "_benchmarks"))]\nmod benches {'
tests = r'''#[cfg(test)]
mod row_batch_tests {
    use super::*;

    fn bytes(len: usize, seed: &mut u32) -> Vec<u8> {
        (0..len)
            .map(|_| {
                *seed = seed.wrapping_mul(1664525).wrapping_add(1013904223);
                (*seed >> 24) as u8
            })
            .collect()
    }

    #[test]
    fn row_batched_transforms_match_whole_image_transforms() {
        let width = 67u16;
        let height = 35u16;
        let size_bits = 3u8;
        let mut seed = 0x9284_17c3;

        let source = bytes(usize::from(width) * usize::from(height) * 4, &mut seed);
        let block_xsize = usize::from(subsample_size(width, size_bits));
        let block_ysize = usize::from(subsample_size(height, size_bits));
        let mut predictor_data = bytes(block_xsize * block_ysize * 4, &mut seed);
        for predictor in predictor_data.chunks_exact_mut(4) {
            predictor[1] %= 14;
        }
        let color_data = bytes(block_xsize * block_ysize * 4, &mut seed);

        let mut expected = source.clone();
        apply_predictor_transform(
            &mut expected,
            width,
            height,
            size_bits,
            &predictor_data,
        )
        .unwrap();
        apply_color_transform(&mut expected, width, size_bits, &color_data);
        apply_subtract_green_transform(&mut expected);

        let mut batched = source;
        let row_pixels = usize::from(width);
        let mut start = 0u16;
        while start < height {
            let end = (start + 16).min(height);
            apply_predictor_transform_rows(
                &mut batched,
                width,
                height,
                size_bits,
                &predictor_data,
                start,
                end,
            )
            .unwrap();
            apply_color_transform_rows(
                &mut batched,
                width,
                size_bits,
                &color_data,
                start,
                end,
            );
            apply_subtract_green_transform_rows(
                &mut batched,
                usize::from(start) * row_pixels,
                usize::from(end) * row_pixels,
            );
            start = end;
        }

        assert_eq!(expected, batched);
    }
}

''' + marker
if marker not in s:
    raise SystemExit("benchmark module marker not found")
s = s.replace(marker, tests, 1)
p.write_text(s)

p = Path("src/lossless/decoder/mod.rs")
s = p.read_text()
old_import = '''use reverse_transform::{
    apply_color_indexing_transform, apply_color_transform, apply_predictor_transform,
    apply_subtract_green_transform, TransformType,
};
'''
new_import = '''use reverse_transform::{
    apply_color_indexing_transform, apply_color_transform, apply_color_transform_rows,
    apply_predictor_transform, apply_predictor_transform_rows, apply_subtract_green_transform,
    apply_subtract_green_transform_rows, TransformType,
};
'''
if old_import not in s:
    raise SystemExit("reverse-transform import marker not found")
s = s.replace(old_import, new_import, 1)

old_loop_start = s.index("        let mut image_size = transformed_size;\n        let mut width = transformed_width;\n        for &trans_index in self.transform_order.iter().rev() {")
old_loop_end = s.index("\n\n        Ok(())", old_loop_start)
old_loop = s[old_loop_start:old_loop_end]
new_loop = r'''        let has_color_indexing = self.transform_order.iter().any(|&trans_index| {
            matches!(
                self.transforms[usize::from(trans_index)].as_ref(),
                Some(TransformType::ColorIndexingTransform { .. })
            )
        });

        if !has_color_indexing {
            // Keep the active inverse-transform working set cache-local. The
            // entropy decoder still owns the full output buffer; only the
            // inverse-transform traversal is batched here.
            const ROW_BATCH: u16 = 16;
            let row_pixels = usize::from(transformed_width);
            let mut start_row = 0u16;
            while start_row < self.height {
                let end_row = (start_row + ROW_BATCH).min(self.height);
                for &trans_index in self.transform_order.iter().rev() {
                    let transform = self.transforms[usize::from(trans_index)].as_ref().unwrap();
                    match transform {
                        TransformType::PredictorTransform {
                            size_bits,
                            predictor_data,
                        } => apply_predictor_transform_rows(
                            &mut buf[..transformed_size],
                            transformed_width,
                            self.height,
                            *size_bits,
                            predictor_data,
                            start_row,
                            end_row,
                        )?,
                        TransformType::ColorTransform {
                            size_bits,
                            transform_data,
                        } => apply_color_transform_rows(
                            &mut buf[..transformed_size],
                            transformed_width,
                            *size_bits,
                            transform_data,
                            start_row,
                            end_row,
                        ),
                        TransformType::SubtractGreen => apply_subtract_green_transform_rows(
                            &mut buf[..transformed_size],
                            usize::from(start_row) * row_pixels,
                            usize::from(end_row) * row_pixels,
                        ),
                        TransformType::ColorIndexingTransform { .. } => unreachable!(),
                    }
                }
                start_row = end_row;
            }
        } else {
''' + old_loop + r'''
        }
'''
s = s[:old_loop_start] + new_loop + s[old_loop_end:]
p.write_text(s)
