# Fancy YUV row-pair benchmark

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- candidate: `22938e493eaeb0c9a6dda3d743ab4d1f58ee6762`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- full decoded outputs match before timing

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 236298.349 us | 286385.387 us | 0.825x | 0.819–0.832x |
| issue136 | 26225.608 us | 30163.113 us | 0.868x | 0.859–0.877x |
