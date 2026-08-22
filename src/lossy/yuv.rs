//! Utilities for doing the YUV -> RGB conversion
//! The images are encoded in the Y'CbCr format as detailed here: <https://en.wikipedia.org/wiki/YCbCr>
//! so need to be converted to RGB to be displayed
//! To do the YUV -> RGB conversion we need to first decide how to map the yuv values to the pixels
//! The y buffer is the same size as the pixel buffer so that maps 1-1 but the
//! u and v buffers are half the size of the pixel buffer so we need to scale it up
//! The simple way to upscale is just to take each u/v value and associate it with the 4
//! pixels around it e.g. for a 4x4 image:
//!
//! ||||||
//! |yyyy|
//! |yyyy|
//! |yyyy|
//! |yyyy|
//! ||||||
//!
//! |||||||
//! |uu|vv|
//! |uu|vv|
//! |||||||
//!
//! Then each of the 2x2 pixels would match the u/v from the same quadrant
//!
//! However fancy upsampling is the default for libwebp which does a little more work to make the values smoother
//! It interpolates u and v so that for e.g. the pixel 1 down and 1 from the left the u value
//! would be (9*u0 + 3*u1 + 3*u2 + u3 + 8) / 16 and similar for the other pixels
//! The edges are mirrored, so for the pixel 1 down and 0 from the left it uses (9*u0 + 3*u2 + 3*u0 + u2 + 8) / 16

/// `_mm_mulhi_epu16` emulation
fn mulhi(v: u8, coeff: u16) -> i32 {
    ((u32::from(v) * u32::from(coeff)) >> 8) as i32
}

/// This function has been rewritten to encourage auto-vectorization.
///
/// Based on [src/dsp/yuv.h](https://github.com/webmproject/libwebp/blob/8534f53960befac04c9631e6e50d21dcb42dfeaf/src/dsp/yuv.h#L79)
/// from the libwebp source.
/// ```text
/// const YUV_FIX2: i32 = 6;
/// const YUV_MASK2: i32 = (256 << YUV_FIX2) - 1;
/// fn clip(v: i32) -> u8 {
///     if (v & !YUV_MASK2) == 0 {
///         (v >> YUV_FIX2) as u8
///     } else if v < 0 {
///         0
///     } else {
///         255
///     }
/// }
/// ```
// Clippy suggests the clamp method, but it seems to optimize worse as of rustc 1.82.0 nightly.
#[allow(clippy::manual_clamp)]
fn clip(v: i32) -> u8 {
    const YUV_FIX2: i32 = 6;
    (v >> YUV_FIX2).max(0).min(255) as u8
}

#[inline(always)]
fn yuv_to_r(y: u8, v: u8) -> u8 {
    clip(mulhi(y, 19077) + mulhi(v, 26149) - 14234)
}

#[inline(always)]
fn yuv_to_g(y: u8, u: u8, v: u8) -> u8 {
    clip(mulhi(y, 19077) - mulhi(u, 6419) - mulhi(v, 13320) + 8708)
}

#[inline(always)]
fn yuv_to_b(y: u8, u: u8) -> u8 {
    clip(mulhi(y, 19077) + mulhi(u, 33050) - 17685)
}

/// Fills an rgb buffer with the image from the yuv buffers
/// Size of the buffer is assumed to be correct
/// BPP is short for bytes per pixel, allows both rgb and rgba to be decoded
pub(crate) fn fill_rgb_buffer_fancy<const BPP: usize>(
    buffer: &mut [u8],
    y_buffer: &[u8],
    u_buffer: &[u8],
    v_buffer: &[u8],
    width: usize,
    height: usize,
    buffer_width: usize,
) {
    // buffer width is always even so don't need to do div_ceil
    let chroma_buffer_width = buffer_width / 2;
    let chroma_width = width.div_ceil(2);

    // fill top row first since it only uses the top u/v row
    let top_row_y = &y_buffer[..width];
    let top_row_u = &u_buffer[..chroma_width];
    let top_row_v = &v_buffer[..chroma_width];
    let top_row_buffer = &mut buffer[..width * BPP];
    fill_row_fancy_with_1_uv_row::<BPP>(top_row_buffer, top_row_y, top_row_u, top_row_v);

    let mut main_row_chunks = buffer[width * BPP..].chunks_exact_mut(width * BPP * 2);
    // the y buffer iterator limits the end of the row iterator so we need this end index
    let end_y_index = height * buffer_width;
    let mut main_y_chunks = y_buffer[buffer_width..end_y_index].chunks_exact(buffer_width * 2);
    let mut main_u_windows = u_buffer
        .windows(chroma_buffer_width * 2)
        .step_by(chroma_buffer_width);
    let mut main_v_windows = v_buffer
        .windows(chroma_buffer_width * 2)
        .step_by(chroma_buffer_width);

    for (((row_buffer, y_rows), u_rows), v_rows) in (&mut main_row_chunks)
        .zip(&mut main_y_chunks)
        .zip(&mut main_u_windows)
        .zip(&mut main_v_windows)
    {
        let (u_row_1, u_row_2) = u_rows.split_at(chroma_buffer_width);
        let (v_row_1, v_row_2) = v_rows.split_at(chroma_buffer_width);
        let (row_buf_1, row_buf_2) = row_buffer.split_at_mut(width * BPP);
        let (y_row_1, y_row_2) = y_rows.split_at(buffer_width);
        fill_row_pair_fancy::<BPP>(
            row_buf_1,
            row_buf_2,
            &y_row_1[..width],
            &y_row_2[..width],
            &u_row_1[..chroma_width],
            &u_row_2[..chroma_width],
            &v_row_1[..chroma_width],
            &v_row_2[..chroma_width],
        );
    }

    let final_row_buffer = main_row_chunks.into_remainder();

    // if the image has even height there will be one final row with only one u/v row matching it
    if !final_row_buffer.is_empty() {
        let final_y_row = main_y_chunks.remainder();

        let chroma_height = height.div_ceil(2);
        let start_chroma_index = (chroma_height - 1) * chroma_buffer_width;

        let final_u_row = &u_buffer[start_chroma_index..];
        let final_v_row = &v_buffer[start_chroma_index..];
        fill_row_fancy_with_1_uv_row::<BPP>(
            final_row_buffer,
            &final_y_row[..width],
            &final_u_row[..chroma_width],
            &final_v_row[..chroma_width],
        );
    }
}

#[inline(always)]
fn pack_uv(u: u8, v: u8) -> u32 {
    u32::from(u) | (u32::from(v) << 16)
}

#[inline(always)]
fn interpolate_uv_square(
    top_left: u32,
    top_right: u32,
    bottom_left: u32,
    bottom_right: u32,
) -> [u32; 4] {
    let average = top_left + top_right + bottom_left + bottom_right + 0x0008_0008;
    let diagonal_12 = (average + 2 * (top_right + bottom_left)) >> 3;
    let diagonal_03 = (average + 2 * (top_left + bottom_right)) >> 3;
    [
        (diagonal_12 + top_left) >> 1,
        (diagonal_03 + top_right) >> 1,
        (diagonal_03 + bottom_left) >> 1,
        (diagonal_12 + bottom_right) >> 1,
    ]
}

#[inline(always)]
fn set_pixel_packed_uv(rgb: &mut [u8], y: u8, uv: u32) {
    set_pixel(rgb, y, (uv & 0xff) as u8, ((uv >> 16) & 0xff) as u8);
}

/// Fills two neighboring luma rows together so each 2x2 chroma square is
/// interpolated once and reused for all four output pixels.
#[allow(clippy::too_many_arguments)]
fn fill_row_pair_fancy<const BPP: usize>(
    top_buffer: &mut [u8],
    bottom_buffer: &mut [u8],
    top_y: &[u8],
    bottom_y: &[u8],
    top_u: &[u8],
    bottom_u: &[u8],
    top_v: &[u8],
    bottom_v: &[u8],
) {
    let width = top_y.len();
    debug_assert_eq!(bottom_y.len(), width);

    let mut top_left = pack_uv(top_u[0], top_v[0]);
    let mut bottom_left = pack_uv(bottom_u[0], bottom_v[0]);

    let top_edge = (3 * top_left + bottom_left + 0x0002_0002) >> 2;
    let bottom_edge = (3 * bottom_left + top_left + 0x0002_0002) >> 2;
    set_pixel_packed_uv(&mut top_buffer[..3], top_y[0], top_edge);
    set_pixel_packed_uv(&mut bottom_buffer[..3], bottom_y[0], bottom_edge);

    let last_pair = (width - 1) >> 1;
    for x in 1..=last_pair {
        let top_right = pack_uv(top_u[x], top_v[x]);
        let bottom_right = pack_uv(bottom_u[x], bottom_v[x]);
        let values = interpolate_uv_square(top_left, top_right, bottom_left, bottom_right);
        let left_pixel = 2 * x - 1;
        let right_pixel = 2 * x;

        set_pixel_packed_uv(
            &mut top_buffer[left_pixel * BPP..][..3],
            top_y[left_pixel],
            values[0],
        );
        set_pixel_packed_uv(
            &mut top_buffer[right_pixel * BPP..][..3],
            top_y[right_pixel],
            values[1],
        );
        set_pixel_packed_uv(
            &mut bottom_buffer[left_pixel * BPP..][..3],
            bottom_y[left_pixel],
            values[2],
        );
        set_pixel_packed_uv(
            &mut bottom_buffer[right_pixel * BPP..][..3],
            bottom_y[right_pixel],
            values[3],
        );

        top_left = top_right;
        bottom_left = bottom_right;
    }

    if width % 2 == 0 {
        let pixel = width - 1;
        let top_edge = (3 * top_left + bottom_left + 0x0002_0002) >> 2;
        let bottom_edge = (3 * bottom_left + top_left + 0x0002_0002) >> 2;
        set_pixel_packed_uv(&mut top_buffer[pixel * BPP..][..3], top_y[pixel], top_edge);
        set_pixel_packed_uv(
            &mut bottom_buffer[pixel * BPP..][..3],
            bottom_y[pixel],
            bottom_edge,
        );
    }
}

fn fill_row_fancy_with_1_uv_row<const BPP: usize>(
    row_buffer: &mut [u8],
    y_row: &[u8],
    u_row: &[u8],
    v_row: &[u8],
) {
    // doing left pixel first
    {
        let rgb1 = &mut row_buffer[0..3];
        let y_value = y_row[0];

        let u_value = u_row[0];
        let v_value = v_row[0];
        set_pixel(rgb1, y_value, u_value, v_value);
    }

    // two pixels at a time since they share the same u/v value
    let mut main_row_chunks = row_buffer[BPP..].chunks_exact_mut(BPP * 2);
    let mut main_y_row_chunks = y_row[1..].chunks_exact(2);

    for (((rgb, y_val), u_val), v_val) in (&mut main_row_chunks)
        .zip(&mut main_y_row_chunks)
        .zip(u_row.windows(2))
        .zip(v_row.windows(2))
    {
        {
            let rgb1 = &mut rgb[0..3];
            let y_value = y_val[0];
            // first pixel uses the first u/v as the main one
            let u_value = get_fancy_chroma_value(u_val[0], u_val[1], u_val[0], u_val[1]);
            let v_value = get_fancy_chroma_value(v_val[0], v_val[1], v_val[0], v_val[1]);
            set_pixel(rgb1, y_value, u_value, v_value);
        }
        {
            let rgb2 = &mut rgb[BPP..];
            let y_value = y_val[1];
            let u_value = get_fancy_chroma_value(u_val[1], u_val[0], u_val[1], u_val[0]);
            let v_value = get_fancy_chroma_value(v_val[1], v_val[0], v_val[1], v_val[0]);
            set_pixel(rgb2, y_value, u_value, v_value);
        }
    }

    let final_pixel = main_row_chunks.into_remainder();
    let final_y = main_y_row_chunks.remainder();

    if let (rgb, [final_y]) = (final_pixel, final_y) {
        let final_u = *u_row.last().unwrap();
        let final_v = *v_row.last().unwrap();

        set_pixel(rgb, *final_y, final_u, final_v);
    }
}

#[inline]
fn get_fancy_chroma_value(main: u8, secondary1: u8, secondary2: u8, tertiary: u8) -> u8 {
    let val0 = u16::from(main);
    let val1 = u16::from(secondary1);
    let val2 = u16::from(secondary2);
    let val3 = u16::from(tertiary);
    ((9 * val0 + 3 * val1 + 3 * val2 + val3 + 8) / 16) as u8
}

#[inline]
fn set_pixel(rgb: &mut [u8], y: u8, u: u8, v: u8) {
    rgb[0] = yuv_to_r(y, v);
    rgb[1] = yuv_to_g(y, u, v);
    rgb[2] = yuv_to_b(y, u);
}

/// Simple conversion, not currently used but could add a config to allow for using the simple
#[allow(unused)]
pub(crate) fn fill_rgb_buffer_simple<const BPP: usize>(
    buffer: &mut [u8],
    y_buffer: &[u8],
    u_buffer: &[u8],
    v_buffer: &[u8],
    width: usize,
    chroma_width: usize,
    buffer_width: usize,
) {
    let u_row_twice_iter = u_buffer
        .chunks_exact(buffer_width / 2)
        .flat_map(|n| std::iter::repeat(n).take(2));
    let v_row_twice_iter = v_buffer
        .chunks_exact(buffer_width / 2)
        .flat_map(|n| std::iter::repeat(n).take(2));

    for (((row, y_row), u_row), v_row) in buffer
        .chunks_exact_mut(width * BPP)
        .zip(y_buffer.chunks_exact(buffer_width))
        .zip(u_row_twice_iter)
        .zip(v_row_twice_iter)
    {
        fill_rgba_row_simple::<BPP>(
            &y_row[..width],
            &u_row[..chroma_width],
            &v_row[..chroma_width],
            row,
        );
    }
}

fn fill_rgba_row_simple<const BPP: usize>(
    y_vec: &[u8],
    u_vec: &[u8],
    v_vec: &[u8],
    rgba: &mut [u8],
) {
    // Fill 2 pixels per iteration: these pixels share `u` and `v` components
    let mut rgb_chunks = rgba.chunks_exact_mut(BPP * 2);
    let mut y_chunks = y_vec.chunks_exact(2);
    let mut u_iter = u_vec.iter();
    let mut v_iter = v_vec.iter();

    for (((rgb, y), &u), &v) in (&mut rgb_chunks)
        .zip(&mut y_chunks)
        .zip(&mut u_iter)
        .zip(&mut v_iter)
    {
        let coeffs = [
            mulhi(v, 26149),
            mulhi(u, 6419),
            mulhi(v, 13320),
            mulhi(u, 33050),
        ];

        let get_r = |y: u8| clip(mulhi(y, 19077) + coeffs[0] - 14234);
        let get_g = |y: u8| clip(mulhi(y, 19077) - coeffs[1] - coeffs[2] + 8708);
        let get_b = |y: u8| clip(mulhi(y, 19077) + coeffs[3] - 17685);

        let rgb1 = &mut rgb[0..3];
        rgb1[0] = get_r(y[0]);
        rgb1[1] = get_g(y[0]);
        rgb1[2] = get_b(y[0]);

        let rgb2 = &mut rgb[BPP..];
        rgb2[0] = get_r(y[1]);
        rgb2[1] = get_g(y[1]);
        rgb2[2] = get_b(y[1]);
    }

    let remainder = rgb_chunks.into_remainder();
    if remainder.len() >= 3 {
        if let (Some(&y), Some(&u), Some(&v)) = (
            y_chunks.remainder().iter().next(),
            u_iter.next(),
            v_iter.next(),
        ) {
            let coeffs = [
                mulhi(v, 26149),
                mulhi(u, 6419),
                mulhi(v, 13320),
                mulhi(u, 33050),
            ];

            remainder[0] = clip(mulhi(y, 19077) + coeffs[0] - 14234);
            remainder[1] = clip(mulhi(y, 19077) - coeffs[1] - coeffs[2] + 8708);
            remainder[2] = clip(mulhi(y, 19077) + coeffs[3] - 17685);
        }
    }
}

// constants used for yuv -> rgb conversion, using ones from libwebp
const YUV_FIX: i32 = 16;
const YUV_HALF: i32 = 1 << (YUV_FIX - 1);

/// converts the whole image to yuv data and adds values on the end to make it match the macroblock sizes
/// downscales the u/v data as well so it's half the width and height of the y data
pub(crate) fn convert_image_yuv<const BPP: usize>(
    image_data: &[u8],
    width: u16,
    height: u16,
) -> (Vec<u8>, Vec<u8>, Vec<u8>) {
    let width = usize::from(width);
    let height = usize::from(height);
    let mb_width = width.div_ceil(16);
    let mb_height = height.div_ceil(16);
    let y_size = 16 * mb_width * 16 * mb_height;
    let luma_width = 16 * mb_width;
    let chroma_width = 8 * mb_width;
    let chroma_size = 8 * mb_width * 8 * mb_height;
    let mut y_bytes = vec![0u8; y_size];
    let mut u_bytes = vec![0u8; chroma_size];
    let mut v_bytes = vec![0u8; chroma_size];

    // loop through two rows at a time so that we can calculate the average of the 2x2 pixels
    // for averaging for the chroma pixels when downscaling
    for (((image_rows, y_rows), u_row), v_row) in image_data
        .chunks_exact(BPP * width * 2)
        .zip(y_bytes.chunks_exact_mut(luma_width * 2))
        .zip(u_bytes.chunks_exact_mut(chroma_width))
        .zip(v_bytes.chunks_exact_mut(chroma_width))
    {
        let (image_row_1, image_row_2) = image_rows.split_at(BPP * width);
        let (y_row_1, y_row_2) = y_rows.split_at_mut(luma_width);

        for (((((row_1, row_2), y_pixels_1), y_pixels_2), u_pixel), v_pixel) in image_row_1
            .chunks_exact(BPP * 2)
            .zip(image_row_2.chunks_exact(BPP * 2))
            .zip(y_row_1.chunks_exact_mut(2))
            .zip(y_row_2.chunks_exact_mut(2))
            .zip(u_row.iter_mut())
            .zip(v_row.iter_mut())
        {
            let (rgb1, rgb2) = row_1.split_at(BPP);
            let (rgb3, rgb4) = row_2.split_at(BPP);

            y_pixels_1[0] = rgb_to_y(rgb1);
            y_pixels_1[1] = rgb_to_y(rgb2);
            y_pixels_2[0] = rgb_to_y(rgb3);
            y_pixels_2[1] = rgb_to_y(rgb4);

            *u_pixel = rgb_to_u_avg(rgb1, rgb2, rgb3, rgb4);
            *v_pixel = rgb_to_v_avg(rgb1, rgb2, rgb3, rgb4);
        }
    }

    (y_bytes, u_bytes, v_bytes)
}

pub(crate) fn convert_image_y<const BPP: usize>(
    image_data: &[u8],
    width: u16,
    height: u16,
) -> (Vec<u8>, Vec<u8>, Vec<u8>) {
    let width = usize::from(width);
    let height = usize::from(height);
    let mb_width = width.div_ceil(16);
    let mb_height = height.div_ceil(16);
    let y_size = 16 * mb_width * 16 * mb_height;
    let luma_width = 16 * mb_width;
    let chroma_size = 8 * mb_width * 8 * mb_height;
    let mut y_bytes = vec![0u8; y_size];
    let u_bytes = vec![127u8; chroma_size];
    let v_bytes = vec![127u8; chroma_size];

    for (image_row, y_row) in image_data
        .chunks_exact(BPP * width)
        .zip(y_bytes.chunks_exact_mut(luma_width))
    {
        for (image_value, y_pixel) in image_row.chunks_exact(BPP).zip(y_row.iter_mut()) {
            *y_pixel = image_value[0];
        }
    }

    (y_bytes, u_bytes, v_bytes)
}

// values come from libwebp
// Y = 0.2568 * R + 0.5041 * G + 0.0979 * B + 16
// U = -0.1482 * R - 0.2910 * G + 0.4392 * B + 128
// V = 0.4392 * R - 0.3678 * G - 0.0714 * B + 128

// this is converted to 16 bit fixed point by multiplying by 2^16
// and shifting back

fn rgb_to_y(rgb: &[u8]) -> u8 {
    let luma = 16839 * i32::from(rgb[0]) + 33059 * i32::from(rgb[1]) + 6420 * i32::from(rgb[2]);
    ((luma + YUV_HALF + (16 << YUV_FIX)) >> YUV_FIX) as u8
}

// get the average of the four surrounding pixels
fn rgb_to_u_avg(rgb1: &[u8], rgb2: &[u8], rgb3: &[u8], rgb4: &[u8]) -> u8 {
    let u1 = rgb_to_u_raw(rgb1);
    let u2 = rgb_to_u_raw(rgb2);
    let u3 = rgb_to_u_raw(rgb3);
    let u4 = rgb_to_u_raw(rgb4);

    ((u1 + u2 + u3 + u4) >> (YUV_FIX + 2)) as u8
}

// get the average of the four surrounding pixels
fn rgb_to_v_avg(rgb1: &[u8], rgb2: &[u8], rgb3: &[u8], rgb4: &[u8]) -> u8 {
    let v1 = rgb_to_v_raw(rgb1);
    let v2 = rgb_to_v_raw(rgb2);
    let v3 = rgb_to_v_raw(rgb3);
    let v4 = rgb_to_v_raw(rgb4);

    ((v1 + v2 + v3 + v4) >> (YUV_FIX + 2)) as u8
}

fn rgb_to_u_raw(rgb: &[u8]) -> i32 {
    -9719 * i32::from(rgb[0]) - 19081 * i32::from(rgb[1])
        + 28800 * i32::from(rgb[2])
        + (128 << YUV_FIX)
}

fn rgb_to_v_raw(rgb: &[u8]) -> i32 {
    28800 * i32::from(rgb[0]) - 24116 * i32::from(rgb[1]) - 4684 * i32::from(rgb[2])
        + (128 << YUV_FIX)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_packed_fancy_interpolation_matches_scalar_formula() {
        let mut seed = 0x0bad_f00du32;
        for _ in 0..10_000 {
            let mut next = || {
                seed = seed.wrapping_mul(1664525).wrapping_add(1013904223);
                (seed >> 24) as u8
            };
            let (tu0, tv0) = (next(), next());
            let (tu1, tv1) = (next(), next());
            let (bu0, bv0) = (next(), next());
            let (bu1, bv1) = (next(), next());
            let packed = interpolate_uv_square(
                pack_uv(tu0, tv0),
                pack_uv(tu1, tv1),
                pack_uv(bu0, bv0),
                pack_uv(bu1, bv1),
            );
            let expected_u = [
                get_fancy_chroma_value(tu0, tu1, bu0, bu1),
                get_fancy_chroma_value(tu1, tu0, bu1, bu0),
                get_fancy_chroma_value(bu0, bu1, tu0, tu1),
                get_fancy_chroma_value(bu1, bu0, tu1, tu0),
            ];
            let expected_v = [
                get_fancy_chroma_value(tv0, tv1, bv0, bv1),
                get_fancy_chroma_value(tv1, tv0, bv1, bv0),
                get_fancy_chroma_value(bv0, bv1, tv0, tv1),
                get_fancy_chroma_value(bv1, bv0, tv1, tv0),
            ];
            for i in 0..4 {
                assert_eq!((packed[i] & 0xff) as u8, expected_u[i]);
                assert_eq!(((packed[i] >> 16) & 0xff) as u8, expected_v[i]);
            }
        }
    }

    #[test]
    fn test_fancy_grid() {
        #[rustfmt::skip]
        let y_buffer = [
            77, 162, 202, 185,
            28, 13, 199, 182,
            135, 147, 164, 135, 
            66, 27, 171, 130,
        ];

        #[rustfmt::skip]
        let u_buffer = [
            34, 101, 
            123, 163
        ];

        #[rustfmt::skip]
        let v_buffer = [
            97, 167,
            149, 23,
        ];

        let mut rgb_buffer = [0u8; 16 * 3];
        fill_rgb_buffer_fancy::<3>(&mut rgb_buffer, &y_buffer, &u_buffer, &v_buffer, 4, 4, 4);

        #[rustfmt::skip]
        let upsampled_u_buffer = [
            34, 51, 84, 101,
            56, 71, 101, 117,
            101, 112, 136, 148,
            123, 133, 153, 163,
        ];

        #[rustfmt::skip]
        let upsampled_v_buffer = [
            97, 115, 150, 167,
            110, 115, 126, 131,
            136, 117, 78, 59,
            149, 118, 55, 23,
        ];

        let mut upsampled_rgb_buffer = [0u8; 16 * 3];
        for (((rgb_val, y), u), v) in upsampled_rgb_buffer
            .chunks_exact_mut(3)
            .zip(y_buffer)
            .zip(upsampled_u_buffer)
            .zip(upsampled_v_buffer)
        {
            rgb_val[0] = yuv_to_r(y, v);
            rgb_val[1] = yuv_to_g(y, u, v);
            rgb_val[2] = yuv_to_b(y, u);
        }

        assert_eq!(rgb_buffer, upsampled_rgb_buffer);
    }

    #[test]
    fn test_yuv_conversions() {
        let (y, u, v) = (203, 40, 42);

        assert_eq!(yuv_to_r(y, v), 80);
        assert_eq!(yuv_to_g(y, u, v), 255);
        assert_eq!(yuv_to_b(y, u), 40);
    }
}
