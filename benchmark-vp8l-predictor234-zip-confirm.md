# VP8L predictor 2/3/4 disjoint-zip long confirmation

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 7763 64-Core Processor`
- disjoint previous-row slices expose alias-free byte loops; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | p4 | **1.0039x** | 21/25 | 0.9563–1.0156x |
| corpus | all | **1.0192x** | 25/25 | 1.0117–1.0258x |
| large | p4 | **0.9919x** | 7/25 | 0.8645–1.0270x |
| large | all | **0.9415x** | 0/25 | 0.8671–0.9790x |
