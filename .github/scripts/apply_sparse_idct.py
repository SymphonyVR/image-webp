from pathlib import Path

p = Path("src/lossy/transform.rs")
s = p.read_text()
marker = """// 14.3 inverse walsh-hadamard transform, used in decoding
pub(crate) fn iwht4x4(block: &mut [i32]) {
"""
insert = """/// Inverse DCT specialized by the last non-zero coefficient in VP8 scan order.
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

""" + marker
if marker not in s:
    raise SystemExit("transform insertion marker missing")
s = s.replace(marker, insert, 1)

test_marker = """    #[test]
    fn test_dct_inverse() {
"""
test = """    #[test]
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

""" + test_marker
if test_marker not in s:
    raise SystemExit("test marker missing")
p.write_text(s.replace(test_marker, test, 1))

p = Path("src/lossy/mod.rs")
s = p.read_text()
macro_marker = """#[derive(Default, Clone, Copy)]
struct MacroBlock {
"""
info = """#[derive(Clone, Copy)]
struct CoeffInfo {
    coded: bool,
    extent: u8,
}

""" + macro_marker
if macro_marker not in s:
    raise SystemExit("macro marker missing")
s = s.replace(macro_marker, info, 1)

old = """    ) -> Result<bool, DecodingError> {
        assert!(complexity <= 2);
"""
new = """    ) -> Result<CoeffInfo, DecodingError> {
        assert!(complexity <= 2);
"""
if old not in s:
    raise SystemExit("coefficient return marker missing")
s = s.replace(old, new, 1)

old = """        let mut has_coefficients = false;
        let mut skip_eob = false;
"""
new = """        let mut has_coefficients = false;
        let mut extent = 0u8;
        let mut skip_eob = false;
"""
if old not in s:
    raise SystemExit("coefficient state marker missing")
s = s.replace(old, new, 1)

old = """            block[zigzag] = i32::from(value) * i32::from(if zigzag > 0 { acq } else { dcq });
            has_coefficients = true;
"""
new = """            block[zigzag] = i32::from(value) * i32::from(if zigzag > 0 { acq } else { dcq });
            has_coefficients = true;
            extent = (i + 1) as u8;
"""
if old not in s:
    raise SystemExit("extent update marker missing")
s = s.replace(old, new, 1)

old = """        decoder.check(res, has_coefficients)
    }

    fn read_residual_data(
"""
new = """        decoder.check(
            res,
            CoeffInfo {
                coded: has_coefficients,
                extent,
            },
        )
    }

    fn read_residual_data(
"""
if old not in s:
    raise SystemExit("coefficient result marker missing")
s = s.replace(old, new, 1)

# Y2 only needs the coded bit for entropy context; the normal WHT stays unchanged.
old = """            let n = self.read_coefficients(&mut block, p, plane, complexity as usize, dcq, acq)?;

            self.left.complexity[0] = if n { 1 } else { 0 };
            self.top[mbx].complexity[0] = if n { 1 } else { 0 };
"""
new = """            let info = self.read_coefficients(&mut block, p, plane, complexity as usize, dcq, acq)?;

            self.left.complexity[0] = if info.coded { 1 } else { 0 };
            self.top[mbx].complexity[0] = if info.coded { 1 } else { 0 };
"""
if old not in s:
    raise SystemExit("Y2 caller marker missing")
s = s.replace(old, new, 1)

old = """                let n = self.read_coefficients(block, p, plane, complexity as usize, dcq, acq)?;

                if block[0] != 0 || n {
                    mb.non_zero_dct = true;
                    transform::idct4x4(block);
                }

                left = if n { 1 } else { 0 };
                self.top[mbx].complexity[x + 1] = if n { 1 } else { 0 };
"""
new = """                let info = self.read_coefficients(block, p, plane, complexity as usize, dcq, acq)?;

                if block[0] != 0 || info.coded {
                    mb.non_zero_dct = true;
                    let extent = info.extent.max(u8::from(block[0] != 0));
                    transform::idct4x4_sparse(block, extent);
                }

                left = if info.coded { 1 } else { 0 };
                self.top[mbx].complexity[x + 1] = if info.coded { 1 } else { 0 };
"""
if old not in s:
    raise SystemExit("luma caller marker missing")
s = s.replace(old, new, 1)

old = """                    let n =
                        self.read_coefficients(block, p, plane, complexity as usize, dcq, acq)?;
                    if block[0] != 0 || n {
                        mb.non_zero_dct = true;
                        transform::idct4x4(block);
                    }

                    left = if n { 1 } else { 0 };
                    self.top[mbx].complexity[x + j] = if n { 1 } else { 0 };
"""
new = """                    let info =
                        self.read_coefficients(block, p, plane, complexity as usize, dcq, acq)?;
                    if block[0] != 0 || info.coded {
                        mb.non_zero_dct = true;
                        transform::idct4x4_sparse(block, info.extent);
                    }

                    left = if info.coded { 1 } else { 0 };
                    self.top[mbx].complexity[x + j] = if info.coded { 1 } else { 0 };
"""
if old not in s:
    raise SystemExit("chroma caller marker missing")
s = s.replace(old, new, 1)
p.write_text(s)
