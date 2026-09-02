# VP8L small-palette stack current-tree long confirmation

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- stack lookup table and scratchless reverse expansion; full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | stack | **1.0085x** | 24/25 | 0.9966–1.0158x |
| palette | stack | **1.0043x** | 14/25 | 0.9404–1.1589x |
