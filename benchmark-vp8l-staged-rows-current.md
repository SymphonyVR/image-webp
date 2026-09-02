# VP8L staged-row current-tree matrix

- baseline: `84d8d20753fce0a9972e8a244fdf929b5a55671c`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- non-palette images only; predictor-stage boundary row preserved; full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | r8 | **0.9749x** | 0/13 | 0.8608–0.9825x |
| corpus | r16 | **0.9764x** | 0/13 | 0.9069–0.9874x |
| corpus | r32 | **0.9786x** | 0/13 | 0.9648–0.9892x |
| large | r8 | **0.8955x** | 0/13 | 0.8824–0.9364x |
| large | r16 | **0.9016x** | 0/13 | 0.8864–0.9093x |
| large | r32 | **0.9048x** | 0/13 | 0.8886–0.9362x |
