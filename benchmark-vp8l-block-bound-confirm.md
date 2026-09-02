# VP8L block-bound current-tree long confirmation

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 9V45 96-Core Processor`
- removes redundant image-end comparison from entropy block loop; full verification passed

| workload | paired median | positive | range |
|---|---:|---:|---:|
| corpus | **1.0015x** | 14/25 | 0.9596–1.1640x |
| large | **0.9919x** | 9/25 | 0.8999–1.0342x |
