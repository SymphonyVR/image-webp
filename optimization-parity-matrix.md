# Safe-Rust decode parity campaign

Goal: systematically test scalar/safe architectural optimizations suggested by libwebp and independently re-derived ideas inspired by ZenWebP's public high-level design notes. ZenWebP implementation code is not to be copied, translated, or adapted.

Constraints: `#![forbid(unsafe_code)]`, Rust 1.80.1 MSRV, no PR, final-tree A/B required before promotion.

## Retained
- VP8 fixed DCT token topology / raw probability rows / fused value+sign decode
- VP8 sparse IDCT dispatch
- VP8 loop-filter helper inlining
- ALPH written during final RGBA emission
- VP8L 9-bit Huffman root tables
- VP8L predictor-1 pixel recurrence
- VP8L periodic backreference color-cache tail updates

## Rejected / non-portable
- VP8 coefficient zero-run transaction fusion
- VP8 B_PRED fixed-tree specialization
- VP8 fancy YUV row-pair fusion
- residual block masks
- transform-add without sparse classification
- in-place speculative arithmetic state after final-tree composition
- VP8L 8-bit Huffman roots
- VP8L packed literal table graft
- VP8L trivial R/B/A literal fast path graft
- VP8L color+subtract-green pass fusion
- VP8L predictor-2 pixel recurrence (did not confirm)
- BitReader fill early return

## Running / must finish
- VP8 row-local reconstruct->filter pipeline, discard full-frame MacroBlock metadata
- VP8 read_coefficients out-of-line / branch-target-aliasing test
- VP8 rare coefficient magnitude/category path outlining
- VP8 fixed-size residue/prediction region bounds proof
- VP8 per-row prediction-border reuse
- VP8 animation scratch-buffer reuse
- VP8 decoder scratch/context reuse across animation frames
- VP8 direct predict+IDCT / remove 384-i32 residual staging
- VP8 macroblock-row YUV->RGB streaming / remove full-frame YUV output pass
- VP8 precomputed filter parameter table
- VP8 partition buffer allocation reuse
- VP8L bulk non-overlap LZ copy
- VP8L small-pattern / overlap copy variants
- VP8L deferred color-cache population
- VP8L single-Huffman-group position fast path
- VP8L contiguous Huffman table allocation/layout
- VP8L 16-row inverse-transform batching
- VP8L predictor-11 algebra simplification
- VP8L color-cache hash/collision reduction

## Acceptance
Correctness hashes first; then same-run alternating A/B pinned to one CPU. Small wins require independent confirmation. Candidate must still win when composed with the current `performance-optimizations` head before promotion.
