# VP8L Huffman scratch closure v2

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- hashes + tests + MSRV passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | reuse | 1.0001x | 6/11 | 0.9701–1.0079x |
| corpus | reuse_sorted | 1.0057x | 10/11 | 0.9915–1.0134x |
| corpus | all | 0.9984x | 1/11 | 0.9917–1.0006x |
| large | reuse | 1.0061x | 7/11 | 0.8497–1.0587x |
| large | reuse_sorted | 0.9975x | 4/11 | 0.9652–1.0447x |
| large | all | 0.9529x | 1/11 | 0.9465–1.0311x |
