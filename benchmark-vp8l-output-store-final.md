# VP8L output-store matrix

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- hashes + tests + MSRV passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | literal | 0.9873x | 0/13 | 0.9802–0.9970x |
| corpus | fill | 1.0012x | 8/13 | 0.9901–1.0073x |
| corpus | both | 0.9951x | 2/13 | 0.9728–1.0029x |
| large | literal | 0.9660x | 0/13 | 0.9455–0.9895x |
| large | fill | 1.0119x | 12/13 | 0.9890–1.0186x |
| large | both | 1.0157x | 12/13 | 0.9805–1.0416x |
