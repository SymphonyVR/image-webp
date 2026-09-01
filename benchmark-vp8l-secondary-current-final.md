# VP8L secondary transforms current-final matrix

- baseline: `0881ec1a66f09e11b766c309cf6e651077775bd9`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- hashes + tests + release tests + docs + Clippy + fmt + MSRV passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | green | **1.0144x** | 11/13 | 0.9844–1.0206x |
| corpus | stack | **1.0003x** | 7/13 | 0.9954–1.0054x |
| corpus | green-stack | **1.0204x** | 12/13 | 0.9978–1.0260x |
| corpus | all | **1.0191x** | 13/13 | 1.0159–1.0256x |
| palette | green | **1.0175x** | 8/13 | 0.8800–1.1063x |
| palette | stack | **1.0181x** | 8/13 | 0.8803–1.1358x |
| palette | green-stack | **0.9897x** | 5/13 | 0.9233–1.1272x |
| palette | all | **0.9642x** | 2/13 | 0.8891–1.0855x |
| green | green | **1.1648x** | 13/13 | 1.1498–1.1739x |
| green | stack | **1.0029x** | 10/13 | 0.9940–1.0476x |
| green | green-stack | **1.2406x** | 13/13 | 1.2226–1.2980x |
| green | all | **1.2457x** | 13/13 | 1.2385–1.2587x |
