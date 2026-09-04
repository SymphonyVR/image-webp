# VP8L predictor1 word-lane current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- safe 32-bit independent byte-lane arithmetic; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | word | **0.9647x** | 0/17 | 0.9536–0.9687x |
| corpus | word4 | **0.9387x** | 0/17 | 0.9291–0.9411x |
| large | word | **0.8534x** | 0/17 | 0.8240–0.8773x |
| large | word4 | **0.7253x** | 0/17 | 0.7009–0.7606x |
