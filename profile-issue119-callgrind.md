# Issue 119 post-optimization Callgrind profile

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- optimized branch: `46d1ebe66258fa20675590aba2ae2d501751e311`
- CPU: `AMD EPYC 7763 64-Core Processor`
- architecture / vCPUs: `x86_64` / `4`
- workload: exact issue #119 animated WebP
- profiler: Callgrind, one complete animation decode per variant, pinned to CPU 0
- release builds with line debug info; no source candidate applied

- main instruction references: `4,424,326,900`
- optimized instruction references: `3,457,093,835`
- instruction-count improvement: `1.280x` (21.86% fewer)

## Main filtered attribution

```text
4,424,326,900 (100.0%)  PROGRAM TOTALS
4,423,934,749 (99.99%)  ???:<image_webp::decoder::WebPDecoder<core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>::read_frame [/tmp/webp-main/target/release/examples/decode_profile]
2,603,434,706 (58.84%)  ???:<image_webp::lossy::Vp8Decoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_frame [/tmp/webp-main/target/release/examples/decode_profile]
```

## Optimized branch filtered attribution

```text
3,457,093,835 (100.0%)  PROGRAM TOTALS
3,456,699,275 (99.99%)  ???:<image_webp::decoder::WebPDecoder<core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>::read_frame [/tmp/webp-branch/target/release/examples/decode_profile]
2,603,432,987 (75.31%)  ???:<image_webp::lossy::Vp8Decoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_frame [/tmp/webp-branch/target/release/examples/decode_profile]
```
