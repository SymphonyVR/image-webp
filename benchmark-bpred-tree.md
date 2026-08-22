# Fixed VP8 B_PRED tree benchmark

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- candidate: `f03bebe621138769679680c3231045de51c3f6b8`
- CPU: `AMD EPYC 7763 64-Core Processor`
- full decoded outputs match before timing

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 307659.039 us | 312794.108 us | 0.987x | 0.975–1.085x |
| issue136 | 33597.134 us | 33722.626 us | 0.997x | 0.986–1.006x |
