# Reconstructed alpha-plane benchmark

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- pre-change performance baseline: `362dc4f475a69c258eee78c7e882d0b4b2f8adb0`
- direct alpha-plane write: `0c567b2b17e99b7ce967736922dbf6b15abb9720`
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 7 rotating-order rounds; values are microseconds per full decode

| Workload | main median | baseline median | alpha median | branch vs main | alpha vs baseline |
|---|---:|---:|---:|---:|---:|
| random_lossless | 217.620 us | 208.187 us | 208.540 us | 1.044x | 0.998x |
| issue119 | 415178.747 us | 407781.119 us | 361580.367 us | 1.148x | 1.128x |

## Raw samples

```tsv
workload	round	variant	us_per_decode
random_lossless	1	main	217.724
issue119	1	main	414312.551
random_lossless	1	baseline	208.187
issue119	1	baseline	407715.491
random_lossless	1	alpha	208.602
issue119	1	alpha	361070.893
random_lossless	2	baseline	208.811
issue119	2	baseline	422090.938
random_lossless	2	alpha	208.059
issue119	2	alpha	361700.552
random_lossless	2	main	217.620
issue119	2	main	418142.818
random_lossless	3	alpha	208.227
issue119	3	alpha	359796.586
random_lossless	3	main	217.374
issue119	3	main	414718.480
random_lossless	3	baseline	207.859
issue119	3	baseline	407109.106
random_lossless	4	main	228.829
issue119	4	main	415178.747
random_lossless	4	baseline	207.772
issue119	4	baseline	407781.119
random_lossless	4	alpha	209.318
issue119	4	alpha	359021.969
random_lossless	5	baseline	210.857
issue119	5	baseline	408933.260
random_lossless	5	alpha	208.540
issue119	5	alpha	369695.311
random_lossless	5	main	218.174
issue119	5	main	415284.053
random_lossless	6	alpha	209.113
issue119	6	alpha	361580.367
random_lossless	6	main	217.173
issue119	6	main	415812.577
random_lossless	6	baseline	208.300
issue119	6	baseline	409465.685
random_lossless	7	main	217.269
issue119	7	main	413907.766
random_lossless	7	baseline	208.092
issue119	7	baseline	407432.594
random_lossless	7	alpha	207.878
issue119	7	alpha	362176.861
```
