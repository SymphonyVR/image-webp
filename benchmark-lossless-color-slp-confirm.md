# Safe color-transform SLP confirmation

- branch baseline: `6eab3381a15c5c0030b1b6c8aa3a79bf07d9519c`
- ephemeral candidate: `f9f2b9a8492545e4407f05dc7c6733c5b3338e31`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- architecture / vCPUs: `x86_64` / `4`
- static VP8L fixtures: `10`
- candidate remains 100% safe Rust and builds on MSRV 1.80.1
- normal release target; 13 alternating high-precision corpus rounds

| Workload | baseline median | candidate median | ratio | paired median | paired range |
|---|---:|---:|---:|---:|---:|
| VP8L corpus (us/decode) | 1300.009 | 1299.916 | 1.000x | 1.000x | 0.995–1.004x |
| color_transform (ns/iter) | 130401.360 | 129815.070 | 1.005x | 1.004x | 1.002–1.006x |

## Corpus raw samples

```tsv
workload	round	variant	value
vp8l_default	1	baseline	1308.219
vp8l_default	1	candidate	1303.903
vp8l_default	2	candidate	1299.916
vp8l_default	2	baseline	1300.009
vp8l_default	3	baseline	1299.298
vp8l_default	3	candidate	1305.987
vp8l_default	4	candidate	1299.290
vp8l_default	4	baseline	1303.065
vp8l_default	5	baseline	1305.843
vp8l_default	5	candidate	1300.095
vp8l_default	6	candidate	1302.620
vp8l_default	6	baseline	1301.147
vp8l_default	7	baseline	1298.229
vp8l_default	7	candidate	1298.242
vp8l_default	8	candidate	1300.177
vp8l_default	8	baseline	1299.449
vp8l_default	9	baseline	1299.097
vp8l_default	9	candidate	1299.262
vp8l_default	10	candidate	1298.258
vp8l_default	10	baseline	1300.176
vp8l_default	11	baseline	1299.118
vp8l_default	11	candidate	1299.270
vp8l_default	12	candidate	1300.121
vp8l_default	12	baseline	1299.761
vp8l_default	13	baseline	1300.758
vp8l_default	13	candidate	1299.896
```

## Microbenchmark raw samples

```tsv
workload	round	variant	value
color_transform_ns	1	baseline	130506.94
color_transform_ns	1	candidate	129706.17
color_transform_ns	2	candidate	129908.63
color_transform_ns	2	baseline	130174.38
color_transform_ns	3	baseline	130485.77
color_transform_ns	3	candidate	129798.82
color_transform_ns	4	candidate	129815.07
color_transform_ns	4	baseline	130122.81
color_transform_ns	5	baseline	130401.36
color_transform_ns	5	candidate	129823.80
```
