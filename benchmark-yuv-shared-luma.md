# Shared-luma YUV benchmark

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- branch baseline: `ae6f81d45a040c02cdbb12b7c90b6ae3a854633a`
- ephemeral shared-luma candidate: `bb5f1acf33bbc00177d8e35b8fdee907d6f1bac7`
- CPU: `AMD EPYC 7763 64-Core Processor`
- architecture / vCPUs: `x86_64` / `4`
- candidate source is intentionally not retained on the branch pending benchmark review
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 7 rotating-order rounds; paired speedup is the median baseline/candidate ratio per round

| Workload | main median | baseline median | candidate median | candidate vs baseline | paired speedup |
|---|---:|---:|---:|---:|---:|
| random_lossless | 205.269 us | 192.044 us | 196.409 us | 0.978x | 0.982x |
| issue119 | 403706.184 us | 341956.665 us | 341921.435 us | 1.000x | 1.001x |

## Raw samples

```tsv
workload	round	variant	us_per_decode
random_lossless	1	main	203.865
issue119	1	main	402438.142
random_lossless	1	baseline	196.789
issue119	1	baseline	340388.859
random_lossless	1	candidate	196.635
issue119	1	candidate	340406.422
random_lossless	2	baseline	197.144
issue119	2	baseline	350760.884
random_lossless	2	candidate	192.086
issue119	2	candidate	342515.245
random_lossless	2	main	204.845
issue119	2	main	404948.321
random_lossless	3	candidate	196.953
issue119	3	candidate	341464.729
random_lossless	3	main	204.238
issue119	3	main	405375.151
random_lossless	3	baseline	192.044
issue119	3	baseline	342124.766
random_lossless	4	main	206.365
issue119	4	main	403482.798
random_lossless	4	baseline	190.781
issue119	4	baseline	347343.299
random_lossless	4	candidate	194.270
issue119	4	candidate	341921.435
random_lossless	5	baseline	198.774
issue119	5	baseline	341956.665
random_lossless	5	candidate	195.730
issue119	5	candidate	341636.304
random_lossless	5	main	205.269
issue119	5	main	404614.982
random_lossless	6	candidate	197.871
issue119	6	candidate	345009.040
random_lossless	6	main	206.409
issue119	6	main	400615.824
random_lossless	6	baseline	190.893
issue119	6	baseline	341547.062
random_lossless	7	main	206.479
issue119	7	main	403706.184
random_lossless	7	baseline	191.204
issue119	7	baseline	341917.263
random_lossless	7	candidate	196.409
issue119	7	candidate	342405.724
```
