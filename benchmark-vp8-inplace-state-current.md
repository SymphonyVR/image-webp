# In-place VP8 arithmetic state current confirmation

- baseline: `0fdcb2f57d1d7dd272ee45d08e26fc80cb3f2aa8`
- candidate: `444de117b4c862adfd072997f0a1bd2be060aca5`
- CPU: `AMD EPYC 7763 64-Core Processor`
- full decoded outputs match before timing
- 21 alternating paired rounds

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 325111.500 us | 330687.045 us | 0.9846x | 0.9682–1.0298x |
| issue136 | 33612.123 us | 33632.639 us | 0.9999x | 0.9949–1.0079x |
