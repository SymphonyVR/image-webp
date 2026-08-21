# Controlled decode benchmark

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- performance-optimizations baseline: `362dc4f475a69c258eee78c7e882d0b4b2f8adb0`
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 7 alternating rounds; values are microseconds per full decode

| Workload | main median | optimized median | speedup | main range | optimized range |
|---|---:|---:|---:|---:|---:|
| random_lossless | 217.308 us | 208.201 us | 1.044x | 216.858–221.200 | 207.458–209.293 |
| issue119 | 414724.251 us | 408447.553 us | 1.015x | 413928.886–423627.159 | 406719.022–411222.746 |

## Raw samples

```tsv
workload	round	variant	us_per_decode
random_lossless	1	main	218.154
issue119	1	main	414320.672
random_lossless	1	opt	209.086
issue119	1	opt	406719.022
random_lossless	2	opt	209.252
issue119	2	opt	408447.553
random_lossless	2	main	216.936
issue119	2	main	413928.886
random_lossless	3	main	217.697
issue119	3	main	414724.251
random_lossless	3	opt	207.860
issue119	3	opt	407273.100
random_lossless	4	opt	208.201
issue119	4	opt	411222.746
random_lossless	4	main	217.303
issue119	4	main	423627.159
random_lossless	5	main	221.200
issue119	5	main	417778.636
random_lossless	5	opt	207.776
issue119	5	opt	410015.571
random_lossless	6	opt	209.293
issue119	6	opt	408666.268
random_lossless	6	main	217.308
issue119	6	main	415208.326
random_lossless	7	main	216.858
issue119	7	main	414212.717
random_lossless	7	opt	207.458
issue119	7	opt	408378.672
```
