# VP8L entropy explicit source profile

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 7763 64-Core Processor`
- fixture: gallery2/3 lossless, 800x600

## huffman.rs
```text
41,901,862 (100.0%)  PROGRAM TOTALS
   18,396 ( 0.04%)          if codeword == table_size - 1 {
   17,900 ( 0.04%)          let adv = (u16::BITS - 1) - (codeword ^ (table_size - 1)).leading_zeros();
   17,900 ( 0.04%)          let bit = 1 << adv;
   17,900 ( 0.04%)          codeword &= bit - 1;
    8,950 ( 0.02%)          codeword |= bit;
    2,356 ( 0.01%)      pub(crate) fn build_implicit(code_lengths: impl AsRef<[u16]>) -> Result<Self, DecodingError> {
      248 ( 0.00%)          let code_lengths = code_lengths.as_ref();
    2,232 ( 0.01%)          let mut histogram = [0; MAX_ALLOWED_CODE_LENGTH + 1];
   70,360 ( 0.17%)          for &length in code_lengths.iter() {
   70,360 ( 0.17%)              histogram[usize::from(length)] += 1;
   70,360 ( 0.17%)              if length != 0 {
      992 ( 0.00%)          if num_symbols == 0 {
    6,287 ( 0.02%)          while max_length > 1 && histogram[max_length] == 0 {
    2,232 ( 0.01%)          let mut offsets = [0; 16];
      496 ( 0.00%)          offsets[1] = histogram[0];
    5,121 ( 0.01%)              offsets[i + 1] = offsets[i] + histogram[i];
    1,459 ( 0.00%)              codespace_used = (codespace_used << 1) + histogram[i];
      496 ( 0.00%)          codespace_used = (codespace_used << 1) + histogram[max_length];
      868 ( 0.00%)          if codespace_used != (1 << max_length) {
      496 ( 0.00%)          let table_size = (1 << table_bits) as usize;
        .                   let mut primary_table = vec![0; table_size];
        .                   let mut sorted_symbols = vec![0u16; code_lengths.len()];
   70,360 ( 0.17%)              let length = code_lengths[symbol];
  105,540 ( 0.25%)              sorted_symbols[next_index[length as usize]] = symbol as u16;
   70,360 ( 0.17%)              next_index[length as usize] += 1;
        .                   let primary_table_bits = primary_table.len().ilog2() as usize;
      744 ( 0.00%)          let primary_table_mask = (1 << primary_table_bits) - 1;
        .                   for length in 1..=primary_table_bits {
    8,555 ( 0.02%)              let current_table_end = 1 << length;
    5,133 ( 0.01%)              for _ in 0..histogram[length] {
        .                           let symbol = sorted_symbols[i];
    5,582 ( 0.01%)                  i += 1;
   11,164 ( 0.03%)                  let entry = ((length as u16) << 12) | symbol;
   11,164 ( 0.03%)                  primary_table[codeword as usize] = entry;
    3,422 ( 0.01%)              if length < primary_table_bits {
        .                           primary_table.copy_within(0..current_table_end, current_table_end);
      496 ( 0.00%)          let mut secondary_table = if max_length > primary_table_bits {
        .                   if max_length > primary_table_bits {
       99 ( 0.00%)              for length in (primary_table_bits + 1)..=max_length {
    1,464 ( 0.00%)                  let subtable_size = 1 << (length - primary_table_bits);
      244 ( 0.00%)                  for _ in 0..histogram[length] {
   14,464 ( 0.03%)                      if codeword & primary_table_mask != subtable_prefix {
        .                                   subtable_prefix = codeword & primary_table_mask;
        .                                   subtable_start = secondary_table.len();
    3,832 ( 0.01%)                          primary_table[subtable_prefix as usize] =
        .                                   secondary_table.resize(subtable_start + subtable_size, 0);
    3,616 ( 0.01%)                      let symbol = sorted_symbols[i];
    3,616 ( 0.01%)                      i += 1;
   21,696 ( 0.05%)                      secondary_table[subtable_start + (codeword >> primary_table_bits) as usize] =
    3,616 ( 0.01%)                          (symbol << 4) | (length as u16);
    1,018 ( 0.00%)                  if length < max_length && codeword & primary_table_mask == subtable_prefix {
        .                               secondary_table.extend_from_within(subtable_start..);
      950 ( 0.00%)                      primary_table[subtable_prefix as usize] =
      285 ( 0.00%)                          (((length + 1) as u16) << 12) | subtable_start as u16;
      198 ( 0.00%)          assert!(secondary_table.len() <= 4096);
    1,488 ( 0.00%)          Ok(Self(HuffmanTreeInner::Tree {
        .                       primary_table,
    1,984 ( 0.00%)              secondary_table,
    2,356 ( 0.01%)      }
      324 ( 0.00%)      pub(crate) fn build_two_node(zero: u16, one: u16) -> Self {
      252 ( 0.00%)          Self(HuffmanTreeInner::Tree {
      144 ( 0.00%)              primary_table: vec![(1 << 12) | zero, (1 << 12) | one],
        .                       secondary_table: Vec::new(),
      252 ( 0.00%)      }
   21,474 ( 0.05%)          matches!(self.0, HuffmanTreeInner::Single(_))
   11,002 ( 0.03%)      fn read_symbol_slowpath<R: BufRead>(
        .                   secondary_table: &[u16],
        .                   primary_table_entry: u16,
    5,501 ( 0.01%)          let length = primary_table_entry >> 12;
   27,505 ( 0.07%)          let mask = (1 << (length - TABLE_BITS as u16)) - 1;
   22,004 ( 0.05%)              ((primary_table_entry & 0xfff) as usize) + ((v >> TABLE_BITS) as usize & mask as usize);
   16,503 ( 0.04%)          let secondary_entry = secondary_table[secondary_index];
   11,002 ( 0.03%)          bit_reader.consume((secondary_entry & 0xf) as u8)?;
   22,004 ( 0.05%)          Ok(secondary_entry >> 4)
    5,501 ( 0.01%)      }
        .               pub(crate) fn read_symbol<R: BufRead>(
  922,393 ( 2.20%)          match &self.0 {
        .                           primary_table,
        .                           secondary_table,
  770,698 ( 1.84%)                  let entry = primary_table[(v & table_mask) as usize];
1,145,045 ( 2.73%)                  if (entry >> 12) <= TABLE_BITS as u16 {
  556,560 ( 1.33%)                      return Ok(entry & 0xfff);
   26,866 ( 0.06%)                  Self::read_symbol_slowpath(secondary_table, v, entry, bit_reader)
  159,529 ( 0.38%)  => src/lossless/decoder/huffman.rs:<image_webp::lossless::decoder::huffman::HuffmanTree<9>>::read_symbol_slowpath::<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>> (5,501x)
   90,693 ( 0.22%)              HuffmanTreeInner::Single(symbol) => Ok(*symbol),
   13,736 ( 0.03%)          match &self.0 {
        .                           primary_table,
   13,736 ( 0.03%)                  let entry = primary_table[(v & table_mask) as usize];
   54,630 ( 0.13%)                  if (entry >> 12) <= TABLE_BITS as u16 {
   13,579 ( 0.03%)                      return Some(((entry >> 12) as u8, entry & 0xfff));
  116,047 ( 0.28%)  <counts for unidentified lines in src/lossless/decoder/huffman.rs>
4,420,259 (10.55%)  events annotated
```

## decoder/mod.rs
```text
41,901,862 (100.0%)  PROGRAM TOTALS
      390 ( 0.00%)          let Self::Implicit(code_lengths) = self else {
   16,660 ( 0.04%)          for &length in code_lengths {
  172,326 ( 0.41%)              if length != 0 {
      124 ( 0.00%)          symbols >= 256 && long_symbols * 8 >= symbols
    1,880 ( 0.00%)          match self {
      122 ( 0.00%)              Self::Single(symbol) => Ok(HuffmanTree::build_single_node(symbol)),
       72 ( 0.00%)              Self::Two(zero, one) => Ok(HuffmanTree::build_two_node(zero, one)),
    8,563 ( 0.02%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/huffman.rs:<image_webp::lossless::decoder::huffman::HuffmanTree<9>>::build_two_node (35x)
    1,389 ( 0.00%)              Self::Implicit(code_lengths) => HuffmanTree::build_implicit(code_lengths),
1,233,307 ( 2.94%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/huffman.rs:<image_webp::lossless::decoder::huffman::HuffmanTree<9>>::build_implicit::<alloc::vec::Vec<u16>> (123x)
       30 ( 0.00%)      ((u32::from(size) + (1u32 << bits) - 1) >> bits)
       13 ( 0.00%)          Self {
        9 ( 0.00%)      pub(crate) fn decode_frame(
        3 ( 0.00%)          if implicit_dimensions {
        1 ( 0.00%)              let signature = self.bit_reader.read_bits::<u8>(8)?;
        2 ( 0.00%)              if signature != 0x2f {
        2 ( 0.00%)              self.width = self.bit_reader.read_bits::<u16>(14)? + 1;
        2 ( 0.00%)              self.height = self.bit_reader.read_bits::<u16>(14)? + 1;
        4 ( 0.00%)              if u32::from(self.width) != width || u32::from(self.height) != height {
        3 ( 0.00%)              let _alpha_used = self.bit_reader.read_bits::<u8>(1)?;
       32 ( 0.00%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::BitReader<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::read_bits::<u8> (1x)
        3 ( 0.00%)              let version_num = self.bit_reader.read_bits::<u8>(3)?;
       32 ( 0.00%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::BitReader<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::read_bits::<u8> (1x)
        4 ( 0.00%)              if version_num != 0 {
        3 ( 0.00%)          let transformed_size = usize::from(transformed_width) * usize::from(self.height) * 4;
        7 ( 0.00%)          self.decode_image_stream(
26,521,447 (63.29%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream (1x)
        4 ( 0.00%)          for &trans_index in self.transform_order.iter().rev() {
        6 ( 0.00%)              let transform = self.transforms[usize::from(trans_index)].as_ref().unwrap();
        9 ( 0.00%)                  } => apply_predictor_transform(
8,168,767 (19.49%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/reverse_transform.rs:image_webp::lossless::decoder::reverse_transform::apply_predictor_transform (1x)
        5 ( 0.00%)                      apply_color_transform(
6,556,274 (15.65%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/reverse_transform.rs:image_webp::lossless::decoder::reverse_transform::apply_color_transform (1x)
        1 ( 0.00%)                  }
        1 ( 0.00%)          Ok(())
       10 ( 0.00%)      }
       52 ( 0.00%)      fn decode_image_stream(
        .                   let color_cache = color_cache_bits.map(|bits| ColorCache {
        3 ( 0.00%)              color_cache: vec![[0; 4]; 1 << bits],
       48 ( 0.00%)          let huffman_info = self.read_huffman_codes(is_argb_img, xsize, ysize, color_cache)?;
2,390,369 ( 5.70%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::read_huffman_codes (3x)
       32 ( 0.00%)      }
        2 ( 0.00%)          let mut xsize = self.width;
        6 ( 0.00%)          while self.bit_reader.read_bits::<u8>(1)? == 1 {
        4 ( 0.00%)              if self.transforms[usize::from(transform_type_val)].is_some() {
       10 ( 0.00%)              let transform_type = match transform_type_val {
        1 ( 0.00%)                      let size_bits = self.bit_reader.read_bits::<u8>(3)? + 2;
        1 ( 0.00%)                      let block_ysize = subsample_size(self.height, size_bits);
        3 ( 0.00%)                          vec![0; usize::from(block_xsize) * usize::from(block_ysize) * 4];
        9 ( 0.00%)                      self.decode_image_stream(block_xsize, block_ysize, false, &mut predictor_data)?;
   92,381 ( 0.22%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream (1x)
        1 ( 0.00%)                      let size_bits = self.bit_reader.read_bits::<u8>(3)? + 2;
        1 ( 0.00%)                      let block_ysize = subsample_size(self.height, size_bits);
        3 ( 0.00%)                          vec![0; usize::from(block_xsize) * usize::from(block_ysize) * 4];
       10 ( 0.00%)                      self.decode_image_stream(block_xsize, block_ysize, false, &mut transform_data)?;
  168,293 ( 0.40%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream (1x)
       18 ( 0.00%)              self.transforms[usize::from(transform_type_val)] = Some(transform_type);
       40 ( 0.00%)      fn read_huffman_codes(
        .                   color_cache: Option<ColorCache>,
       16 ( 0.00%)          let mut num_huff_groups = 1u32;
       14 ( 0.00%)          if read_meta && self.bit_reader.read_bits::<u8>(1)? == 1 {
        1 ( 0.00%)              huffman_bits = self.bit_reader.read_bits::<u8>(3)? + 2;
        4 ( 0.00%)              let mut data = vec![0; usize::from(huffman_xsize) * usize::from(huffman_ysize) * 4];
        8 ( 0.00%)              self.decode_image_stream(huffman_xsize, huffman_ysize, false, &mut data)?;
   95,066 ( 0.23%)  => src/lossless/decoder/mod.rs:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream'2 (1x)
        3 ( 0.00%)              entropy_image = data
    5,700 ( 0.01%)                      let meta_huff_code = (u16::from(pixel[0]) << 8) | u16::from(pixel[1]);
    3,801 ( 0.01%)                      if u32::from(meta_huff_code) >= num_huff_groups {
        9 ( 0.00%)                          num_huff_groups = u32::from(meta_huff_code) + 1;
        8 ( 0.00%)          let mut hufftree_groups = Vec::with_capacity(num_huff_groups as usize);
        4 ( 0.00%)          for _i in 0..num_huff_groups {
    1,365 ( 0.00%)                  if j == 0 {
    2,340 ( 0.01%)                  specs[j] = Some(self.read_huffman_code_spec(alphabet_size)?);
    1,287 ( 0.00%)                  let group: HuffmanCodeGroup9 = [
      195 ( 0.00%)                      specs[0].take().unwrap().build::<9>()?,
      195 ( 0.00%)                      specs[1].take().unwrap().build::<9>()?,
      195 ( 0.00%)                      specs[2].take().unwrap().build::<9>()?,
      195 ( 0.00%)                      specs[3].take().unwrap().build::<9>()?,
      156 ( 0.00%)                      specs[4].take().unwrap().build::<9>()?,
      273 ( 0.00%)                  hufftree_groups.push(HuffmanCodeGroup::Normal(group));
    1,140 ( 0.00%)  => ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:__memcpy_avx_unaligned_erms (38x)
       78 ( 0.00%)          }
    1,330 ( 0.00%)  => /rustc/48a229ceaefd4985c50990b14116b6d856af0985/library/core/src/ptr/mod.rs:core::ptr::drop_glue::<[core::option::Option<image_webp::lossless::decoder::HuffmanCodeSpec>; 5]> (38x)
       24 ( 0.00%)              huffman_code_groups: hufftree_groups,
       60 ( 0.00%)          Ok(info)
       32 ( 0.00%)      }
        .               fn read_huffman_code_spec(
      195 ( 0.00%)          let simple = self.bit_reader.read_bits::<u8>(1)? == 1;
      195 ( 0.00%)          if simple {
      284 ( 0.00%)              let zero_symbol = self.bit_reader.read_bits::<u16>(1 + 7 * is_first_8bits)?;
      142 ( 0.00%)              if zero_symbol >= alphabet_size {
      177 ( 0.00%)              if num_symbols == 1 {
      108 ( 0.00%)                  if one_symbol >= alphabet_size {
      372 ( 0.00%)              let mut code_length_code_lengths = [0u16; CODE_LENGTH_CODES];
    6,228 ( 0.01%)                  code_length_code_lengths[CODE_LENGTH_CODE_ORDER[i]] =
    1,240 ( 0.00%)                  self.read_huffman_code_lengths(&code_length_code_lengths, alphabet_size)?;
        .               fn read_huffman_code_lengths(
    2,108 ( 0.01%)          let table = HuffmanTree9::build_implicit(code_length_code_lengths)?;
  226,221 ( 0.54%)  => /home/runner/work/image-webp/image-webp/src/lossless/decoder/huffman.rs:<image_webp::lossless::decoder::huffman::HuffmanTree<9>>::build_implicit::<&[u16]> (123x)
      372 ( 0.00%)          let mut max_symbol = if self.bit_reader.read_bits::<u8>(1)? == 1 {
   20,968 ( 0.05%)          while symbol < num_symbols {
        .                       let code_len = table.read_symbol(&mut self.bit_reader)?;
    8,978 ( 0.02%)              if code_len < 16 {
    3,169 ( 0.01%)                  code_lengths[usize::from(symbol)] = code_len;
    3,169 ( 0.01%)                  symbol += 1;
   12,676 ( 0.03%)                  if code_len != 0 {
    1,320 ( 0.00%)                  let use_prev = code_len == 16;
   14,520 ( 0.03%)                  let extra_bits = match slot {
    2,640 ( 0.01%)                  let mut repeat = self.bit_reader.read_bits::<u16>(extra_bits)? + repeat_offset;
    3,960 ( 0.01%)                  if symbol + repeat > num_symbols {
    2,640 ( 0.01%)                  let length = if use_prev { prev_code_len } else { 0 };
   49,265 ( 0.12%)                  while repeat > 0 {
   12,417 ( 0.03%)                      code_lengths[usize::from(symbol)] = length;
    8,439 ( 0.02%)                      symbol += 1;
      496 ( 0.00%)          Ok(code_lengths)
        4 ( 0.00%)          let num_values = usize::from(width) * usize::from(height);
   23,274 ( 0.06%)          while index < num_values {
   23,214 ( 0.06%)              let (huff_index, block_end) = if huffman_info.bits == 0 {
   54,145 ( 0.13%)                  let y = index / width_usize;
    7,735 ( 0.02%)                  let meta_width = usize::from(huffman_info.xsize);
   15,470 ( 0.04%)                  let meta_x = x >> huffman_info.bits;
   15,470 ( 0.04%)                  let meta_y = y >> huffman_info.bits;
   23,205 ( 0.06%)                  let pos = meta_y * meta_width + meta_x;
    7,735 ( 0.02%)                  let huff_index = usize::from(huffman_info.image[pos]);
   15,470 ( 0.04%)                  let row_end = (meta_y + 1) * meta_width;
  166,583 ( 0.40%)                  while end_pos < row_end && usize::from(huffman_info.image[end_pos]) == huff_index {
    7,735 ( 0.02%)                  let run_end_meta = end_pos - meta_y * meta_width;
    7,735 ( 0.02%)                  let run_end_x = (run_end_meta << huffman_info.bits).min(width_usize);
    7,735 ( 0.02%)                  (huff_index, y * width_usize + run_end_x)
   15,476 ( 0.04%)              match &groups[huff_index] {
        4 ( 0.00%)          Ok(())
        8 ( 0.00%)      }
   55,177 ( 0.13%)  => /rustc/48a229ceaefd4985c50990b14116b6d856af0985/library/core/src/ptr/mod.rs:core::ptr::drop_glue::<image_webp::lossless::decoder::HuffmanInfo> (3x)
        .                   color_cache: &mut Option<ColorCache>,
  300,366 ( 0.72%)          while *index < num_values && *index < block_end {
        .                       let code = tree[GREEN].read_symbol(&mut self.bit_reader)?;
  381,149 ( 0.91%)              if code < 256 {
        .                           let red = tree[RED].read_symbol(&mut self.bit_reader)? as u8;
        .                           let blue = tree[BLUE].read_symbol(&mut self.bit_reader)? as u8;
  350,404 ( 0.84%)                  if self.bit_reader.nbits < 15 {
        .                           let alpha = tree[ALPHA].read_symbol(&mut self.bit_reader)? as u8;
  543,435 ( 1.30%)                  data[*index * 4] = red;
  543,435 ( 1.30%)                  data[*index * 4 + 1] = green;
  543,435 ( 1.30%)                  data[*index * 4 + 2] = blue;
  543,435 ( 1.30%)                  data[*index * 4 + 3] = alpha;
  108,687 ( 0.26%)                  *index += 1;
   36,564 ( 0.09%)              } else if code < 256 + 24 {
        .                           let length = Self::get_copy_distance(&mut self.bit_reader, length_symbol)?;
        .                           let dist_symbol = tree[DIST].read_symbol(&mut self.bit_reader)?;
        .                           let dist_code = Self::get_copy_distance(&mut self.bit_reader, dist_symbol)?;
   15,228 ( 0.04%)                  if *index < dist || num_values - *index < length {
   13,261 ( 0.03%)                  if dist == 1 {
    3,680 ( 0.01%)                      let value: [u8; 4] = data[(*index - dist) * 4..][..4].try_into().unwrap();
    9,835 ( 0.02%)                      if *index + length + 3 <= num_values {
    3,934 ( 0.01%)                          data.copy_within(start..start + 16, *index * 4);
    4,478 ( 0.01%)                          if length > 4 || dist < 4 {
    1,695 ( 0.00%)                              for i in (0..length * 4).step_by((dist * 4).min(16)).skip(1) {
  133,968 ( 0.32%)                                  data.copy_within(start + i..start + i + 16, *index * 4 + i);
    3,752 ( 0.01%)                          let cache_start = *index + length - cache_pixels;
    3,752 ( 0.01%)                          for pixel in data[cache_start * 4..][..cache_pixels * 4].chunks_exact(4) {
    3,680 ( 0.01%)                  *index += length;
   14,475 ( 0.03%)                  let color = color_cache.lookup((code - 280).into());
   14,475 ( 0.03%)                  data[*index * 4..][..4].copy_from_slice(&color);
   14,475 ( 0.03%)                  *index += 1;
   28,950 ( 0.07%)                  if *index < block_end {
   31,885 ( 0.08%)                      if let Some((bits, code)) = tree[GREEN].peek_symbol(&self.bit_reader) {
    4,570 ( 0.01%)                              data[*index * 4..][..4]
    4,570 ( 0.01%)                                  .copy_from_slice(&color_cache.lookup((code - 280).into()));
    4,570 ( 0.01%)                              *index += 1;
       16 ( 0.00%)          if self.bit_reader.read_bits::<u8>(1)? == 1 {
        1 ( 0.00%)              if !(1..=11).contains(&code_bits) {
        .                           return Err(DecodingError::InvalidColorCacheBits(code_bits));
        .               fn get_copy_distance(
   15,228 ( 0.04%)          if prefix_code < 4 {
    4,371 ( 0.01%)              return Ok(usize::from(prefix_code + 1));
    6,486 ( 0.02%)          let extra_bits: u8 = ((prefix_code - 2) >> 1).try_into().unwrap();
    9,729 ( 0.02%)          let offset = (2 + (usize::from(prefix_code) & 1)) << extra_bits;
    6,486 ( 0.02%)          Ok(offset + bits + 1)
   19,035 ( 0.05%)              let (xoffset, yoffset) = DISTANCE_MAP[plane_code - 1];
    7,614 ( 0.02%)              let dist = i32::from(xoffset) + i32::from(yoffset) * i32::from(xsize);
   11,421 ( 0.03%)              if dist < 1 {
        .           impl ColorCache {
  284,038 ( 0.68%)          let index = (0x1e35a7bdu32.wrapping_mul(color_u32)) >> (32 - self.color_cache_bits);
  604,405 ( 1.44%)          self.color_cache[index as usize] = color;
    4,570 ( 0.01%)          self.color_cache[index]
  390,054 ( 0.93%)          if buf.len() >= 8 {
  394,359 ( 0.94%)              self.reader.consume(usize::from((63 - self.nbits) / 8));
  394,714 ( 0.94%)              self.buffer |= lookahead << self.nbits;
  267,574 ( 0.64%)              self.nbits |= 56;
       45 ( 0.00%)              while !buf.is_empty() && self.nbits < 56 {
       31 ( 0.00%)                  self.buffer |= u64::from(buf[0]) << self.nbits;
       10 ( 0.00%)                  self.nbits += 8;
   25,391 ( 0.06%)          self.buffer & ((1 << num) - 1)
  385,349 ( 0.92%)          self.buffer
1,089,265 ( 2.60%)          if self.nbits < num {
  789,085 ( 1.88%)          self.buffer >>= num;
  400,178 ( 0.96%)          self.nbits -= num;
       14 ( 0.00%)      pub(crate) fn read_bits<T: TryFrom<u32>>(&mut self, num: u8) -> Result<T, DecodingError> {
    9,921 ( 0.02%)          if self.nbits < num {
      248 ( 0.00%)          let value = self.peek(num) as u32;
       14 ( 0.00%)      }
1,232,078 ( 2.94%)  <counts for unidentified lines in src/lossless/decoder/mod.rs>
9,542,163 (22.77%)  events annotated
```
