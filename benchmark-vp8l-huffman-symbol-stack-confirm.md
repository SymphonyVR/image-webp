# VP8L Huffman symbol-stack current-tree long confirmation

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- fixed stack scratch for common Huffman alphabets; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | s512 | **0.9860x** | 0/25 | 0.9645–0.9999x |
| large | s512 | **0.9328x** | 0/25 | 0.9054–0.9475x |
