/// 16 bit fixed point version of cos(PI/8) * sqrt(2) - 1
const CONST1: i64 = 20091;
/// 16 bit fixed point version of sin(PI/8) * sqrt(2)
const CONST2: i64 = 35468;

// inverse discrete cosine transform, used in decoding
pub(crate) fn idct4x4(block: &mut [i32]) {
    // The intermediate results may overflow the types, so we stretch the type.
    fn fetch(block: &[i32], idx: usize) -> i64 {
        i64::from(block[idx])
    }

    // Perform one length check up front to avoid subsequent bounds checks in this function
    assert!(block.len() >= 16);

    for i in 0usize..4 {
        let a1 = fetch(block, i) + fetch(block, 8 + i);
        let b1 = fetch(block, i) - fetch(block, 8 + i);

        let t1 = (fetch(block, 4 + i) * CONST2) >> 16;
        let t2 = fetch(block, 12 + i) + ((fetch(block, 12 + i) * CONST1) >> 16);
        let c1 = t1 - t2;

        let t1 = fetch(block, 4 + i) + ((fetch(block, 4 + i) * CONST1) >> 16);
        let t2 = (fetch(block, 12 + i) * CONST2) >> 16;
        let d1 = t1 + t2;

        block[i] = (a1 + d1) as i32;
        block[4 + i] = (b1 + c1) as i32;
        block[4 * 3 + i] = (a1 - d1) as i32;
        block[4 * 2 + i] = (b1 - c1) as i32;
    }

    for i in 0usize..4 {
        let a1 = fetch(block, 4 * i) + fetch(block, 4 * i + 2);
        let b1 = fetch(block, 4 * i) - fetch(block, 4 * i + 2);

        let t1 = (fetch(block, 4 * i + 1) * CONST2) >> 16;
        let t2 = fetch(block, 4 * i + 3) + ((fetch(block, 4 * i + 3) * CONST1) >> 16);
        let c1 = t1 - t2;

        let t1 = fetch(block, 4 * i + 1) + ((fetch(block, 4 * i + 1) * CONST1) >> 16);
        let t2 = (fetch(block, 4 * i + 3) * CONST2) >> 16;
        let d1 = t1 + t2;

        block[4 * i] = ((a1 + d1 + 4) >> 3) as i32;
        block[4 * i + 3] = ((a1 - d1 + 4) >> 3) as i32;
        block[4 * i + 1] = ((b1 + c1 + 4) >> 3) as i32;
        block[4 * i + 2] = ((b1 - c1 + 4) >> 3) as i32;
    }
}

/// Inverse DCT and add the resulting residuals directly to a predicted 4x4 block.
///
/// This is the same transform as [`idct4x4`], but avoids materializing the final
/// 16 transformed residuals when decoding. The first pass stays local and the
/// second pass writes/clamps directly into the prediction buffer.
pub(crate) fn idct4x4_add(block: &[i32; 16], dst: &mut [u8], y0: usize, x0: usize, stride: usize) {
    #[inline(always)]
    fn fetch(block: &[i32; 16], idx: usize) -> i64 {
        i64::from(block[idx])
    }

    #[allow(clippy::manual_clamp)]
    #[inline(always)]
    fn add_clamped(pixel: &mut u8, residual: i32) {
        let value = i32::from(*pixel) + residual;
        *pixel = value.max(0).min(255) as u8;
    }

    let mut tmp = [0i32; 16];

    for i in 0usize..4 {
        let a1 = fetch(block, i) + fetch(block, 8 + i);
        let b1 = fetch(block, i) - fetch(block, 8 + i);

        let t1 = (fetch(block, 4 + i) * CONST2) >> 16;
        let t2 = fetch(block, 12 + i) + ((fetch(block, 12 + i) * CONST1) >> 16);
        let c1 = t1 - t2;

        let t1 = fetch(block, 4 + i) + ((fetch(block, 4 + i) * CONST1) >> 16);
        let t2 = (fetch(block, 12 + i) * CONST2) >> 16;
        let d1 = t1 + t2;

        tmp[i] = (a1 + d1) as i32;
        tmp[4 + i] = (b1 + c1) as i32;
        tmp[12 + i] = (a1 - d1) as i32;
        tmp[8 + i] = (b1 - c1) as i32;
    }

    for row in 0usize..4 {
        let base = 4 * row;
        let a1 = fetch(&tmp, base) + fetch(&tmp, base + 2);
        let b1 = fetch(&tmp, base) - fetch(&tmp, base + 2);

        let t1 = (fetch(&tmp, base + 1) * CONST2) >> 16;
        let t2 = fetch(&tmp, base + 3) + ((fetch(&tmp, base + 3) * CONST1) >> 16);
        let c1 = t1 - t2;

        let t1 = fetch(&tmp, base + 1) + ((fetch(&tmp, base + 1) * CONST1) >> 16);
        let t2 = (fetch(&tmp, base + 3) * CONST2) >> 16;
        let d1 = t1 + t2;

        let residuals = [
            ((a1 + d1 + 4) >> 3) as i32,
            ((b1 + c1 + 4) >> 3) as i32,
            ((b1 - c1 + 4) >> 3) as i32,
            ((a1 - d1 + 4) >> 3) as i32,
        ];
        let pos = (y0 + row) * stride + x0;
        for (pixel, residual) in dst[pos..pos + 4].iter_mut().zip(residuals) {
            add_clamped(pixel, residual);
        }
    }
}

// 14.3 inverse walsh-hadamard transform, used in decoding
pub(crate) fn iwht4x4(block: &mut [i32]) {
    // Perform one length check up front to avoid subsequent bounds checks in this function
    assert!(block.len() >= 16);

    for i in 0usize..4 {
        let a1 = block[i] + block[12 + i];
        let b1 = block[4 + i] + block[8 + i];
        let c1 = block[4 + i] - block[8 + i];
        let d1 = block[i] - block[12 + i];

        block[i] = a1 + b1;
        block[4 + i] = c1 + d1;
        block[8 + i] = a1 - b1;
        block[12 + i] = d1 - c1;
    }

    for block in block.chunks_exact_mut(4) {
        let a1 = block[0] + block[3];
        let b1 = block[1] + block[2];
        let c1 = block[1] - block[2];
        let d1 = block[0] - block[3];

        let a2 = a1 + b1;
        let b2 = c1 + d1;
        let c2 = a1 - b1;
        let d2 = d1 - c1;

        block[0] = (a2 + 3) >> 3;
        block[1] = (b2 + 3) >> 3;
        block[2] = (c2 + 3) >> 3;
        block[3] = (d2 + 3) >> 3;
    }
}

pub(crate) fn wht4x4(block: &mut [i32; 16]) {
    // The intermediate results may overflow the types, so we stretch the type.
    fn fetch(block: &[i32], idx: usize) -> i64 {
        i64::from(block[idx])
    }

    // vertical
    for i in 0..4 {
        let a = fetch(block, i * 4) + fetch(block, i * 4 + 3);
        let b = fetch(block, i * 4 + 1) + fetch(block, i * 4 + 2);
        let c = fetch(block, i * 4 + 1) - fetch(block, i * 4 + 2);
        let d = fetch(block, i * 4) - fetch(block, i * 4 + 3);

        block[i * 4] = (a + b) as i32;
        block[i * 4 + 1] = (c + d) as i32;
        block[i * 4 + 2] = (a - b) as i32;
        block[i * 4 + 3] = (d - c) as i32;
    }

    // horizontal
    for i in 0..4 {
        let a1 = fetch(block, i) + fetch(block, i + 12);
        let b1 = fetch(block, i + 4) + fetch(block, i + 8);
        let c1 = fetch(block, i + 4) - fetch(block, i + 8);
        let d1 = fetch(block, i) - fetch(block, i + 12);

        let a2 = a1 + b1;
        let b2 = c1 + d1;
        let c2 = a1 - b1;
        let d2 = d1 - c1;

        let a3 = (a2 + if a2 > 0 { 1 } else { 0 }) / 2;
        let b3 = (b2 + if b2 > 0 { 1 } else { 0 }) / 2;
        let c3 = (c2 + if c2 > 0 { 1 } else { 0 }) / 2;
        let d3 = (d2 + if d2 > 0 { 1 } else { 0 }) / 2;

        block[i] = a3 as i32;
        block[i + 4] = b3 as i32;
        block[i + 8] = c3 as i32;
        block[i + 12] = d3 as i32;
    }
}

pub(crate) fn dct4x4(block: &mut [i32; 16]) {
    // The intermediate results may overflow the types, so we stretch the type.
    fn fetch(block: &[i32], idx: usize) -> i64 {
        i64::from(block[idx])
    }

    // vertical
    for i in 0..4 {
        let a = (fetch(block, i * 4) + fetch(block, i * 4 + 3)) * 8;
        let b = (fetch(block, i * 4 + 1) + fetch(block, i * 4 + 2)) * 8;
        let c = (fetch(block, i * 4 + 1) - fetch(block, i * 4 + 2)) * 8;
        let d = (fetch(block, i * 4) - fetch(block, i * 4 + 3)) * 8;

        block[i * 4] = (a + b) as i32;
        block[i * 4 + 2] = (a - b) as i32;
        block[i * 4 + 1] = ((c * 2217 + d * 5352 + 14500) >> 12) as i32;
        block[i * 4 + 3] = ((d * 2217 - c * 5352 + 7500) >> 12) as i32;
    }

    // horizontal
    for i in 0..4 {
        let a = fetch(block, i) + fetch(block, i + 12);
        let b = fetch(block, i + 4) + fetch(block, i + 8);
        let c = fetch(block, i + 4) - fetch(block, i + 8);
        let d = fetch(block, i) - fetch(block, i + 12);

        block[i] = ((a + b + 7) >> 4) as i32;
        block[i + 8] = ((a - b + 7) >> 4) as i32;
        block[i + 4] = (((c * 2217 + d * 5352 + 12000) >> 16) + if d != 0 { 1 } else { 0 }) as i32;
        block[i + 12] = ((d * 2217 - c * 5352 + 51000) >> 16) as i32;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_idct4x4_add_matches_staged_transform() {
        let mut seed = 0x1234_5678u32;
        for _ in 0..1000 {
            let mut block = [0i32; 16];
            for coeff in &mut block {
                seed = seed.wrapping_mul(1664525).wrapping_add(1013904223);
                *coeff = ((seed >> 16) as i16 as i32) / 8;
            }

            let mut expected = [127u8; 8 * 8];
            let mut transformed = block;
            idct4x4(&mut transformed);
            for row in 0..4 {
                for col in 0..4 {
                    let pos = (2 + row) * 8 + 2 + col;
                    expected[pos] = (i32::from(expected[pos]) + transformed[row * 4 + col])
                        .max(0)
                        .min(255) as u8;
                }
            }

            let mut actual = [127u8; 8 * 8];
            idct4x4_add(&block, &mut actual, 2, 2, 8);
            assert_eq!(expected, actual);
        }
    }

    #[test]
    fn test_dct_inverse() {
        const BLOCK: [i32; 16] = [
            38, 6, 210, 107, 42, 125, 185, 151, 241, 224, 125, 233, 227, 8, 57, 96,
        ];

        let mut dct_block = BLOCK.clone();

        dct4x4(&mut dct_block);

        let mut inverse_dct_block = dct_block.clone();

        idct4x4(&mut inverse_dct_block);

        assert_eq!(BLOCK, inverse_dct_block);
    }
}
