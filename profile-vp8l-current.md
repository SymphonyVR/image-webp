# Current VP8L Callgrind profile

- CPU: `AMD EPYC 7763 64-Core Processor`
- fixture: `tests/images/gallery2/3_webp_ll.webp` (800x600)
- one full static decode; normal release; CPU 0

## Exclusive

```text
52,113,888 (100.0%)  PROGRAM TOTALS
30,352,524 (58.24%)  ???:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream [/home/runner/work/image-webp/image-webp/target/release/examples/profile_vp8l]
```

## Inclusive

```text
52,113,888 (100.0%)  PROGRAM TOTALS
```
