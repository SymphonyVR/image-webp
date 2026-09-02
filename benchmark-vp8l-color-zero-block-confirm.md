# VP8L zero-coefficient color-block long confirmation

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 7763 64-Core Processor`
- allzero skips transform blocks whose three coefficients are zero; mask dispatches compile-time-specialized arithmetic for all coefficient-presence masks; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | allzero | **1.0181x** | 25/25 | 1.0106–1.0249x |
| colorhot | allzero | **1.0200x** | 24/25 | 0.9989–1.0431x |
