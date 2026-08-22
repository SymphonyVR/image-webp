# Fused alpha-emission benchmark v2

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- candidate: `4b9a3669fc536fc97334ef84d152c3255662e0b5`
- CPU: `AMD EPYC 7763 64-Core Processor`
- verified candidate; full decoded outputs match before timing
- 17 alternating paired rounds

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 309750.838 us | 298994.428 us | 1.0362x | 0.9511–1.0562x |
| issue136 | 33612.536 us | 33565.150 us | 1.0007x | 0.9907–1.0081x |
