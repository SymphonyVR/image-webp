# VP8L packed Huffman v2

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- contiguous packed tables; hashes + tests/docs/Clippy/fmt/MSRV passed

| workload | baseline | candidate | paired median | positive | range |
|---|---:|---:|---:|---:|---:|
| corpus | 960.660 us | 964.830 us | 1.0020x | 7/13 | 0.9489–1.0255x |
| large | 9812.597 us | 10153.288 us | 0.9700x | 4/13 | 0.8990–1.1954x |
