# VP8L batched literal Huffman long confirmation

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- primary-table peeks decode multiple literal channels with one bit consume; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | rgb | **1.0011x** | 19/25 | 0.9969–1.0096x |
| large | rgb | **0.9993x** | 12/25 | 0.9787–1.0374x |
