# Specialized VP8 DCT token benchmark v3

- baseline: `9861deb8931aeaa823d412d83c35f3ae199946ae`
- candidate: `ad4b14aeec58f8dce93422a52e535b263e6ee56c`
- CPU: `Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz`
- safe Rust; fixed DCT topology; normal release target

| Workload | baseline | candidate | ratio | paired median | range |
|---|---:|---:|---:|---:|---:|
| issue119 | 355931.184 us | 349228.854 us | 1.019x | 1.020x | 1.009–1.036x |
| issue136 | 36205.364 us | 35838.632 us | 1.010x | 1.010x | 1.007–1.012x |