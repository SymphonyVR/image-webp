# VP8L Huffman repeat-fill current-tree benchmark

- baseline: `84d8d20753fce0a9972e8a244fdf929b5a55671c`
- CPU: `AMD EPYC 7763 64-Core Processor`
- replaces scalar repeat-code writes with slice fill; full verification passed

| workload | paired median | positive | range |
|---|---:|---:|---:|
| corpus | **1.0021x** | 12/17 | 0.9750–1.0129x |
| large | **1.0057x** | 12/17 | 0.9784–1.0456x |
