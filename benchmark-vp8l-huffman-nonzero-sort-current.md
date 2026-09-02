# VP8L Huffman nonzero-symbol sort current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- excludes zero-length symbols from sort scratch; dense_stack also uses 512-entry stack scratch; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | dense | **0.9989x** | 4/17 | 0.9947–1.0026x |
| corpus | dense_stack | **1.0039x** | 17/17 | 1.0013–1.0054x |
| large | dense | **0.9989x** | 8/17 | 0.9873–1.0215x |
| large | dense_stack | **0.9712x** | 0/17 | 0.9503–0.9951x |
