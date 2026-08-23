# Final VP8L Huffman allocation confirmation

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- hashes + tests/docs/Clippy/fmt/MSRV 1.80.1 passed

| workload | baseline | candidate | paired median | positive | range |
|---|---:|---:|---:|---:|---:|
| corpus | 1139.204 us | 1134.737 us | 1.0045x | 24/25 | 0.9989–1.0089x |
| large | 18194.655 us | 18210.857 us | 0.9996x | 10/25 | 0.9826–1.0056x |
