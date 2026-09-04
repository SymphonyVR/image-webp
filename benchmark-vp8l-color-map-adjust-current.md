# VP8L color-map adjustment current-tree benchmark

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `Intel(R) Xeon(R) 6973P-C`
- safe packed four-lane cumulative palette reconstruction; hashes + full verification passed

| workload | paired median | positive | range |
|---|---:|---:|---:|
| corpus | **0.9927x** | 2/17 | 0.8622–1.0635x |
| palette256 | **1.0068x** | 12/17 | 0.9428–1.0817x |
