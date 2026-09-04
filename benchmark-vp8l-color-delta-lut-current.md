# VP8L color-delta LUT current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 7763 64-Core Processor`
- 64 KiB exact modulo-256 delta table; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | lut | **0.9041x** | 0/17 | 0.8873–0.9104x |
| corpus | lutzero | **0.9761x** | 0/17 | 0.9660–0.9820x |
| colorhot | lut | **0.8761x** | 0/17 | 0.8591–0.8922x |
| colorhot | lutzero | **0.9619x** | 0/17 | 0.9505–0.9816x |
