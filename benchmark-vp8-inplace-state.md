# In-place VP8 arithmetic-state benchmark

- baseline: `41490df368bb675e1f50922329b390968d352f10`
- candidate: `7c08b7b5d3ed3f2fa5000ebeac0f6d8d2d8e31ce`
- CPU: `AMD EPYC 7763 64-Core Processor`
- full decoded outputs match before timing
- candidate already passed tests, docs, Clippy, formatting, and Rust 1.80.1

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 293097.589 us | 283775.114 us | 1.0334x | 1.0084–1.0469x |
| issue136 | 31431.340 us | 30930.800 us | 1.0168x | 1.0140–1.0228x |
