# VP8L zero-coefficient color-transform current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- allzero skips transform blocks whose three coefficients are zero; mask dispatches compile-time-specialized arithmetic for all coefficient-presence masks; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | allzero | **1.0204x** | 16/17 | 0.9989–1.0590x |
| corpus | mask | **1.0070x** | 16/17 | 0.9889–1.0433x |
| colorhot | allzero | **1.0165x** | 17/17 | 1.0025–1.0303x |
| colorhot | mask | **1.0085x** | 16/17 | 0.9978–1.0211x |
