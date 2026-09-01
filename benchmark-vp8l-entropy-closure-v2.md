# VP8L entropy closure matrix

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 7763 64-Core Processor`
- static VP8L fixtures: `10`
- all candidates: decoded hashes match; cargo test and Rust 1.80.1 build pass

| workload | candidate | base median | candidate median | paired median | positive | range |
|---|---|---:|---:|---:|---:|---:|
| corpus | repeat | 1081.200 us | 1088.953 us | 0.9930x | 3/15 | 0.9806–1.0015x |
| corpus | prealloc | 1081.200 us | 1071.951 us | 1.0074x | 14/15 | 0.9966–1.0132x |
| corpus | literal | 1081.200 us | 1082.436 us | 0.9987x | 3/15 | 0.9881–1.0129x |
| corpus | prefix | 1081.200 us | 1082.731 us | 0.9985x | 5/15 | 0.9679–1.0048x |
| corpus | all | 1081.200 us | 1078.241 us | 1.0013x | 9/15 | 0.9929–1.0114x |
| large | repeat | 18005.641 us | 18325.506 us | 0.9864x | 3/15 | 0.9361–1.0275x |
| large | prealloc | 18005.641 us | 18061.135 us | 0.9962x | 6/15 | 0.8669–1.0124x |
| large | literal | 18005.641 us | 18509.970 us | 0.9728x | 0/15 | 0.9248–0.9865x |
| large | prefix | 18005.641 us | 18718.202 us | 0.9610x | 0/15 | 0.9122–0.9826x |
| large | all | 18005.641 us | 18952.483 us | 0.9526x | 0/15 | 0.7066–0.9871x |
