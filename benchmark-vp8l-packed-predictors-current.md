# Packed VP8L predictors current-final matrix

- baseline: `c52de05b9c902a6743941b998c96d5e4d3ba3609`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | direct | **1.0158x** | 17/17 | 1.0105–1.0276x |
| corpus | avg | **1.0002x** | 9/17 | 0.9783–1.0066x |
| corpus | both | **1.0205x** | 17/17 | 1.0108–1.0339x |
| large | direct | **0.9418x** | 0/17 | 0.9124–0.9839x |
| large | avg | **0.9975x** | 7/17 | 0.9573–1.0311x |
| large | both | **0.9905x** | 5/17 | 0.9636–1.0274x |
