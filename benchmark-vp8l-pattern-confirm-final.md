# Final VP8L overlap-pattern confirmation

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- candidate: `986bb712b5b4c908059d2f19ad65a53119408eec`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests/docs/Clippy/fmt/MSRV 1.80.1 passed
- 25 alternating paired rounds; large workload uses 8 decodes/sample

| workload | baseline | candidate | paired median | positive rounds | range |
|---|---:|---:|---:|---:|---:|
| corpus | 1062.261 us | 1074.239 us | 0.9876x | 3/25 | 0.9825–1.0074x |
| large | 16885.782 us | 17125.504 us | 0.9848x | 2/25 | 0.9464–1.0153x |
