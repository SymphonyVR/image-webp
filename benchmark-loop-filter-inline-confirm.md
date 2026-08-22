# Horizontal loop-filter inline confirmation

- baseline: `13448c6a17180ee9939154b052dd70b44cd1729c`
- candidate: `523bfb1778b7338c2b6a468cf8f4a8ba3441bf31`
- CPU: `Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz`

| Workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| issue119 | 328427.691 us | 327420.357 us | 1.0007x | 0.9879–1.0160x |
| issue136 | 33343.446 us | 33202.979 us | 1.0044x | 0.9979–1.0071x |
