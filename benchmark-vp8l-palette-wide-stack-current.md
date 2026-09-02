# VP8L wide-palette fixed-table benchmark

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 7763 64-Core Processor`
- fixed [[u8;4];256] palette table; hashes + full verification passed

| workload | paired median | positive | range |
|---|---:|---:|---:|
| corpus | **1.0004x** | 11/17 | 0.9921–1.0177x |
| palette64 | **1.0300x** | 15/17 | 0.9438–1.1070x |
