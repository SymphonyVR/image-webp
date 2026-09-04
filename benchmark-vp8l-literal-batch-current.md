# VP8L batched literal Huffman current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 7763 64-Core Processor`
- primary-table peeks decode multiple literal channels with one bit consume; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | rgb | **1.0182x** | 16/17 | 0.9720–1.0204x |
| corpus | rgba | **0.9643x** | 0/17 | 0.9432–0.9727x |
| large | rgb | **1.0630x** | 17/17 | 1.0561–1.0706x |
| large | rgba | **0.8806x** | 0/17 | 0.8739–0.9008x |
