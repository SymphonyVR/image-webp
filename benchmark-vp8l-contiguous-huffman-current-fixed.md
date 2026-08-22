# Current VP8L contiguous-Huffman benchmark

- CPU: `AMD EPYC 9V74 80-Core Processor`
- fixed refs; hashes match; tests/Clippy/fmt pass

| workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| corpus | 1240.103 us | 1237.578 us | 1.0015x | 0.9759–1.0137x |
| large | 23170.220 us | 23198.806 us | 0.9988x | 0.9753–1.0037x |
