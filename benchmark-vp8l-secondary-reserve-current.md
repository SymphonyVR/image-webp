# VP8L secondary Huffman reserve current-tree matrix

- baseline: `84d8d20753fce0a9972e8a244fdf929b5a55671c`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | r32 | **1.0039x** | 10/13 | 0.9708–1.0091x |
| corpus | r64 | **1.0077x** | 11/13 | 0.9910–1.0230x |
| corpus | r128 | **1.0078x** | 13/13 | 1.0013–1.0179x |
| large | r32 | **1.0071x** | 13/13 | 1.0008–1.0448x |
| large | r64 | **1.0103x** | 10/13 | 0.9815–1.0502x |
| large | r128 | **1.0035x** | 13/13 | 1.0006–1.0322x |
