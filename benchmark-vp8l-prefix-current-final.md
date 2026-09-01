# VP8L prefix-decode current-final matrix

- baseline: `0881ec1a66f09e11b766c309cf6e651077775bd9`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | table | **0.9876x** | 2/17 | 0.9217–1.0036x |
| corpus | pair | **1.0010x** | 10/17 | 0.9336–1.0250x |
| large | table | **0.8980x** | 0/17 | 0.8817–0.9119x |
| large | pair | **0.9984x** | 4/17 | 0.9744–1.0128x |
