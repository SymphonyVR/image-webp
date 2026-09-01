# VP8L meta-Huffman run coalescing

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 7763 64-Core Processor`
- horizontal identical entropy groups are coalesced; 15 alternating paired rounds
- hashes + tests/docs/Clippy/fmt/MSRV passed

| workload | baseline | candidate | paired median | positive | range |
|---|---:|---:|---:|---:|---:|
| corpus | 1067.975 us | 1080.155 us | 0.9880x | 1/15 | 0.9831–1.0057x |
| multi | 1767.773 us | 1785.313 us | 0.9895x | 0/15 | 0.9830–0.9990x |
| structured | 7652.951 us | 7957.203 us | 0.9587x | 0/15 | 0.9522–0.9734x |
| tiles | 8488.683 us | 8762.372 us | 0.9677x | 0/15 | 0.9584–0.9764x |
| noise | 42667.341 us | 42498.211 us | 1.0053x | 13/15 | 0.9381–1.0230x |
