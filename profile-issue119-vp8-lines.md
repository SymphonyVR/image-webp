# Issue 119 VP8 source-line profile

- optimized branch: `59737e51c877fb77f5fdcb39aedc6ace692adad5`
- CPU: `AMD EPYC 7763 64-Core Processor`
- architecture / vCPUs: `x86_64` / `4`
- workload: exact issue #119 animated WebP
- Callgrind, one full animation decode, normal release codegen, CPU 0
- source-line costs are exclusive instruction references from optimized code
- program instruction references: `3,457,081,911`

## Hot image-webp functions

```text
904,894,508 (26.18%)  ???:<image_webp::lossy::arithmetic_decoder::ArithmeticDecoder>::read_with_tree_with_first_node [/home/runner/work/image-webp/image-webp/target/release/examples/decode_profile]
```

## `src/lossy/mod.rs`

```text
(no attributed source lines found)
```

## `src/lossy/arithmetic_decoder.rs`

```text
(no attributed source lines found)
```

## `src/lossy/yuv.rs`

```text
(no attributed source lines found)
```

## `src/lossy/loop_filter.rs`

```text
(no attributed source lines found)
```

## `src/lossy/transform.rs`

```text
(no attributed source lines found)
```

## `src/lossy/prediction.rs`

```text
(no attributed source lines found)
```
