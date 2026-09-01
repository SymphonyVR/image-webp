# VP8L Huffman allocation current-final matrix

- baseline: `6f8f7d994e2f747d46621812e01c27a29ff4be4a`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | fixedgroup | **1.0140x** | 16/17 | 0.9961–1.0253x |
| corpus | stack19 | **1.0123x** | 16/17 | 0.9871–1.0281x |
| corpus | sort512 | **1.0008x** | 9/17 | 0.9949–1.0201x |
| corpus | all | **1.0070x** | 15/17 | 0.9892–1.0228x |
| large | fixedgroup | **1.0651x** | 17/17 | 1.0357–1.0844x |
| large | stack19 | **1.0614x** | 17/17 | 1.0341–1.0896x |
| large | sort512 | **0.9998x** | 7/17 | 0.9664–1.0405x |
| large | all | **1.0004x** | 9/17 | 0.9828–1.0169x |
