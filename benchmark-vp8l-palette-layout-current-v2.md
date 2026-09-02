# VP8L small-palette layout current-tree matrix v2

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- stack lookup table and scratchless reverse expansion; full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | stack | **1.0089x** | 16/17 | 0.9990–1.0213x |
| corpus | reverse | **0.9948x** | 1/17 | 0.9764–1.0077x |
| corpus | both | **0.9956x** | 1/17 | 0.9905–1.0064x |
| palette | stack | **1.0072x** | 9/17 | 0.9414–1.0567x |
| palette | reverse | **0.8585x** | 0/17 | 0.8226–0.9222x |
| palette | both | **0.8565x** | 0/17 | 0.8152–0.9272x |
