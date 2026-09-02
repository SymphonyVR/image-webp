# VP8L predictor-11 current-tree confirmation

- baseline: `c52de05b9c902a6743941b998c96d5e4d3ba3609`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed
- algebra simplification only

| workload | paired median | positive | range |
|---|---:|---:|---:|
| corpus | **1.0016x** | 15/25 | 0.9626–1.0338x |
| large | **1.0080x** | 16/25 | 0.9715–1.0859x |
