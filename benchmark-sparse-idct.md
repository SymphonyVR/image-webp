# Sparse VP8 IDCT benchmark

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- candidate: `97c58735c03c72e8d7f54bcdfdd9a91276392b15`
- CPU: `Intel(R) Xeon(R) 6973P-C`
- full decoded outputs match before timing
- candidate passed tests, docs, Clippy, formatting, and Rust 1.80.1 build

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 251691.422 us | 247946.654 us | 1.018x | 0.954–1.165x |
| issue136 | 23024.274 us | 22317.785 us | 1.032x | 0.967–1.198x |
