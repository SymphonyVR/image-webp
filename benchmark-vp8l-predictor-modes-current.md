# Individual packed VP8L predictor modes current-final matrix

- baseline: `c52de05b9c902a6743941b998c96d5e4d3ba3609`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | p3 | **1.0114x** | 13/13 | 1.0070–1.0272x |
| corpus | p4 | **1.0069x** | 12/13 | 0.9908–1.0220x |
| corpus | p5 | **0.9989x** | 6/13 | 0.9940–1.0113x |
| corpus | p6 | **1.0006x** | 7/13 | 0.9685–1.0140x |
| corpus | p7 | **0.9889x** | 1/13 | 0.9643–1.0024x |
| corpus | p8 | **1.0030x** | 10/13 | 0.9617–1.0107x |
| corpus | p9 | **0.9939x** | 2/13 | 0.9899–1.0038x |
| corpus | p10 | **0.9870x** | 0/13 | 0.9744–0.9997x |
| large | p3 | **0.9981x** | 6/13 | 0.9688–1.0045x |
| large | p4 | **0.9792x** | 0/13 | 0.9569–0.9958x |
| large | p5 | **0.9973x** | 6/13 | 0.9657–1.0233x |
| large | p6 | **0.9993x** | 5/13 | 0.9679–1.0150x |
| large | p7 | **0.9454x** | 0/13 | 0.9198–0.9689x |
| large | p8 | **0.9958x** | 3/13 | 0.9584–1.0257x |
| large | p9 | **0.9346x** | 0/13 | 0.9071–0.9722x |
| large | p10 | **0.9409x** | 0/13 | 0.9023–0.9659x |
