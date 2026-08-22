# Alpha-emission current-baseline confirmation

- baseline: `677794add99a6a68eeb3e183853480e2308ac4f8`
- candidate: `efd50f244c0e232ea7bebc8624d8fe071a100ce5`
- CPU: `AMD EPYC 7763 64-Core Processor`
- full decoded outputs match before timing
- 21 alternating paired rounds

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 309614.155 us | 295086.964 us | 1.0454x | 1.0194–1.0606x |
| issue136 | 33457.482 us | 33428.991 us | 1.0006x | 0.9597–1.0097x |
