# Final VP8L slice-input confirmation

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- hashes + tests/docs/Clippy/fmt/MSRV 1.80.1 passed

| workload | baseline | candidate | paired median | positive | range |
|---|---:|---:|---:|---:|---:|
| corpus | 1097.444 us | 1107.323 us | 0.9908x | 2/25 | 0.9730–1.0049x |
| large | 19001.592 us | 19729.237 us | 0.9636x | 5/25 | 0.9129–1.0329x |
