# Safe-Rust WebP performance parity audit

Goal: systematically test scalar/algorithmic optimizations available from the permissively licensed libwebp reference implementation, while keeping this fork `#![forbid(unsafe_code)]` and Rust 1.80.1 compatible. ZenWebP is used only for public architectural/benchmark inspiration; implementation code is not copied or translated.

## Acceptance gate

A candidate is retained only when decoded outputs match, stable tests/docs/clippy/fmt pass, Rust 1.80.1 builds, and same-run paired benchmarks show a repeatable win on the final composed tree.

## VP8 / lossy

| Candidate | Status | Notes |
|---|---|---|
| Fixed DCT token topology / fused category+sign decode | retained | ~11-12% #119 gain across multiple runners |
| Sparse none/DC/AC3/full IDCT selection | retained | confirmed ~1.5-1.9% |
| ALPH write fused into RGB->RGBA emission | retained | confirmed multi-percent #119 gain |
| Loop-filter helper inlining | retained | small repeatable #136 gain |
| DCT zero-run transaction fusion | rejected | regressed |
| Generic fixed prediction-tree specialization | rejected | regressed |
| Arithmetic state in-place mutation | rejected after composition | isolated win disappeared on final tree |
| Residual block masks | rejected | mask/branch cost exceeded saved work |
| Transform-add fusion without sparse dispatch | rejected | neutral #119 |
| Fancy YUV row-pair fusion | rejected | large regression |
| Range/leaf micro-optimizations | rejected/not portable | CPU-sensitive |
| Safe horizontal filter max-diff rewrite | rejected | regressed |
| Full transform-add combined with sparse dispatch | pending | retest only as complete fused architecture |
| Macroblock-local reconstruction/filter streaming | pending | direct libwebp/streaming architecture class |
| Single-core vs optional threaded decode lane | pending | keep separate from algorithmic benchmark lane |

## VP8L / lossless

| Candidate | Status | Notes |
|---|---|---|
| 9-bit Huffman primary table | retained | two positive runs; better than 8 or 10 bits here |
| Predictor-1 pixel-wise recurrence | retained | survives composition |
| Backreference periodic cache-tail update | retained | ~8.5% on 2048x2048 LZ-heavy workload |
| 8-bit Huffman root | rejected | worse than 9-bit |
| 64-entry packed literal table | rejected | corpus regression |
| Trivial R/B/A literal channel fast path | rejected | corpus regression |
| Deferred `last_cached` cache population | rejected | corpus 0.9756x, large 0.9386x |
| Predictor-2 pixel kernel | rejected | confirmation neutral |
| Color + subtract-green pass fusion | rejected | neutral/regressive |
| BitReader early-fill shortcut | rejected | regressed |
| Safe color-transform SLP variants | rejected | neutral/regressive end-to-end |
| libwebp non-overlap bulk copy (`dist >= length`) | running | direct safe equivalent of scalar memcpy path |
| libwebp distance-1/2 small-pattern copy | running | safe 8-byte pattern kernel |
| libwebp single-Huffman-group hoist | running | avoid row/block recomputation when meta bits=0 |
| libwebp 16-row inverse-transform batches | running | current-tree rebase |
| Contiguous compressed/slice-backed input | running | tests cost of staging input vs hotter entropy loop |
| Contiguous primary+secondary Huffman storage | pending/rerun | old harness did not persist a verdict |
| Overlap pattern copy strategy | pending/rerun | compare forward copy, chunked copy, doubling |
| Predictor-11 algebra simplification | pending/rerun | remove unnecessary temporary prediction arithmetic |
| Packed u32 pixel/LZ/cache representation | pending | major architectural candidate; libwebp native representation |
| All-group Huffman table arena / allocation reduction | pending | libwebp-style table storage architecture |
| Huffman code-length workspace reuse | pending | reduce setup allocations for many groups |
| Color-cache packed representation / hash path | pending | test independently and with packed pixels |
| Full row-streaming inverse-transform pipeline including palette | pending | larger form of row batching |
| Direct RGB/no-alpha specialization | pending | avoid unnecessary alpha/channel work where legal |
| Distance/length decode table shaping | pending | compare scalar reference organization |

## Architectural priorities

1. VP8L entropy/LZ path: current profiling attributes roughly 58% of instructions here.
2. Safe bulk/pattern backreference copies and cache maintenance.
3. Packed-pixel internal representation.
4. Huffman table/storage/setup architecture.
5. Row-local inverse transforms and streaming reconstruction.
6. Reprofile, then repeat against remaining libwebp scalar differences.
