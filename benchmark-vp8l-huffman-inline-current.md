# Current-tree VP8L Huffman inline confirmation

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- `#[inline(always)]` on `HuffmanTree::read_symbol`
- full hashes + tests/docs/Clippy/fmt/MSRV 1.80.1 passed

| workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| corpus | 1144.271 us | 1137.053 us | 1.0063x | 0.9984–1.0121x |
| large | 18728.603 us | 18931.127 us | 0.9913x | 0.9420–1.0565x |
