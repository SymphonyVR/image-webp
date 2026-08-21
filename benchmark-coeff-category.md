# VP8 coefficient category benchmark

- branch baseline: `a3f8573acf4ab3da2d8c4c8b6faf49cfc5c24cac`
- ephemeral exact-category candidate: `e6d3db102477edb44de5bf85eddf9363ce697df3`
- CPU: `AMD EPYC 7763 64-Core Processor`
- architecture / vCPUs: `x86_64` / `4`
- candidate source is intentionally not retained on the branch pending benchmark review
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 11 alternating A/B rounds; paired speedup is baseline/candidate for the same round

| Workload | baseline median | candidate median | ratio of medians | paired median | paired range |
|---|---:|---:|---:|---:|---:|
| random_lossless | 196.001 us | 190.583 us | 1.028x | 1.028x | 0.997–1.033x |
| issue119 | 336672.280 us | 344384.661 us | 0.978x | 0.978x | 0.964–1.000x |

## Raw samples

```tsv
workload	round	variant	us_per_decode
random_lossless	1	baseline	197.150
issue119	1	baseline	337528.843
random_lossless	1	candidate	191.472
issue119	1	candidate	343404.666
random_lossless	2	candidate	190.917
issue119	2	candidate	344038.427
random_lossless	2	baseline	196.333
issue119	2	baseline	338189.480
random_lossless	3	baseline	196.043
issue119	3	baseline	338243.638
random_lossless	3	candidate	190.708
issue119	3	candidate	350967.010
random_lossless	4	candidate	190.378
issue119	4	candidate	348150.075
random_lossless	4	baseline	196.645
issue119	4	baseline	335846.204
random_lossless	5	baseline	191.708
issue119	5	baseline	336338.483
random_lossless	5	candidate	190.428
issue119	5	candidate	343865.906
random_lossless	6	candidate	190.940
issue119	6	candidate	342295.605
random_lossless	6	baseline	191.763
issue119	6	baseline	336672.280
random_lossless	7	baseline	190.437
issue119	7	baseline	336593.744
random_lossless	7	candidate	191.089
issue119	7	candidate	344384.661
random_lossless	8	candidate	190.531
issue119	8	candidate	344267.788
random_lossless	8	baseline	191.585
issue119	8	baseline	339958.559
random_lossless	9	baseline	190.973
issue119	9	baseline	346824.356
random_lossless	9	candidate	190.583
issue119	9	candidate	346653.352
random_lossless	10	candidate	190.216
issue119	10	candidate	345877.809
random_lossless	10	baseline	196.326
issue119	10	baseline	335492.368
random_lossless	11	baseline	196.001
issue119	11	baseline	335366.391
random_lossless	11	candidate	190.344
issue119	11	candidate	346079.206
```
