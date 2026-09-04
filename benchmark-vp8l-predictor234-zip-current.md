# VP8L predictor 2/3/4 disjoint-zip current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- disjoint previous-row slices expose alias-free byte loops; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | p2 | **1.0145x** | 15/17 | 0.9895–1.0437x |
| corpus | p3 | **1.0138x** | 16/17 | 0.9877–1.0422x |
| corpus | p4 | **1.0186x** | 17/17 | 1.0104–1.0487x |
| corpus | all | **1.0346x** | 17/17 | 1.0216–1.0628x |
| large | p2 | **1.0080x** | 14/17 | 0.9710–1.0339x |
| large | p3 | **1.0067x** | 13/17 | 0.9679–1.0200x |
| large | p4 | **1.0695x** | 17/17 | 1.0167–1.0828x |
| large | all | **1.0063x** | 14/17 | 0.9700–1.0323x |
