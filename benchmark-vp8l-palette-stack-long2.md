# VP8L small-palette stack high-iteration confirmation

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 7763 64-Core Processor`
- stack lookup table and scratchless reverse expansion; full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| palette | stack | **0.9993x** | 12/25 | 0.9752–1.0432x |
