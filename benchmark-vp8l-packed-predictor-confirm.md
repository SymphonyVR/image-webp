# Strict VP8L packed-predictor confirmation

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- 25 alternating paired rounds; hashes + tests + MSRV passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | packed | 1.0291x | 25/25 | 1.0147–1.0407x |
| large | packed | 0.9906x | 6/25 | 0.9551–1.0190x |
