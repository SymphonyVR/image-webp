# VP8L code-length arena current-final matrix

- baseline: `c52de05b9c902a6743941b998c96d5e4d3ba3609`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | arena | **0.9955x** | 3/17 | 0.9861–1.0075x |
| corpus | arena-fixed | **0.9858x** | 0/17 | 0.9804–0.9981x |
| large | arena | **1.0022x** | 11/17 | 0.9792–1.0291x |
| large | arena-fixed | **0.9315x** | 0/17 | 0.9120–0.9526x |
