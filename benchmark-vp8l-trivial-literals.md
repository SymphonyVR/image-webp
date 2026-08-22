# VP8L trivial-literal benchmark

- baseline: `41490df368bb675e1f50922329b390968d352f10`
- candidate: `75322420c001281928a4739ec8c5fc3698766e8c`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- static VP8L fixtures: `10`
- full decoded output hash matched for every fixture
- candidate passed tests, docs, Clippy, formatting, and Rust 1.80.1
- normal release target; 17 alternating paired rounds

| Workload | baseline | candidate | ratio of medians | paired median | range |
|---|---:|---:|---:|---:|---:|
| VP8L corpus | 1293.092 us | 1335.762 us | 0.9681x | 0.9681x | 0.9622–0.9729x |
