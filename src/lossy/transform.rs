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

/// Inverse DCT specialized by the last non-zero coefficient in VP8 scan order.
///
/// `extent` is zero when the block is empty and otherwise one plus the scan
/// position of the last non-zero coefficient. Extents 1 and 2/3 have much
/// cheaper exact transforms than the general 4x4 inverse DCT.
pub(crate) fn idct4x4_sparse(block: &mut [i32; 16], extent: u8) {
    match extent {
        0 => {}
        1 => {
            let dc = (block[0] + 4) >> 3;
            block.fill(dc);
        }
        2 | 3 => {
            let a = i64::from(block[0]) + 4;
            let b1 = i64::from(block[1]);
            let b4 = i64::from(block[4]);
            let c4 = (b4 * CONST2) >> 16;
            let d4 = b4 + ((b4 * CONST1) >> 16);
            let c1 = (b1 * CONST2) >> 16;
            let d1 = b1 + ((b1 * CONST1) >> 16);

            let rows = [a + d4, a + c4, a - c4, a - d4];
            for (row, dc) in rows.into_iter().enumerate() {
                let base = row * 4;
                block[base] = ((dc + d1) >> 3) as i32;
                block[base + 1] = ((dc + c1) >> 3) as i32;
                block[base + 2] = ((dc - c1) >> 3) as i32;
                block[base + 3] = ((dc - d1) >> 3) as i32;
            }
        }
        _ => idct4x4(block),
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
    fn test_sparse_idct_matches_full_idct() {
        let mut seed = 0x51a7_9e31u32;
        for extent in [0u8, 1, 2, 3] {
            for _ in 0..2000 {
                let mut block = [0i32; 16];
                let mut next = || {
                    seed = seed.wrapping_mul(1664525).wrapping_add(1013904223);
                    ((seed >> 16) as i16 as i32) / 8
                };
                match extent {
                    0 => {}
                    1 => block[0] = next(),
                    2 => {
                        block[0] = next();
                        block[1] = next();
                    }
                    3 => {
                        block[0] = next();
                        block[1] = next();
                        block[4] = next();
                    }
                    _ => unreachable!(),
                }
                let mut expected = block;
                idct4x4(&mut expected);
                idct4x4_sparse(&mut block, extent);
                assert_eq!(expected, block);
            }
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
