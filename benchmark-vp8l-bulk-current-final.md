# Current-tree VP8L bulk backreference confirmation

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests/docs/Clippy/fmt/MSRV 1.80.1 passed

| workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| corpus | 1062.041 us | 1065.245 us | 0.9956x | 0.9737–1.0242x |
| large | 17429.467 us | 17836.761 us | 0.9776x | 0.9539–0.9921x |
