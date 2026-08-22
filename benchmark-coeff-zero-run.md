# VP8 coefficient zero-run benchmark

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- candidate: `fec072e93406b08ff91ac1f538a886d54dae2a16`
- CPU: `AMD EPYC 7763 64-Core Processor`
- full decoded outputs match before timing

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 304558.113 us | 309465.584 us | 0.983x | 0.978–0.989x |
| issue136 | 33254.709 us | 33574.720 us | 0.990x | 0.987–1.003x |
