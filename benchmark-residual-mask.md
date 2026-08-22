# Per-block residual mask benchmark

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- candidate: `f932b8ca4df52027c1efdfd6400d7fcc666fcb88`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- full decoded outputs match before timing

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 290763.260 us | 300629.520 us | 0.980x | 0.919–1.026x |
| issue136 | 28538.412 us | 28802.862 us | 0.992x | 0.931–1.033x |
