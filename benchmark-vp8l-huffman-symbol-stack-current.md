# VP8L Huffman symbol-stack current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 7763 64-Core Processor`
- fixed stack scratch for common Huffman alphabets; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | s256 | **1.0156x** | 11/13 | 0.9777–1.0201x |
| corpus | s512 | **1.0150x** | 13/13 | 1.0082–1.0173x |
| large | s256 | **1.0643x** | 13/13 | 1.0334–1.0994x |
| large | s512 | **1.0732x** | 13/13 | 1.0401–1.1133x |
