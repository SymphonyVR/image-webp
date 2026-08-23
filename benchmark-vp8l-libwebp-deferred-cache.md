# VP8L deferred color-cache benchmark

- CPU: `AMD EPYC 9V74 80-Core Processor`
- direct safe-Rust port of libwebp last_cached strategy
- full output hashes match; stable/MSRV verification passed

| workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| corpus | 1235.679 us | 1266.508 us | 0.9756x | 0.9606–0.9795x |
| large | 23436.668 us | 24981.345 us | 0.9386x | 0.8997–1.2368x |
