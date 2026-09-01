# VP8L packed subtract-green current-final confirmation

- baseline: `6f8f7d994e2f747d46621812e01c27a29ff4be4a`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV debug/release passed
- 25 alternating paired rounds

| workload | paired median | positive | range |
|---|---:|---:|---:|
| corpus | **1.0327x** | 25/25 | 1.0167–1.0491x |
| green | **1.3199x** | 25/25 | 1.3087–1.3386x |
| large | **1.0659x** | 25/25 | 1.0368–1.0975x |
