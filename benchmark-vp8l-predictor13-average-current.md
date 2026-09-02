# VP8L predictor13 average current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 7763 64-Core Processor`
- replaces predictor13 i16 add/divide average with equivalent byte average; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | avg | **1.0003x** | 9/17 | 0.9924–1.0055x |
| corpus | autovec | **0.9941x** | 2/17 | 0.9770–1.0030x |
| p13hot | avg | **1.0010x** | 10/17 | 0.9434–1.0244x |
| p13hot | autovec | **0.9996x** | 8/17 | 0.9238–1.0228x |
