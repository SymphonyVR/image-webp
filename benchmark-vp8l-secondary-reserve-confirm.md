# VP8L secondary Huffman reserve long confirmation

- baseline: `84d8d20753fce0a9972e8a244fdf929b5a55671c`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | r64 | **1.0058x** | 23/25 | 0.9836–1.0128x |
| corpus | r128 | **1.0056x** | 22/25 | 0.9932–1.0130x |
| large | r64 | **1.0117x** | 20/25 | 0.8236–1.0522x |
| large | r128 | **1.0119x** | 23/25 | 0.9180–1.0650x |
