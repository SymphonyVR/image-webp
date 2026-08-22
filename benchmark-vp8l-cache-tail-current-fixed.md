# Current VP8L cache-tail benchmark

- CPU: `AMD EPYC 7763 64-Core Processor`
- fixed refs; full hashes match; tests/docs/Clippy/fmt/MSRV pass

| workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| corpus | 1183.161 us | 1170.629 us | 1.0107x | 1.0056–1.0291x |
| large | 23273.771 us | 21664.354 us | 1.0735x | 1.0337–1.2122x |
