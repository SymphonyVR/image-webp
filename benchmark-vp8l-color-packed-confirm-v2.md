# Final VP8L packed-color confirmation

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- 25 alternating paired rounds; full hashes/tests/docs/Clippy/fmt/MSRV passed

| workload | baseline | candidate | paired median | positive | range |
|---|---:|---:|---:|---:|---:|
| corpus | 1095.520 us | 1031.723 us | 1.0618x | 25/25 | 1.0387–1.0830x |
| large | 11851.815 us | 10587.545 us | 1.1064x | 25/25 | 1.0652–1.1595x |
| color | 13974.246 us | 14190.789 us | 0.9847x | 11/25 | 0.8874–1.1325x |
