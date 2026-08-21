# VP8 coefficient complexity benchmark

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- branch baseline: `6c0bcee37cbd5bd6e6d72e37aaf922dc33318d75`
- ephemeral coefficient candidate: `eb20b8e551c9d4e48718561febb91382d2aeb28c`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- architecture / vCPUs: `x86_64` / `4`
- candidate source is intentionally not retained on the branch pending benchmark review
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 9 rotating-order rounds; paired speedup is median baseline/candidate ratio per round

| Workload | main median | baseline median | candidate median | ratio of medians | paired speedup |
|---|---:|---:|---:|---:|---:|
| random_lossless | 218.007 us | 206.859 us | 208.887 us | 0.990x | 0.989x |
| issue119 | 414839.949 us | 355997.300 us | 357528.460 us | 0.996x | 0.995x |

## Raw samples

```tsv
workload	round	variant	us_per_decode
random_lossless	1	main	218.007
issue119	1	main	414855.676
random_lossless	1	baseline	206.506
issue119	1	baseline	360165.285
random_lossless	1	candidate	208.268
issue119	1	candidate	358015.433
random_lossless	2	baseline	206.859
issue119	2	baseline	356055.942
random_lossless	2	candidate	210.277
issue119	2	candidate	359512.931
random_lossless	2	main	218.366
issue119	2	main	418974.321
random_lossless	3	candidate	208.449
issue119	3	candidate	356937.275
random_lossless	3	main	217.854
issue119	3	main	418567.588
random_lossless	3	baseline	207.471
issue119	3	baseline	355135.408
random_lossless	4	main	217.683
issue119	4	main	413385.269
random_lossless	4	baseline	206.989
issue119	4	baseline	355271.796
random_lossless	4	candidate	208.246
issue119	4	candidate	356935.790
random_lossless	5	baseline	206.574
issue119	5	baseline	355491.364
random_lossless	5	candidate	208.887
issue119	5	candidate	357270.821
random_lossless	5	main	217.485
issue119	5	main	412421.338
random_lossless	6	candidate	208.921
issue119	6	candidate	356775.081
random_lossless	6	main	220.667
issue119	6	main	413638.420
random_lossless	6	baseline	206.520
issue119	6	baseline	356494.697
random_lossless	7	main	218.235
issue119	7	main	414839.949
random_lossless	7	baseline	207.031
issue119	7	baseline	356350.383
random_lossless	7	candidate	210.394
issue119	7	candidate	357528.460
random_lossless	8	baseline	207.495
issue119	8	baseline	355503.396
random_lossless	8	candidate	210.572
issue119	8	candidate	358143.102
random_lossless	8	main	218.008
issue119	8	main	415247.058
random_lossless	9	candidate	208.286
issue119	9	candidate	357608.799
random_lossless	9	main	217.161
issue119	9	main	413791.854
random_lossless	9	baseline	206.001
issue119	9	baseline	355997.300
```
