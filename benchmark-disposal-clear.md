# Disposal row-clear benchmark

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- branch baseline: `c26b2a9a02287554ea1d74f0b507ab90ec39d106`
- ephemeral row-clear candidate: `e5f6a6a2ea3febcfff0594c081d7e24e56c5221c`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- architecture / vCPUs: `x86_64` / `4`
- candidate source is intentionally not retained on the branch pending benchmark review
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 7 rotating-order rounds; values are microseconds per full decode

| Workload | main median | baseline median | candidate median | branch vs main | candidate vs baseline |
|---|---:|---:|---:|---:|---:|
| random_lossless | 172.633 us | 164.624 us | 161.864 us | 1.067x | 1.017x |
| issue119 | 352547.716 us | 309990.192 us | 312082.680 us | 1.130x | 0.993x |

## Raw samples

```tsv
workload	round	variant	us_per_decode
random_lossless	1	main	168.245
issue119	1	main	352547.716
random_lossless	1	baseline	164.624
issue119	1	baseline	313457.906
random_lossless	1	candidate	170.612
issue119	1	candidate	321441.963
random_lossless	2	baseline	158.117
issue119	2	baseline	312012.543
random_lossless	2	candidate	160.568
issue119	2	candidate	309246.262
random_lossless	2	main	179.110
issue119	2	main	357357.596
random_lossless	3	candidate	166.991
issue119	3	candidate	312082.680
random_lossless	3	main	168.873
issue119	3	main	346977.932
random_lossless	3	baseline	171.346
issue119	3	baseline	309990.192
random_lossless	4	main	175.511
issue119	4	main	350230.513
random_lossless	4	baseline	168.672
issue119	4	baseline	308382.768
random_lossless	4	candidate	160.803
issue119	4	candidate	306907.026
random_lossless	5	baseline	159.526
issue119	5	baseline	305427.307
random_lossless	5	candidate	160.280
issue119	5	candidate	310782.015
random_lossless	5	main	172.471
issue119	5	main	348437.167
random_lossless	6	candidate	161.864
issue119	6	candidate	314497.647
random_lossless	6	main	174.858
issue119	6	main	361438.365
random_lossless	6	baseline	172.267
issue119	6	baseline	307333.467
random_lossless	7	main	172.633
issue119	7	main	356518.513
random_lossless	7	baseline	160.261
issue119	7	baseline	336593.791
random_lossless	7	candidate	177.803
issue119	7	candidate	334208.372
```
