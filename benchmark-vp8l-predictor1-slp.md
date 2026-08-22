# VP8L predictor-1 four-lane benchmark

- baseline: `0fdcb2f57d1d7dd272ee45d08e26fc80cb3f2aa8`
- candidate: `9506cad4ca7ff0f1f9280a3e473832b34ac9e30e`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- hashes match; tests/docs/Clippy/fmt/MSRV passed

| baseline | candidate | paired median | range |
|---:|---:|---:|---:|
| 1302.520 us | 1277.138 us | 1.0197x | 1.0031–1.0346x |
