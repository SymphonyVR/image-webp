use super::lossless::LosslessDecoder;
use crate::decoder::DecodingError;
use byteorder_lite::ReadBytesExt;
use std::io::{BufRead, Read};

use crate::alpha_blending::do_alpha_blending;

#[derive(Debug, Clone)]
pub(crate) struct WebPExtendedInfo {
    pub(crate) alpha: bool,

    pub(crate) canvas_width: u32,
    pub(crate) canvas_height: u32,

    #[allow(unused)]
    pub(crate) icc_profile: bool,
    pub(crate) exif_metadata: bool,
    pub(crate) xmp_metadata: bool,
    pub(crate) animation: bool,

    pub(crate) background_color: Option<[u8; 4]>,
    pub(crate) background_color_hint: [u8; 4],
}

/// Composites a frame onto a canvas.
///
/// Starts by filling the rectangle occupied by the previous frame with the background
/// color, if provided. Then copies or blends the frame onto the canvas.
#[allow(clippy::too_many_arguments)]
pub(crate) fn composite_frame(
    canvas: &mut [u8],
    canvas_width: u32,
    canvas_height: u32,
    clear_color: Option<[u8; 4]>,
    frame: &[u8],
    frame_offset_x: u32,
    frame_offset_y: u32,
    frame_width: u32,
    frame_height: u32,
    frame_has_alpha: bool,
    frame_use_alpha_blending: bool,
    previous_frame_width: u32,
    previous_frame_height: u32,
    previous_frame_offset_x: u32,
    previous_frame_offset_y: u32,
) {
    let frame_is_full_size = frame_offset_x == 0
        && frame_offset_y == 0
        && frame_width == canvas_width
        && frame_height == canvas_height;

    if frame_is_full_size && !frame_use_alpha_blending {
        if frame_has_alpha {
            canvas.copy_from_slice(frame);
        } else {
            for (input, output) in frame.chunks_exact(3).zip(canvas.chunks_exact_mut(4)) {
                output[..3].copy_from_slice(input);
                output[3] = 255;
            }
        }
        return;
    }

    // Clear rectangle occupied by previous frame.
    // The canvas is always RGBA (4 bytes/pixel) regardless of whether the
    // current frame carries alpha, so we always clear with 4-byte pixels.
    if let Some(clear_color) = clear_color {
        if frame_is_full_size {
            for pixel in canvas.chunks_exact_mut(4) {
                pixel.copy_from_slice(&clear_color);
            }
        } else {
            for y in 0..previous_frame_height as usize {
                for x in 0..previous_frame_width as usize {
                    let canvas_index = ((x + previous_frame_offset_x as usize)
                        + (y + previous_frame_offset_y as usize) * canvas_width as usize)
                        * 4;

                    let output = &mut canvas[canvas_index..][..4];
                    output.copy_from_slice(&clear_color);
                }
            }
        }
    }

    let width = frame_width.min(canvas_width.saturating_sub(frame_offset_x)) as usize;
    let height = frame_height.min(canvas_height.saturating_sub(frame_offset_y)) as usize;

    if frame_has_alpha && frame_use_alpha_blending {
        let frame_stride = frame_width as usize * 4;
        let canvas_stride = canvas_width as usize * 4;

        for y in 0..height {
            let frame_start = y * frame_stride;
            let canvas_start =
                (y + frame_offset_y as usize) * canvas_stride + frame_offset_x as usize * 4;
            let input_row = &frame[frame_start..][..width * 4];
            let output_row = &mut canvas[canvas_start..][..width * 4];

            for (input, output) in input_row
                .chunks_exact(4)
                .zip(output_row.chunks_exact_mut(4))
            {
                match input[3] {
                    0 => {}
                    255 => output.copy_from_slice(input),
                    _ => {
                        let blended = do_alpha_blending(
                            input.try_into().unwrap(),
                            output.try_into().unwrap(),
                        );
                        output.copy_from_slice(&blended);
                    }
                }
            }
        }
    } else if frame_has_alpha {
        for y in 0..height {
            let frame_index = (y * frame_width as usize) * 4;
            let canvas_index = (frame_offset_x as usize
                + (y + frame_offset_y as usize) * canvas_width as usize)
                * 4;

            canvas[canvas_index..][..width * 4].copy_from_slice(&frame[frame_index..][..width * 4]);
        }
    } else {
        for y in 0..height {
            let index = (y * frame_width as usize) * 3;
            let canvas_index = (frame_offset_x as usize
                + (y + frame_offset_y as usize) * canvas_width as usize)
                * 4;
            let input = &frame[index..][..width * 3];
            let output = &mut canvas[canvas_index..][..width * 4];

            for (input, output) in input.chunks_exact(3).zip(output.chunks_exact_mut(4)) {
                output[..3].copy_from_slice(input);
                output[3] = 255;
            }
        }
    }
}

fn reconstruct_alpha(data: &mut [u8], width: usize, filtering_method: FilteringMethod) {
    if data.is_empty() || width == 0 {
        return;
    }

    debug_assert_eq!(data.len() % width, 0);
    let height = data.len() / width;

    match filtering_method {
        FilteringMethod::None => {}
        FilteringMethod::Horizontal => {
            for y in 0..height {
                let row = y * width;
                if y != 0 {
                    data[row] = data[row].wrapping_add(data[row - width]);
                }
                for x in 1..width {
                    let i = row + x;
                    data[i] = data[i].wrapping_add(data[i - 1]);
                }
            }
        }
        FilteringMethod::Vertical => {
            for x in 1..width {
                data[x] = data[x].wrapping_add(data[x - 1]);
            }
            for y in 1..height {
                let row = y * width;
                for x in 0..width {
                    let i = row + x;
                    data[i] = data[i].wrapping_add(data[i - width]);
                }
            }
        }
        FilteringMethod::Gradient => {
            for x in 1..width {
                data[x] = data[x].wrapping_add(data[x - 1]);
            }
            for y in 1..height {
                let row = y * width;
                data[row] = data[row].wrapping_add(data[row - width]);
                for x in 1..width {
                    let i = row + x;
                    let predictor = i16::from(data[i - 1]) + i16::from(data[i - width])
                        - i16::from(data[i - width - 1]);
                    data[i] = data[i].wrapping_add(predictor.clamp(0, 255) as u8);
                }
            }
        }
    }
}

pub(crate) fn read_extended_header<R: Read>(
    reader: &mut R,
) -> Result<WebPExtendedInfo, DecodingError> {
    let chunk_flags = reader.read_u8()?;

    let icc_profile = chunk_flags & 0b00100000 != 0;
    let alpha = chunk_flags & 0b00010000 != 0;
    let exif_metadata = chunk_flags & 0b00001000 != 0;
    let xmp_metadata = chunk_flags & 0b00000100 != 0;
    let animation = chunk_flags & 0b00000010 != 0;

    // reserved bytes are ignored
    let _reserved_bytes = read_3_bytes(reader)?;

    let canvas_width = read_3_bytes(reader)? + 1;
    let canvas_height = read_3_bytes(reader)? + 1;

    //product of canvas dimensions cannot be larger than u32 max
    if u32::checked_mul(canvas_width, canvas_height).is_none() {
        return Err(DecodingError::ImageTooLarge);
    }

    let info = WebPExtendedInfo {
        icc_profile,
        alpha,
        exif_metadata,
        xmp_metadata,
        animation,
        canvas_width,
        canvas_height,
        background_color_hint: [0; 4],
        background_color: None,
    };

    Ok(info)
}

pub(crate) fn read_3_bytes<R: Read>(reader: &mut R) -> Result<u32, DecodingError> {
    let mut buffer: [u8; 3] = [0; 3];
    reader.read_exact(&mut buffer)?;
    let value: u32 =
        (u32::from(buffer[2]) << 16) | (u32::from(buffer[1]) << 8) | u32::from(buffer[0]);
    Ok(value)
}

#[derive(Debug)]
pub(crate) struct AlphaChunk {
    _preprocessing: bool,
    pub(crate) data: Vec<u8>,
}

#[derive(Debug, Copy, Clone)]
pub(crate) enum FilteringMethod {
    None,
    Horizontal,
    Vertical,
    Gradient,
}

pub(crate) fn read_alpha_chunk<R: BufRead>(
    reader: &mut R,
    width: u16,
    height: u16,
) -> Result<AlphaChunk, DecodingError> {
    let info_byte = reader.read_u8()?;

    let preprocessing = (info_byte & 0b00110000) >> 4;
    let filtering = (info_byte & 0b00001100) >> 2;
    let compression = info_byte & 0b00000011;

    let preprocessing = match preprocessing {
        0 => false,
        1 => true,
        _ => return Err(DecodingError::InvalidAlphaPreprocessing),
    };

    let filtering_method = match filtering {
        0 => FilteringMethod::None,
        1 => FilteringMethod::Horizontal,
        2 => FilteringMethod::Vertical,
        3 => FilteringMethod::Gradient,
        _ => unreachable!(),
    };

    let lossless_compression = match compression {
        0 => false,
        1 => true,
        _ => return Err(DecodingError::InvalidCompressionMethod),
    };

    let mut data = if lossless_compression {
        let mut decoder = LosslessDecoder::new(reader);

        let mut data = vec![0; usize::from(width) * usize::from(height) * 4];
        decoder.decode_frame(u32::from(width), u32::from(height), true, &mut data)?;

        let mut green = Vec::with_capacity(usize::from(width) * usize::from(height));
        green.extend(data.chunks_exact(4).map(|rgba| rgba[1]));
        green
    } else {
        let mut framedata = vec![0; width as usize * height as usize];
        reader.read_exact(&mut framedata)?;
        framedata
    };

    reconstruct_alpha(&mut data, usize::from(width), filtering_method);

    let chunk = AlphaChunk {
        _preprocessing: preprocessing,
        data,
    };

    Ok(chunk)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reconstruct_alpha_filters() {
        let residuals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
        let cases = [
            (
                FilteringMethod::None,
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ),
            (
                FilteringMethod::Horizontal,
                [1, 3, 6, 10, 6, 12, 19, 27, 15, 25, 36, 48],
            ),
            (
                FilteringMethod::Vertical,
                [1, 3, 6, 10, 6, 9, 13, 18, 15, 19, 24, 30],
            ),
            (
                FilteringMethod::Gradient,
                [1, 3, 6, 10, 6, 14, 24, 36, 15, 33, 54, 78],
            ),
        ];

        for (filter, expected) in cases {
            let mut data = residuals;
            reconstruct_alpha(&mut data, 4, filter);
            assert_eq!(data, expected);
        }
    }

    #[test]
    fn binary_alpha_blend_selects_exact_pixel() {
        let mut canvas = vec![10, 20, 30, 40, 50, 60, 70, 80];
        let frame = vec![1, 2, 3, 0, 200, 201, 202, 255];
        composite_frame(
            &mut canvas,
            2,
            1,
            None,
            &frame,
            0,
            0,
            2,
            1,
            true,
            true,
            0,
            0,
            0,
            0,
        );
        assert_eq!(canvas, [10, 20, 30, 40, 200, 201, 202, 255]);
    }

    /// Regression test: clearing the canvas for a non-alpha frame used 3-byte
    /// stride on the always-RGBA canvas, corrupting pixel alignment.
    #[test]
    fn dispose_clear_fullsize_rgb_frame() {
        let w = 4u32;
        let h = 4u32;
        let mut canvas = vec![0xAA_u8; (w * h * 4) as usize];
        let frame = vec![0xFF_u8; (w * h * 3) as usize];

        composite_frame(
            &mut canvas,
            w,
            h,
            Some([0, 0, 0, 0]),
            &frame,
            0,
            0,
            w,
            h,
            false, // frame_has_alpha
            true,  // frame_use_alpha_blending (forces slow path)
            w,
            h,
            0,
            0,
        );

        for (i, pixel) in canvas.chunks_exact(4).enumerate() {
            assert_eq!(
                pixel,
                [0xFF, 0xFF, 0xFF, 0xFF],
                "pixel {i} corrupted: {pixel:?}"
            );
        }
    }

    /// Regression test: sub-frame clear used 3-byte indexing on RGBA canvas.
    #[test]
    fn dispose_clear_subframe_rgb_frame() {
        let canvas_w = 8u32;
        let canvas_h = 8u32;
        let mut canvas = vec![0xAA_u8; (canvas_w * canvas_h * 4) as usize];

        let prev_x = 2u32;
        let prev_y = 2u32;
        let prev_w = 4u32;
        let prev_h = 4u32;

        let frame_w = 4u32;
        let frame_h = 4u32;
        let frame = vec![0xFF_u8; (frame_w * frame_h * 3) as usize];

        composite_frame(
            &mut canvas,
            canvas_w,
            canvas_h,
            Some([0, 0, 0, 0]),
            &frame,
            0,
            0,
            frame_w,
            frame_h,
            false,
            true,
            prev_w,
            prev_h,
            prev_x,
            prev_y,
        );

        let stride = canvas_w as usize * 4;

        // Previous-frame rectangle should be cleared to [0,0,0,0].
        // Only check the region cleared but NOT overwritten by the new frame.
        for y in prev_y as usize..(prev_y + prev_h) as usize {
            for x in prev_x as usize..(prev_x + prev_w) as usize {
                let idx = y * stride + x * 4;
                let pixel = &canvas[idx..idx + 4];
                if x >= frame_w as usize || y >= frame_h as usize {
                    assert_eq!(
                        pixel,
                        [0, 0, 0, 0],
                        "prev-frame pixel ({x},{y}) not cleared: {pixel:?}"
                    );
                }
            }
        }

        // New frame region should be opaque white from RGB→RGBA.
        for y in 0..frame_h as usize {
            for x in 0..frame_w as usize {
                let idx = y * stride + x * 4;
                let pixel = &canvas[idx..idx + 4];
                assert_eq!(
                    pixel,
                    [0xFF, 0xFF, 0xFF, 0xFF],
                    "new-frame pixel ({x},{y}) wrong: {pixel:?}"
                );
            }
        }

        // Pixels outside both rectangles should be untouched.
        let pixel = &canvas[7 * 4..7 * 4 + 4];
        assert_eq!(pixel, [0xAA, 0xAA, 0xAA, 0xAA], "untouched pixel modified");
    }
}
