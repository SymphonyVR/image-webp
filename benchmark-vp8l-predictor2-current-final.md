# Current-tree VP8L predictor-2 confirmation

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- hashes + tests/docs/Clippy/fmt/MSRV 1.80.1 passed

| workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| corpus | 1144.586 us | 1144.507 us | 0.9990x | 0.9892–1.0182x |
| large | 18439.087 us | 18385.341 us | 1.0009x | 0.9728–1.1807x |
