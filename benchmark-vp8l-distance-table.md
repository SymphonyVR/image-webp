# VP8L precomputed plane-distance benchmark

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests/docs/Clippy/fmt/MSRV 1.80.1 passed

| workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| corpus | 1060.018 us | 1068.275 us | 0.9921x | 0.9812–1.0014x |
| large | 17278.731 us | 18186.923 us | 0.9506x | 0.9208–0.9716x |
