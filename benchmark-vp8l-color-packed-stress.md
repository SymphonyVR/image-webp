# Deep VP8L packed-color stress

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `Intel(R) Xeon(R) 6973P-C`
- 21 alternating paired rounds; exhaustive randomized width/height/size-bit property test + full hashes/tests/docs/Clippy/fmt/MSRV passed

| workload | color metadata | baseline | candidate | paired median | positive | range |
|---|---|---:|---:|---:|---:|---:|
| corpus | — | 875.464 us | 833.560 us | 1.0579x | 21/21 | 1.0293–1.1050x |
| large | none | 4385.650 us | 4120.879 us | 1.0747x | 20/21 | 0.9546–1.1576x |
| color | none | 5952.507 us | 5528.061 us | 1.0765x | 20/21 | 0.9945–1.1497x |
| rgcorr | none | 4609.458 us | 4213.095 us | 1.0789x | 21/21 | 1.0117–1.1359x |
| bgcorr | none | 7023.825 us | 6638.031 us | 1.0657x | 20/21 | 0.9777–1.0871x |
| gray | none | 4497.352 us | 4546.540 us | 0.9925x | 10/21 | 0.9301–1.0138x |
| tiles | none | 1050.643 us | 1032.320 us | 1.0020x | 11/21 | 0.9232–1.0823x |
| chaos | none | 22450.547 us | 21826.874 us | 1.0234x | 20/21 | 0.9953–1.0569x |
