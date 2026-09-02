# VP8L paired green-color multiply current-tree matrix

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- independently packs green→red and green→blue coefficient products into one u32 multiply; pair_byte also uses byte-domain red→blue delta; hashes + full verification passed

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | pair | **0.9914x** | 0/17 | 0.9479–0.9953x |
| corpus | pair_byte | **0.9908x** | 0/17 | 0.9779–0.9983x |
| colorhot | pair | **0.9971x** | 3/17 | 0.9090–1.0108x |
| colorhot | pair_byte | **0.9976x** | 6/17 | 0.9918–1.0115x |
