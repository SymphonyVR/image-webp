# Fused VP8 transform-add benchmark

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- mask: `f932b8ca4df52027c1efdfd6400d7fcc666fcb88`
- fused: `53906d7967e8cafe21962044e510c10099bced30`
- CPU: `AMD EPYC 7763 64-Core Processor`
- full decoded outputs match before timing

| Workload | base | mask | fused | fused/base paired | fused/mask paired |
|---|---:|---:|---:|---:|---:|
| issue119 | 302215.102 us | 309973.566 us | 308751.099 us | 0.980x | 1.002x |
| issue136 | 33193.401 us | 33791.698 us | 33258.083 us | 0.998x | 1.016x |
