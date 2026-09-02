# VP8L color coefficient-hoist current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 7763 64-Core Processor`
- coeff converts transform coefficients to i8 once per block; green hoists green signed conversion once per pixel; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | coeff | **0.9991x** | 7/17 | 0.9901–1.0064x |
| corpus | green | **0.9999x** | 8/17 | 0.9911–1.0145x |
| corpus | both | **1.0000x** | 8/17 | 0.9818–1.0157x |
| colorhot | coeff | **0.9997x** | 8/17 | 0.9911–1.0153x |
| colorhot | green | **0.9968x** | 6/17 | 0.9865–1.0119x |
| colorhot | both | **0.9991x** | 7/17 | 0.9695–1.0172x |
