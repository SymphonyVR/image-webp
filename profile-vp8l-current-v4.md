# Current VP8L symbolic Callgrind profile v4

- baseline: `84d8d20753fce0a9972e8a244fdf929b5a55671c`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- fixture: `tests/images/gallery2/3_webp_ll.webp` (800x600)
- release + full debuginfo, CPU 0

```text
42,022,099 (100.0%)  PROGRAM TOTALS
10,200,808 (24.27%)  src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream [/home/runner/work/image-webp/image-webp/target/release/examples/profile_vp8l_v4]
-- Auto-annotated source: src/lossless/decoder/mod.rs
   14,004 ( 0.03%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/huffman.rs:<image_webp::lossless::decoder::huffman::HuffmanTree<9>>::build_two_node (35x)
    1,389 ( 0.00%)              Self::Implicit(code_lengths) => HuffmanTree::build_implicit(code_lengths),
1,349,809 ( 3.21%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/huffman.rs:<image_webp::lossless::decoder::huffman::HuffmanTree<9>>::build_implicit::<alloc::vec::Vec<u16>> (123x)
       32 ( 0.00%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::BitReader<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::read_bits::<u8> (1x)
       32 ( 0.00%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::BitReader<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::read_bits::<u8> (1x)
        7 ( 0.00%)          self.decode_image_stream(
26,639,398 (63.39%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream (1x)
        .                               predictor_data,
        9 ( 0.00%)                  } => apply_predictor_transform(
8,168,767 (19.44%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/reverse_transform.rs:image_webp::lossless::decoder::reverse_transform::apply_predictor_transform (1x)
        .                               predictor_data,
        5 ( 0.00%)                      apply_color_transform(
6,556,274 (15.60%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/reverse_transform.rs:image_webp::lossless::decoder::reverse_transform::apply_color_transform (1x)
        .                               apply_subtract_green_transform(&mut buf[..image_size]);
       52 ( 0.00%)      fn decode_image_stream(
        .                   let color_cache_bits = self.read_color_cache()?;
        .                   let color_cache = color_cache_bits.map(|bits| ColorCache {
        .                       color_cache_bits: bits,
        3 ( 0.00%)              color_cache: vec![[0; 4]; 1 << bits],
       48 ( 0.00%)          let huffman_info = self.read_huffman_codes(is_argb_img, xsize, ysize, color_cache)?;
2,512,621 ( 5.98%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::read_huffman_codes (3x)
        .                   self.decode_image_data(xsize, ysize, huffman_info, data)
        .                               //predictor
        .                               let mut predictor_data =
        9 ( 0.00%)                      self.decode_image_stream(block_xsize, block_ysize, false, &mut predictor_data)?;
   92,389 ( 0.22%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream (1x)
        .                                   predictor_data,
       10 ( 0.00%)                      self.decode_image_stream(block_xsize, block_ysize, false, &mut transform_data)?;
  169,386 ( 0.40%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream (1x)
       40 ( 0.00%)      fn read_huffman_codes(
        .                   color_cache: Option<ColorCache>,
        8 ( 0.00%)              self.decode_image_stream(huffman_xsize, huffman_ysize, false, &mut data)?;
   95,074 ( 0.23%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream'2 (1x)
        .                               if let Some(color_cache) = color_cache.as_ref() {
        .                                   alphabet_size += 1 << color_cache.color_cache_bits;
    2,340 ( 0.01%)                  specs[j] = Some(self.read_huffman_code_spec(alphabet_size)?);
    1,330 ( 0.00%)  => /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/ptr/mod.rs:core::ptr::drop_glue::<[core::option::Option<image_webp::lossless::decoder::HuffmanCodeSpec>; 5]> (38x)
        .                       color_cache,
        .               fn read_huffman_code_spec(
    1,240 ( 0.00%)                  self.read_huffman_code_lengths(&code_length_code_lengths, alphabet_size)?;
        .               fn read_huffman_code_lengths(
    2,108 ( 0.01%)          let table = HuffmanTree9::build_implicit(code_length_code_lengths)?;
  224,542 ( 0.53%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/huffman.rs:<image_webp::lossless::decoder::huffman::HuffmanTree<9>>::build_implicit::<&[u16]> (123x)
        .                       self.bit_reader.fill()?;
        .                       let code_len = table.read_symbol(&mut self.bit_reader)?;
        .               fn decode_image_data(
        .                       let color_cache = &mut huffman_info.color_cache;
        .                           HuffmanCodeGroup::Normal(tree) => self.decode_image_data_block::<9>(
        .                               color_cache,
        .                               color_cache,
   51,977 ( 0.12%)  => /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/ptr/mod.rs:core::ptr::drop_glue::<image_webp::lossless::decoder::HuffmanInfo> (3x)
        .               fn decode_image_data_block<const TABLE_BITS: u8>(
        .                   color_cache: &mut Option<ColorCache>,
        .                           if let Some(color_cache) = color_cache.as_mut() {
        .                               color_cache.insert(value);
        .                       self.bit_reader.fill()?;
        .                       let code = tree[GREEN].read_symbol(&mut self.bit_reader)?;
        .                           let red = tree[RED].read_symbol(&mut self.bit_reader)? as u8;
        .                           let blue = tree[BLUE].read_symbol(&mut self.bit_reader)? as u8;
        .                               self.bit_reader.fill()?;
        .                           let alpha = tree[ALPHA].read_symbol(&mut self.bit_reader)? as u8;
        .                           if let Some(color_cache) = color_cache.as_mut() {
        .                               color_cache.insert([red, green, blue, alpha]);
        .                           let dist_symbol = tree[DIST].read_symbol(&mut self.bit_reader)?;
    3,934 ( 0.01%)                          data.copy_within(start..start + 16, *index * 4);
  133,968 ( 0.32%)                                  data.copy_within(start + i..start + i + 16, *index * 4 + i);
        .                               if let Some(color_cache) = color_cache.as_mut() {
        .                                       color_cache.insert(pixel.try_into().unwrap());
        .                           let color_cache = color_cache.as_mut().ok_or(DecodingError::BitStreamError)?;
   14,475 ( 0.03%)                  let color = color_cache.lookup((code - 280).into());
        .                                       self.bit_reader.consume(bits)?;
    4,570 ( 0.01%)                                  .copy_from_slice(&color_cache.lookup((code - 280).into()));
        .               fn read_color_cache(&mut self) -> Result<Option<u8>, DecodingError> {
        .                           return Err(DecodingError::InvalidColorCacheBits(code_bits));
        .                   bit_reader.consume(extra_bits)?;
        .               color_cache: Vec<[u8; 4]>,
        .           impl ColorCache {
        .               fn insert(&mut self, color: [u8; 4]) {
  284,038 ( 0.68%)          let index = (0x1e35a7bdu32.wrapping_mul(color_u32)) >> (32 - self.color_cache_bits);
  604,405 ( 1.44%)          self.color_cache[index as usize] = color;
    4,570 ( 0.01%)          self.color_cache[index]
        .               pub(crate) fn fill(&mut self) -> Result<(), DecodingError> {
        .                   let mut buf = self.reader.fill_buf()?;
  394,359 ( 0.94%)              self.reader.consume(usize::from((63 - self.nbits) / 8));
        .                           self.reader.consume(1);
        .                           buf = self.reader.fill_buf()?;
        .               pub(crate) fn consume(&mut self, num: u8) -> Result<(), DecodingError> {
        .                       self.fill()?;
        .                   self.consume(num)?;
1,232,078 ( 2.93%)  <counts for unidentified lines in src/lossless/decoder/mod.rs>
```
