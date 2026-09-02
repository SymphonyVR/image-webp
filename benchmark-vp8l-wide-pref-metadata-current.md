# VP8L wide-root preference metadata benchmark

- baseline: `84d8d20753fce0a9972e8a244fdf929b5a55671c`
- CPU: `AMD EPYC 7763 64-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed
- avoids rescanning implicit code lengths solely to select 9/11-bit root width

| workload | paired median | positive | range |
|---|---:|---:|---:|
| corpus | **0.9917x** | 0/17 | 0.9712–0.9995x |
| large | **0.9426x** | 0/17 | 0.9057–0.9605x |
