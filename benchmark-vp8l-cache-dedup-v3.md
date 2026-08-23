# VP8L cache-tail bitmap dedup matrix

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 7763 64-Core Processor`
- all variants pass full hashes + tests/docs/Clippy/fmt/MSRV 1.80.1

| workload | threshold | base median | candidate median | paired speedup | range |
|---|---:|---:|---:|---:|---:|
| corpus | 8 | 1060.390 us | 1088.392 us | 0.9743x | 0.9683–0.9822x |
| corpus | 16 | 1060.390 us | 1059.780 us | 1.0006x | 0.9826–1.0095x |
| corpus | 32 | 1060.390 us | 1061.881 us | 1.0013x | 0.9766–1.0103x |
| corpus | 64 | 1060.390 us | 1059.549 us | 1.0008x | 0.9783–1.0128x |
| large | 8 | 17203.904 us | 21086.790 us | 0.8174x | 0.7855–0.8296x |
| large | 16 | 17203.904 us | 19675.415 us | 0.8728x | 0.8466–0.8995x |
| large | 32 | 17203.904 us | 18096.789 us | 0.9545x | 0.9163–0.9865x |
| large | 64 | 17203.904 us | 17629.140 us | 0.9774x | 0.9336–1.0178x |
