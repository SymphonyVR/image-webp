# VP8L source-line Callgrind profile

- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- fixture: gallery2/3_webp_ll.webp (800x600)
- exact current optimized source; one full decode

## decoder/mod.rs

```text
--------------------------------------------------------------------------------
Profile data file '/tmp/v.callgrind' (creator: callgrind-3.22.0)
--------------------------------------------------------------------------------
I1 cache: 
D1 cache: 
LL cache: 
Timerange: Basic block 0 - 6759909
Trigger: Program termination
Profiled target:  target/release/examples/profile_vp8l_lines (PID 3868, part 1)
Events recorded:  Ir
Events shown:     Ir
Event sort order: Ir
Thresholds:       0.01
Include dirs:     
User annotated:   src/lossless/decoder/mod.rs
Auto-annotation:  on

--------------------------------------------------------------------------------
Ir                  
--------------------------------------------------------------------------------
51,062,552 (100.0%)  PROGRAM TOTALS

--------------------------------------------------------------------------------
Ir                   file:function
--------------------------------------------------------------------------------
29,381,853 (57.54%)  ???:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream [/home/runner/work/image-webp/image-webp/target/release/examples/profile_vp8l_lines]

--------------------------------------------------------------------------------
-- User-annotated source: src/lossless/decoder/mod.rs
--------------------------------------------------------------------------------
  No information has been collected for src/lossless/decoder/mod.rs


```

## huffman.rs

```text
--------------------------------------------------------------------------------
Profile data file '/tmp/v.callgrind' (creator: callgrind-3.22.0)
--------------------------------------------------------------------------------
I1 cache: 
D1 cache: 
LL cache: 
Timerange: Basic block 0 - 6759909
Trigger: Program termination
Profiled target:  target/release/examples/profile_vp8l_lines (PID 3868, part 1)
Events recorded:  Ir
Events shown:     Ir
Event sort order: Ir
Thresholds:       0.01
Include dirs:     
User annotated:   src/lossless/decoder/huffman.rs
Auto-annotation:  on

--------------------------------------------------------------------------------
Ir                  
--------------------------------------------------------------------------------
51,062,552 (100.0%)  PROGRAM TOTALS

--------------------------------------------------------------------------------
Ir                   file:function
--------------------------------------------------------------------------------
29,381,853 (57.54%)  ???:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream [/home/runner/work/image-webp/image-webp/target/release/examples/profile_vp8l_lines]

--------------------------------------------------------------------------------
-- User-annotated source: src/lossless/decoder/huffman.rs
--------------------------------------------------------------------------------
  No information has been collected for src/lossless/decoder/huffman.rs


```

## reverse_transform.rs

```text
--------------------------------------------------------------------------------
Profile data file '/tmp/v.callgrind' (creator: callgrind-3.22.0)
--------------------------------------------------------------------------------
I1 cache: 
D1 cache: 
LL cache: 
Timerange: Basic block 0 - 6759909
Trigger: Program termination
Profiled target:  target/release/examples/profile_vp8l_lines (PID 3868, part 1)
Events recorded:  Ir
Events shown:     Ir
Event sort order: Ir
Thresholds:       0.01
Include dirs:     
User annotated:   src/lossless/decoder/reverse_transform.rs
Auto-annotation:  on

--------------------------------------------------------------------------------
Ir                  
--------------------------------------------------------------------------------
51,062,552 (100.0%)  PROGRAM TOTALS

--------------------------------------------------------------------------------
Ir                   file:function
--------------------------------------------------------------------------------
29,381,853 (57.54%)  ???:<image_webp::lossless::decoder::LosslessDecoder<core::io::util::Take<&mut core::io::cursor::Cursor<alloc::vec::Vec<u8>>>>>::decode_image_stream [/home/runner/work/image-webp/image-webp/target/release/examples/profile_vp8l_lines]

--------------------------------------------------------------------------------
-- User-annotated source: src/lossless/decoder/reverse_transform.rs
--------------------------------------------------------------------------------
  No information has been collected for src/lossless/decoder/reverse_transform.rs


```
