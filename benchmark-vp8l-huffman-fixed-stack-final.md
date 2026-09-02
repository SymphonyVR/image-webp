# VP8L fixed-group + stack19 current-final confirmation

- baseline: `c52de05b9c902a6743941b998c96d5e4d3ba3609`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | fixedgroup | **1.0026x** | 20/25 | 0.9893–1.0145x |
| corpus | stack19 | **0.9996x** | 12/25 | 0.9953–1.0147x |
| corpus | both | **1.0048x** | 23/25 | 0.9848–1.0190x |
| large | fixedgroup | **1.0024x** | 18/25 | 0.9748–1.0350x |
| large | stack19 | **1.0017x** | 15/25 | 0.9705–1.0436x |
| large | both | **1.0056x** | 20/25 | 0.9761–1.0324x |
