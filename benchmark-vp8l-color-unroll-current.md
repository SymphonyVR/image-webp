# VP8L color-transform manual-unroll current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz`
- manually exposes 2/4/8 independent pixels per transform block to LLVM; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | u2 | **0.9145x** | 0/17 | 0.9070–0.9224x |
| corpus | u4 | **0.9349x** | 0/17 | 0.9278–0.9470x |
| corpus | u8 | **0.9798x** | 0/17 | 0.9725–0.9869x |
| colorhot | u2 | **0.9600x** | 0/17 | 0.9024–0.9671x |
| colorhot | u4 | **0.9348x** | 0/17 | 0.8739–0.9430x |
| colorhot | u8 | **0.9805x** | 0/17 | 0.9512–0.9924x |
