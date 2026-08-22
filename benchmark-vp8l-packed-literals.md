# VP8L packed-literal benchmark

- baseline: `677794add99a6a68eeb3e183853480e2308ac4f8`
- candidate: `c2c8f9eb700b5ccfa44cbd507ebb7fdc8c08bfd4`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- static VP8L fixtures: `10`
- full decoded output hash matched for every fixture
- candidate passed tests, docs, Clippy, formatting, and Rust 1.80.1
- normal release target; 17 alternating paired rounds

| Workload | baseline | candidate | ratio of medians | paired median | range |
|---|---:|---:|---:|---:|---:|
| VP8L corpus | 1297.208 us | 1316.562 us | 0.9853x | 0.9861x | 0.9811–1.0076x |
