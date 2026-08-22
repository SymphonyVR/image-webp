# Fixed-ref Y2 extent benchmark

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- candidate: `14f163a9d2b1e6a7c34d33259bb78311e6fe3ef4`
- CPU: `AMD EPYC 7763 64-Core Processor`
- full-output hashes match outside timed region

| Workload | baseline | candidate | speedup | paired median | range |
|---|---:|---:|---:|---:|---:|
| issue119 | 301846.826 us | 304595.698 us | 0.991x | 0.992x | 0.982–1.010x |
| issue136 | 33272.621 us | 33230.323 us | 1.001x | 1.001x | 0.997–1.006x |
