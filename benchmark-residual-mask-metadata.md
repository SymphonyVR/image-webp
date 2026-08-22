# Coefficient-derived residual mask benchmark

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- candidate: `2f55ca30afa6109813b716a14bef10f687438c63`
- CPU: `AMD EPYC 7763 64-Core Processor`
- full decoded outputs match before timing

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 305188.630 us | 313546.047 us | 0.973x | 0.965–0.980x |
| issue136 | 33694.941 us | 34255.392 us | 0.983x | 0.975–1.001x |
