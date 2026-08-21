# Alpha blending scale-table benchmark

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- inline baseline: `a94cdcfb25019388271151e32fc5065f6d995143`
- scale-table candidate: `79536567cca0b513cb8476762ed3f4bd7dc71f9b`
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 7 rotating-order rounds; values are microseconds per full decode

| Workload | main median | baseline median | scale median | branch vs main | scale vs baseline |
|---|---:|---:|---:|---:|---:|
| random_lossless | 174.442 us | 159.304 us | 160.311 us | 1.088x | 0.994x |
| issue119 | 314684.632 us | 268449.994 us | 270343.728 us | 1.164x | 0.993x |

## Raw samples

```tsv
workload	round	variant	us_per_decode
random_lossless	1	main	174.641
issue119	1	main	315625.963
random_lossless	1	baseline	161.105
issue119	1	baseline	268791.419
random_lossless	1	scale	160.250
issue119	1	scale	269927.617
random_lossless	2	baseline	161.342
issue119	2	baseline	268449.994
random_lossless	2	scale	160.016
issue119	2	scale	270191.908
random_lossless	2	main	174.442
issue119	2	main	321141.339
random_lossless	3	scale	160.578
issue119	3	scale	270297.948
random_lossless	3	main	174.272
issue119	3	main	315333.152
random_lossless	3	baseline	159.267
issue119	3	baseline	268600.032
random_lossless	4	main	174.642
issue119	4	main	314532.308
random_lossless	4	baseline	159.084
issue119	4	baseline	267964.819
random_lossless	4	scale	160.391
issue119	4	scale	273155.019
random_lossless	5	baseline	158.632
issue119	5	baseline	268446.174
random_lossless	5	scale	160.311
issue119	5	scale	270343.728
random_lossless	5	main	174.194
issue119	5	main	314415.982
random_lossless	6	scale	160.301
issue119	6	scale	270715.736
random_lossless	6	main	174.674
issue119	6	main	314684.632
random_lossless	6	baseline	159.304
issue119	6	baseline	267186.452
random_lossless	7	main	174.236
issue119	7	main	313758.625
random_lossless	7	baseline	159.520
issue119	7	baseline	268854.356
random_lossless	7	scale	160.823
issue119	7	scale	279607.061
```
