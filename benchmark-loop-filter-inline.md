# Horizontal loop-filter inline benchmark

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- candidate: `523bfb1778b7338c2b6a468cf8f4a8ba3441bf31`
- CPU: `AMD EPYC 7763 64-Core Processor`
- full decoded outputs match before timing

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 302747.500 us | 302072.371 us | 1.003x | 0.986–1.014x |
| issue136 | 33285.084 us | 33146.657 us | 1.004x | 0.995–1.009x |
