# VP8L dense Huffman symbol-sort confirmation

- baseline: `84d8d20753fce0a9972e8a244fdf929b5a55671c`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed
- stores only nonzero-length symbols in the temporary sorted-symbol vector

| workload | paired median | positive | range |
|---|---:|---:|---:|
| corpus | **0.9991x** | 9/25 | 0.9944–1.0118x |
| large | **1.0200x** | 25/25 | 1.0113–1.0327x |
