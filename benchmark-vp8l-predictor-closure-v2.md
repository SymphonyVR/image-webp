# VP8L predictor closure matrix

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 9V45 96-Core Processor`
- hashes + tests + MSRV passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | index | 0.9998x | 5/11 | 0.9901–1.0210x |
| corpus | fuse | 0.9917x | 2/11 | 0.9553–1.0168x |
| corpus | traverse | 0.9884x | 2/11 | 0.8764–1.0179x |
| corpus | direct | 1.0237x | 8/11 | 0.9297–1.0540x |
| corpus | avg | 1.0074x | 6/11 | 0.9632–1.0197x |
| corpus | packed | 1.0486x | 11/11 | 1.0085–1.0663x |
| corpus | p11 | 0.9823x | 3/11 | 0.9537–1.0085x |
| corpus | all | 1.0174x | 11/11 | 1.0048–1.0477x |
| large | index | 1.0066x | 7/11 | 0.9676–1.0582x |
| large | fuse | 1.0048x | 6/11 | 0.9713–1.0404x |
| large | traverse | 0.9928x | 3/11 | 0.8790–1.0313x |
| large | direct | 1.0103x | 6/11 | 0.9350–1.0472x |
| large | avg | 0.9994x | 4/11 | 0.9397–1.0334x |
| large | packed | 1.0040x | 8/11 | 0.9739–1.0561x |
| large | p11 | 0.9865x | 4/11 | 0.9526–1.0793x |
| large | all | 0.9928x | 3/11 | 0.9584–1.0201x |
