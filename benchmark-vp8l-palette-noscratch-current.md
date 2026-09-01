# VP8L scratchless palette current-final benchmark

- baseline: `0881ec1a66f09e11b766c309cf6e651077775bd9`
- CPU: `Intel(R) Xeon(R) 6973P-C`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed

| workload | paired median | positive | range |
|---|---:|---:|---:|
| corpus | **1.0059x** | 16/17 | 0.9964–1.0082x |
| palette | **0.9474x** | 0/17 | 0.8930–0.9776x |
