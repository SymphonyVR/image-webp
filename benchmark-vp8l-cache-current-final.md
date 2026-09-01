# VP8L cache representation current-final matrix

- baseline: `0881ec1a66f09e11b766c309cf6e651077775bd9`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | hash | **1.0174x** | 16/17 | 0.9978–1.0217x |
| corpus | packed | **0.9928x** | 0/17 | 0.9861–0.9956x |
| corpus | both | **0.9776x** | 0/17 | 0.9692–0.9819x |
| large | hash | **1.1009x** | 17/17 | 1.0555–1.1525x |
| large | packed | **0.9911x** | 5/17 | 0.9541–1.0314x |
| large | both | **0.8826x** | 0/17 | 0.8532–0.9215x |
