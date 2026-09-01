# VP8L predictor traversal current-final matrix

- baseline: `0881ec1a66f09e11b766c309cf6e651077775bd9`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | fuse | **0.9863x** | 0/17 | 0.9548–0.9947x |
| corpus | both | **0.9833x** | 0/17 | 0.9745–0.9889x |
| large | fuse | **0.9458x** | 2/17 | 0.9297–1.1123x |
| large | both | **0.9382x** | 2/17 | 0.5907–1.0966x |
