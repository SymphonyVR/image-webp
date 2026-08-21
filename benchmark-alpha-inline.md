# Alpha blending inline benchmark

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- direct-alpha baseline: `f0dd1dcd1a1788668b3f12c13e4759d60679eaf4`
- inline candidate: `4e1c23791b9f84604d59741814f417946e261a51`
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 7 rotating-order rounds; values are microseconds per full decode

| Workload | main median | baseline median | inline median | branch vs main | inline vs baseline |
|---|---:|---:|---:|---:|---:|
| random_lossless | 217.509 us | 207.958 us | 207.619 us | 1.048x | 1.002x |
| issue119 | 412635.627 us | 359662.848 us | 356383.297 us | 1.158x | 1.009x |

## Raw samples

```tsv
workload	round	variant	us_per_decode
random_lossless	1	main	217.673
issue119	1	main	412143.228
random_lossless	1	baseline	208.476
issue119	1	baseline	359567.782
random_lossless	1	inline	208.254
issue119	1	inline	355016.475
random_lossless	2	baseline	212.974
issue119	2	baseline	358159.768
random_lossless	2	inline	208.538
issue119	2	inline	366110.746
random_lossless	2	main	216.866
issue119	2	main	412471.703
random_lossless	3	inline	206.849
issue119	3	inline	356652.670
random_lossless	3	main	229.260
issue119	3	main	416404.767
random_lossless	3	baseline	207.918
issue119	3	baseline	359730.727
random_lossless	4	main	217.205
issue119	4	main	414423.693
random_lossless	4	baseline	207.958
issue119	4	baseline	359662.848
random_lossless	4	inline	206.887
issue119	4	inline	354676.366
random_lossless	5	baseline	209.857
issue119	5	baseline	359704.514
random_lossless	5	inline	207.619
issue119	5	inline	358476.136
random_lossless	5	main	217.509
issue119	5	main	412745.693
random_lossless	6	inline	206.989
issue119	6	inline	356383.297
random_lossless	6	main	219.721
issue119	6	main	412635.627
random_lossless	6	baseline	207.732
issue119	6	baseline	359367.367
random_lossless	7	main	217.262
issue119	7	main	412292.778
random_lossless	7	baseline	207.679
issue119	7	baseline	359740.485
random_lossless	7	inline	208.942
issue119	7	inline	355173.235
```
