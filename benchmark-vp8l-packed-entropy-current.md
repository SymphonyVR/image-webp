# VP8L packed entropy-buffer current-tree benchmark

- baseline: `84d8d20753fce0a9972e8a244fdf929b5a55671c`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- safe `[u8; 4]` pixel lanes during entropy/LZ decode, one final byte-buffer copy
- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed

| workload | paired median | positive | range |
|---|---:|---:|---:|
| corpus | **0.9773x** | 0/17 | 0.9727–0.9974x |
| large | **0.8909x** | 0/17 | 0.8462–0.9059x |
| repeat | **0.8449x** | 0/17 | 0.7925–0.9371x |
