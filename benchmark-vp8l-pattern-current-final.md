# Current-tree VP8L overlap-pattern confirmation

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- hashes + tests/docs/Clippy/fmt/MSRV 1.80.1 passed

| workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| corpus | 896.837 us | 882.305 us | 1.0125x | 1.0075–1.0247x |
| large | 14555.365 us | 14007.405 us | 1.0319x | 0.9863–1.0898x |
