# Fixed-ref libwebp-style coefficient cross-runner benchmark

- baseline: `915e24eb765a4cf5e29cf5e797cc28ac71d041ba`
- candidate: `13448c6a17180ee9939154b052dd70b44cd1729c`
- issue119; full-output hash equality checked on every runner
- release `target-cpu=native`; CPU 0; 9 alternating paired rounds

| Runner | CPU | baseline median | candidate median | paired median | range |
|---:|---|---:|---:|---:|---:|
| 1 | AMD EPYC 9V74 80-Core Processor | 355251.908 us | 316492.422 us | 1.122x | 1.106–1.137x |
| 2 | AMD EPYC 9V74 80-Core Processor | 354049.711 us | 315521.350 us | 1.122x | 1.118–1.138x |
| 3 | AMD EPYC 9V74 80-Core Processor | 268606.705 us | 236727.845 us | 1.134x | 1.126–1.140x |
| 4 | AMD EPYC 7763 64-Core Processor | 351768.531 us | 311946.827 us | 1.128x | 1.124–1.138x |

- aggregate paired median: **1.126x**
- aggregate range: **1.106–1.140x**
