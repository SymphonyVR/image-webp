# VP8L color/green fusion benchmark

- baseline: `677794add99a6a68eeb3e183853480e2308ac4f8`
- candidate: `ff59c573671529d32aaff9870b9072ced377ce8c`
- CPU: `Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz`
- static VP8L fixtures: `10`
- full decoded output hash matched for every fixture
- candidate passed tests, docs, Clippy, formatting, and Rust 1.80.1
- normal release target; 17 alternating paired rounds

| Workload | baseline | candidate | ratio of medians | paired median | range |
|---|---:|---:|---:|---:|---:|
| VP8L corpus | 1184.046 us | 1185.722 us | 0.9986x | 0.9973x | 0.9817–1.0081x |
