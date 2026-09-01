# VP8L scratchless palette current-final benchmark

- baseline: `6f8f7d994e2f747d46621812e01c27a29ff4be4a`
- CPU: `Intel(R) Xeon(R) 6973P-C`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed

| workload | paired median | positive | range |
|---|---:|---:|---:|
| corpus | **0.9962x** | 5/17 | 0.8986–1.0246x |
| palette | **0.9449x** | 1/17 | 0.9231–1.0168x |
