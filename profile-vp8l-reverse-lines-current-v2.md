# VP8L reverse-transform explicit source profile v2

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- fixture: gallery2/3 lossless, 800x600
- explicit Callgrind source annotation; top nonzero instruction lines

```text
41,901,858 (100.0%)  PROGRAM TOTALS
7,542,142 (18.00%)  events annotated
2,640,000 ( 6.30%)      (i32::from(t) * i32::from(c)) as u32 >> 5
  806,903 ( 1.93%)  <counts for unidentified lines in src/lossless/decoder/reverse_transform.rs>
  634,704 ( 1.51%)          pixel[0] = pixel[0].wrapping_add(previous[0]);
  600,000 ( 1.43%)      let out = (argb & 0xff00_ff00) | red | (blue << 16);
  240,000 ( 0.57%)      red &= 0xff;
  240,000 ( 0.57%)      let mut blue = (argb >> 16) & 0xff;
  227,328 ( 0.54%)      (a & b) + ((a ^ b) >> 1)
  223,232 ( 0.53%)      (a + (a - b) / 2).max(0).min(255) as u8
  223,232 ( 0.53%)                  (i16::from(prev[0]) + i16::from(t[0])) / 2,
  194,208 ( 0.46%)          image_data[i] = image_data[i].wrapping_add(image_data[i - width * 4]);
  191,520 ( 0.46%)          if predict_left < predict_top {
  179,700 ( 0.43%)              let predictor = predictor_data[block_index * 4 + 1];
  120,000 ( 0.29%)      red += color_transform_delta(green_to_red as i8, green as i8);
  120,000 ( 0.29%)      blue += color_transform_delta(red_to_blue as i8, red as u8 as i8);
  120,000 ( 0.29%)      blue += color_transform_delta(green_to_blue as i8, green as i8);
  119,800 ( 0.29%)              match predictor {
  118,787 ( 0.28%)          image_data[i] = image_data[i].wrapping_add(image_data[i - width * 4 + 4]);
   93,472 ( 0.22%)      ((u16::from(a) + u16::from(b)) / 2) as u8
   91,392 ( 0.22%)      (a + b - c).max(0).min(255) as u8
   72,960 ( 0.17%)              predict_left += i16::abs(predict - l[i]);
   71,808 ( 0.17%)      while i < range.end {
   67,744 ( 0.16%)      while i < range.end {
   65,968 ( 0.16%)              image_data[i - width * 4 - 4],
   59,900 ( 0.14%)              let end_index = (y * width + ((block_x + 1) << size_bits).min(width)) * 4;
   58,368 ( 0.14%)              predict_top += i16::abs(predict - t[i]);
   43,348 ( 0.10%)          image_data[i] = image_data[i].wrapping_add(image_data[i - width * 4 - 4]);
   39,646 ( 0.09%)      assert!(range.end <= image_data.len());
   38,304 ( 0.09%)              image_data[i - width * 4],
   33,792 ( 0.08%)              chunk[0].wrapping_add(average2_autovec(average2_autovec(prev[0], tr[0]), t[0])),
   30,720 ( 0.07%)                  chunk[0].wrapping_add(average2_autovec(prev[0], t[0])),
   30,464 ( 0.07%)              chunk[0].wrapping_add(clamp_add_subtract_full(
   30,464 ( 0.07%)                  i16::from(tl[0]),
   30,464 ( 0.07%)                  i16::from(t[0]),
   30,000 ( 0.07%)              let red_to_blue = transform[0];
   30,000 ( 0.07%)              let green_to_red = transform[2];
   30,000 ( 0.07%)              let green_to_blue = transform[1];
   29,950 ( 0.07%)              let start_index = (y * width + (block_x << size_bits).max(1)) * 4;
   29,950 ( 0.07%)              let block_index = (y >> size_bits) * block_xsize + block_x;
   29,760 ( 0.07%)      while i < range.end {
   28,736 ( 0.07%)              image_data[i].wrapping_add(average2(image_data[i - 4], image_data[i - width * 4 - 4]));
   27,904 ( 0.07%)              chunk[0].wrapping_add(clamp_add_subtract_half(
   27,904 ( 0.07%)                  i16::from(tl[0]),
   26,112 ( 0.06%)          i += 1;
   25,296 ( 0.06%)              image_data[i - width * 4],
   24,528 ( 0.06%)      while i < range.end {
   17,280 ( 0.04%)      while i < range.end {
   16,576 ( 0.04%)      while i < range.end {
   14,688 ( 0.04%)              image_data[i - width * 4 + 4],
   14,592 ( 0.03%)              i16::from(top[0]),
   10,912 ( 0.03%)          image_data[i] = image_data[i].wrapping_add(average2(
   10,240 ( 0.02%)              chunk[0].wrapping_add(average2(average2(prev[0], tl[0]), average2(t[0], tr[0]))),
    8,988 ( 0.02%)                  image_data[y * width * 4 + i].wrapping_add(image_data[(y - 1) * width * 4 + i]);
    7,936 ( 0.02%)          i += 1;
    6,976 ( 0.02%)      let top_left = &old[range.start - width * 4 - 4..][..(range.end - range.start)];
    6,336 ( 0.02%)          image_data[i] = image_data[i].wrapping_add(average2(
    5,712 ( 0.01%)      let top_left = &old[range.start - width * 4 - 4..];
    4,608 ( 0.01%)          i += 1;
    4,096 ( 0.01%)          image_data[i] =
    3,264 ( 0.01%)      assert!(range.end <= image_data.len());
    2,816 ( 0.01%)      let top_right = &old[range.start - width * 4 + 4..];
    2,736 ( 0.01%)          i16::from(old[range.start - width * 4 - 4]),
    2,400 ( 0.01%)          let row_transform_data_start = (y >> size_bits) * block_xsize * 4;
    2,396 ( 0.01%)              image_data[y * width * 4 + i] =
    1,856 ( 0.00%)      assert!(range.end <= image_data.len());
    1,824 ( 0.00%)          i16::from(old[range.start - 4]),
      992 ( 0.00%)      assert!(range.end <= image_data.len());
      960 ( 0.00%)      let top_left = &old[range.start - width * 4 - 4..];
      912 ( 0.00%)      for (chunk, top) in current.chunks_exact_mut(4).zip(top.chunks_exact(4)) {
      672 ( 0.00%)      assert!(range.end <= image_data.len());
      576 ( 0.00%)      assert!(range.end <= image_data.len());
      160 ( 0.00%)      let top_right = &old[range.start - width * 4 + 4..];
      128 ( 0.00%)      assert!(range.end <= image_data.len());
       10 ( 0.00%)  pub(crate) fn apply_color_transform(
        9 ( 0.00%)  pub(crate) fn apply_predictor_transform(
        8 ( 0.00%)  }
        8 ( 0.00%)  }
        3 ( 0.00%)      image_data[3] = image_data[3].wrapping_add(255);
        3 ( 0.00%)      for pixel in image_data[range].chunks_exact_mut(4) {
        1 ( 0.00%)      if range.start % 4 != 0 || (range.end - range.start) % 4 != 0 {
        1 ( 0.00%)      for (y, row) in image_data.chunks_exact_mut(width * 4).enumerate() {
        1 ( 0.00%)      apply_predictor_transform_1(image_data, 4..width * 4, width);
        1 ( 0.00%)      Ok(())
```
