# Opaque destination alpha-blend benchmark

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- inline baseline: `9e43c7d255506ed2889b50d754b0069dda7c0ff0`
- opaque-destination candidate: `ac425953c368c05ea9a53a052ae7fdbe8896e44c`
- CPU: `AMD EPYC 7763 64-Core Processor`
- architecture / vCPUs: `x86_64` / `4`
- reported CPU MHz range: ``–``
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 7 rotating-order rounds; values are microseconds per full decode

| Workload | main median | baseline median | opaque median | branch vs main | opaque vs baseline |
|---|---:|---:|---:|---:|---:|
| random_lossless | 205.091 us | 193.060 us | 194.995 us | 1.052x | 0.990x |
| issue119 | 396447.826 us | 338825.187 us | 339557.308 us | 1.168x | 0.998x |

## Raw samples

```tsv
workload	round	variant	us_per_decode
random_lossless	1	main	205.405
issue119	1	main	394711.864
random_lossless	1	baseline	196.601
issue119	1	baseline	338421.479
random_lossless	1	opaque	195.589
issue119	1	opaque	341447.499
random_lossless	2	baseline	190.682
issue119	2	baseline	339628.244
random_lossless	2	opaque	195.213
issue119	2	opaque	340406.678
random_lossless	2	main	204.024
issue119	2	main	396447.826
random_lossless	3	opaque	199.824
issue119	3	opaque	339557.308
random_lossless	3	main	205.091
issue119	3	main	397968.662
random_lossless	3	baseline	191.707
issue119	3	baseline	341912.754
random_lossless	4	main	206.175
issue119	4	main	400550.326
random_lossless	4	baseline	196.454
issue119	4	baseline	338825.187
random_lossless	4	opaque	194.995
issue119	4	opaque	340002.293
random_lossless	5	baseline	193.060
issue119	5	baseline	338160.144
random_lossless	5	opaque	193.570
issue119	5	opaque	337670.713
random_lossless	5	main	206.429
issue119	5	main	396060.340
random_lossless	6	opaque	190.916
issue119	6	opaque	338849.111
random_lossless	6	main	203.877
issue119	6	main	398858.219
random_lossless	6	baseline	196.502
issue119	6	baseline	341365.397
random_lossless	7	main	204.618
issue119	7	main	394817.714
random_lossless	7	baseline	191.675
issue119	7	baseline	338248.895
random_lossless	7	opaque	191.643
issue119	7	opaque	337236.544
```
