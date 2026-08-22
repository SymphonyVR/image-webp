# Alpha-emission + sparse-IDCT confirmation

- baseline: `41490df368bb675e1f50922329b390968d352f10`
- candidate: `0fdcb2f57d1d7dd272ee45d08e26fc80cb3f2aa8`
- CPU: `AMD EPYC 7763 64-Core Processor`
- full decoded outputs match before timing
- 21 alternating paired rounds

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 300080.579 us | 281870.765 us | 1.0612x | 1.0329–1.0726x |
| issue136 | 31739.165 us | 31866.378 us | 0.9969x | 0.9870–1.0157x |
