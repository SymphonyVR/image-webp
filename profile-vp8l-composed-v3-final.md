# Final VP8L composed-v3 symbolic Callgrind profile

- candidate source: `4cd194935d100a09acf24eb24d8c1343c7844844`
- fixture: `tests/images/gallery2/3_webp_ll.webp` (800x600)
- release + full debuginfo, CPU 0

```text
47,410,659 (100.0%)  PROGRAM TOTALS
15,981,636 (33.71%)  src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream [/home/runner/work/image-webp/image-webp/target/release/examples/profile_vp8l_final]
-- Auto-annotated source: src/lossless/decoder/mod.rs
       32 ( 0.00%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::BitReader<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::read_bits::<u8> (1x)
       32 ( 0.00%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::BitReader<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::read_bits::<u8> (1x)
        7 ( 0.00%)          self.decode_image_stream(
31,986,728 (67.47%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream (1x)
        .                               predictor_data,
        9 ( 0.00%)                  } => apply_predictor_transform(
8,168,767 (17.23%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/reverse_transform.rs:image_webp::lossless::decoder::reverse_transform::apply_predictor_transform (1x)
        .                               predictor_data,
        5 ( 0.00%)                      apply_color_transform(
6,556,274 (13.83%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/reverse_transform.rs:image_webp::lossless::decoder::reverse_transform::apply_color_transform (1x)
       48 ( 0.00%)      fn decode_image_stream(
        .                   let color_cache_bits = self.read_color_cache()?;
        .                   let color_cache = color_cache_bits.map(|bits| ColorCache {
        .                       color_cache_bits: bits,
        3 ( 0.00%)              color_cache: vec![[0; 4]; 1 << bits],
       52 ( 0.00%)          let huffman_info = self.read_huffman_codes(is_argb_img, xsize, ysize, color_cache)?;
2,471,241 ( 5.21%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::read_huffman_codes (3x)
        .                   self.decode_image_data(xsize, ysize, huffman_info, data)
        .                               //predictor
        .                               let mut predictor_data =
        9 ( 0.00%)                      self.decode_image_stream(block_xsize, block_ysize, false, &mut predictor_data)?;
  112,705 ( 0.24%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream (1x)
        .                                   predictor_data,
       10 ( 0.00%)                      self.decode_image_stream(block_xsize, block_ysize, false, &mut transform_data)?;
  190,199 ( 0.40%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream (1x)
        .                   color_cache: Option<ColorCache>,
        8 ( 0.00%)              self.decode_image_stream(huffman_xsize, huffman_ysize, false, &mut data)?;
  115,324 ( 0.24%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream'2 (1x)
        .                               if let Some(color_cache) = color_cache.as_ref() {
        .                                   alphabet_size += 1 << color_cache.color_cache_bits;
        .                       color_cache,
   12,400 ( 0.03%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/huffman.rs:<image_webp::lossless::decoder::huffman::HuffmanTree>::build_two_node (35x)
1,437,156 ( 3.03%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/huffman.rs:<image_webp::lossless::decoder::huffman::HuffmanTree>::build_implicit (123x)
  257,323 ( 0.54%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/huffman.rs:<image_webp::lossless::decoder::huffman::HuffmanTree>::build_implicit (123x)
        .                       self.bit_reader.fill()?;
        .                       let code_len = table.read_symbol(&mut self.bit_reader)?;
        .                       self.bit_reader.fill()?;
        .                           // and we can just fill the output buffer with the symbol
        .                       let code = tree[GREEN].read_symbol(&mut self.bit_reader)?;
        .                           let red = tree[RED].read_symbol(&mut self.bit_reader)? as u8;
        .                           let blue = tree[BLUE].read_symbol(&mut self.bit_reader)? as u8;
        .                               self.bit_reader.fill()?;
        .                           let alpha = tree[ALPHA].read_symbol(&mut self.bit_reader)? as u8;
        .                           if let Some(color_cache) = huffman_info.color_cache.as_mut() {
1,067,890 ( 2.25%)                      color_cache.insert([red, green, blue, alpha]);
        .                           let dist_symbol = tree[DIST].read_symbol(&mut self.bit_reader)?;
    3,934 ( 0.01%)                          data.copy_within(start..start + 16, index * 4);
   52,187 ( 0.11%)                                  data.copy_within(start + i..start + i + 16, index * 4 + i);
        .                               if let Some(color_cache) = huffman_info.color_cache.as_mut() {
        .                                       color_cache.insert(pixel.try_into().unwrap());
        .                           let color_cache = huffman_info
        .                               .color_cache
   14,475 ( 0.03%)                  let color = color_cache.lookup((code - 280).into());
        .                                       self.bit_reader.consume(bits)?;
    4,570 ( 0.01%)                                  .copy_from_slice(&color_cache.lookup((code - 280).into()));
   52,837 ( 0.11%)  => /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/ptr/mod.rs:core::ptr::drop_glue::<image_webp::lossless::decoder::HuffmanInfo> (3x)
        .               fn read_color_cache(&mut self) -> Result<Option<u8>, DecodingError> {
        .                   bit_reader.consume(extra_bits)?;
        .               color_cache: Option<ColorCache>,
        .               color_cache_bits: u8,
        .               color_cache: Vec<[u8; 4]>,
        .               fn insert(&mut self, color: [u8; 4]) {
  497,616 ( 1.05%)          let index = (0x1e35a7bdu32.wrapping_mul(color_u32)) >> (32 - self.color_cache_bits);
  604,405 ( 1.27%)          self.color_cache[index as usize] = color;
    4,570 ( 0.01%)          self.color_cache[index]
        .               pub(crate) fn fill(&mut self) -> Result<(), DecodingError> {
        .                   let mut buf = self.reader.fill_buf()?;
  394,359 ( 0.83%)              self.reader.consume(usize::from((63 - self.nbits) / 8));
        .                           self.reader.consume(1);
        .                           buf = self.reader.fill_buf()?;
        .               pub(crate) fn consume(&mut self, num: u8) -> Result<(), DecodingError> {
        .                       self.fill()?;
        .                   self.consume(num)?;
4,053,100 ( 8.55%)  <counts for unidentified lines in src/lossless/decoder/mod.rs>
```

## Stop-rule assessment

The exhaustive sweep has already tested entropy decode, Huffman construction/layout, color cache, LZ copy mechanics, inverse-color kernels, predictor kernels, palette/subtract-green, input staging, output stores, distance decoding, and transform batching. No new optimization is opened unless this final profile exposes a distinct >=2% mechanism outside those closed families.