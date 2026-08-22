# VP8L backreference cache-tail benchmark

- baseline: `fc8b701a3cba33887e47768c7b1e5e6a44de239d`
- candidate: `03b72610f1437479a5f88b6f8b7de2bbc39fe91a`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- full hashes match; tests/docs/Clippy/fmt/MSRV passed

| workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| corpus | 1269.585 us | 1260.034 us | 1.0067x | 0.9880–1.0302x |
| large | 27006.193 us | 24936.431 us | 1.0847x | 1.0751–1.0935x |
