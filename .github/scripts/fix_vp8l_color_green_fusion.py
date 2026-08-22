from pathlib import Path

p = Path("src/lossless/decoder/reverse_transform.rs")
s = p.read_text()
old = '''pub(crate) fn apply_color_transform_and_subtract_green<const SUBTRACT_BEFORE_COLOR: bool>(
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
'''
new = '''pub(crate) fn apply_color_transform_and_subtract_green<const SUBTRACT_BEFORE_COLOR: bool>(
    image_data: &mut [u8],
    width: u16,
    size_bits: u8,
    transform_data: &[u8],
) {
    if SUBTRACT_BEFORE_COLOR {
        apply_color_transform_impl::<true, false>(image_data, width, size_bits, transform_data);
    } else {
        apply_color_transform_impl::<false, true>(image_data, width, size_bits, transform_data);
    }
}
'''
if old not in s:
    raise SystemExit("generic const-expression wrapper marker missing")
p.write_text(s.replace(old, new, 1))

p = Path("src/lossless/decoder/mod.rs")
s = p.read_text().replace("usize::from(*next_index)", "usize::from(next_index)")
p.write_text(s)
