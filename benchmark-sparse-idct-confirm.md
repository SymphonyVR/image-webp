# Sparse VP8 IDCT confirmation

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- candidate: `97c58735c03c72e8d7f54bcdfdd9a91276392b15`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- full decoded outputs match before timing
- 21 alternating paired rounds; 5 issue119 and 50 issue136 decodes per timed sample

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 234913.349 us | 231498.855 us | 1.0145x | 1.0031–1.0257x |
| issue136 | 26060.514 us | 25607.040 us | 1.0190x | 1.0019–1.0326x |
