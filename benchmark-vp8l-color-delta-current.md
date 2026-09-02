# VP8L color-delta current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- tests narrower signed multiply and byte-domain channel accumulation; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | i16u32 | **1.0048x** | 15/17 | 0.9860–1.0093x |
| corpus | u8packed | **1.0005x** | 9/17 | 0.9908–1.0073x |
| corpus | u8array | **0.8357x** | 0/17 | 0.8093–0.8389x |
| colorhot | i16u32 | **1.0134x** | 16/17 | 0.9408–1.0529x |
| colorhot | u8packed | **1.0070x** | 14/17 | 0.9965–1.0483x |
| colorhot | u8array | **0.8019x** | 0/17 | 0.7910–0.8123x |
