# VP8L correct staged-row matrix

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 7763 64-Core Processor`
- reusable predictor-stage row buffers; palette/indexed streams fall back to full passes
- hashes + tests + MSRV passed

| workload | batch | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | 8 | 0.9650x | 0/11 | 0.9518–0.9925x |
| corpus | 16 | 0.9681x | 0/11 | 0.9550–0.9818x |
| corpus | 32 | 0.9703x | 0/11 | 0.9634–0.9944x |
| corpus | 64 | 0.9707x | 0/11 | 0.9601–0.9962x |
| large | 8 | 0.8970x | 0/11 | 0.8643–0.9038x |
| large | 16 | 0.9011x | 0/11 | 0.8776–0.9173x |
| large | 32 | 0.8962x | 0/11 | 0.8790–0.9141x |
| large | 64 | 0.9032x | 0/11 | 0.8651–0.9191x |
