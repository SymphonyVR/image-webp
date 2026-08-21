# Safe subtract-green confirmation

- branch baseline: `35d1f5bba9c6c56e3179ef367d30684d59348864`
- ephemeral candidate: `bf7a2bfc31aeb4a41f38fa003710878c34ac54c6`
- CPU: `AMD EPYC 7763 64-Core Processor`
- architecture / vCPUs: `x86_64` / `4`
- static VP8L fixtures: `10`
- candidate remains 100% safe Rust and builds on MSRV 1.80.1
- corpus confirmation uses normal release target (no `target-cpu=native`)

| Workload | baseline median | candidate median | ratio of medians | paired median | paired range |
|---|---:|---:|---:|---:|---:|
| VP8L default-target corpus (us/decode) | 1211.588 | 1223.926 | 0.990x | 0.991x | 0.987–1.022x |
| subtract_green microbench (ns/iter) | 451.500 | 441.770 | 1.022x | 1.022x | 1.017–1.023x |

## Corpus raw samples

```tsv
workload	round	variant	value
vp8l_default	1	baseline	1252.033
vp8l_default	1	candidate	1225.650
vp8l_default	2	candidate	1224.452
vp8l_default	2	baseline	1209.415
vp8l_default	3	baseline	1209.757
vp8l_default	3	candidate	1226.289
vp8l_default	4	candidate	1224.836
vp8l_default	4	baseline	1210.442
vp8l_default	5	baseline	1218.694
vp8l_default	5	candidate	1221.128
vp8l_default	6	candidate	1222.115
vp8l_default	6	baseline	1211.642
vp8l_default	7	baseline	1210.984
vp8l_default	7	candidate	1218.782
vp8l_default	8	candidate	1226.728
vp8l_default	8	baseline	1213.354
vp8l_default	9	baseline	1212.203
vp8l_default	9	candidate	1223.926
vp8l_default	10	candidate	1220.993
vp8l_default	10	baseline	1211.588
vp8l_default	11	baseline	1210.463
vp8l_default	11	candidate	1219.161
```

## Microbenchmark raw samples

```tsv
workload	round	variant	value
subtract_green_ns	1	baseline	451.77
subtract_green_ns	1	candidate	441.62
subtract_green_ns	2	candidate	441.77
subtract_green_ns	2	baseline	451.58
subtract_green_ns	3	baseline	451.17
subtract_green_ns	3	candidate	443.83
subtract_green_ns	4	candidate	441.96
subtract_green_ns	4	baseline	451.12
subtract_green_ns	5	baseline	451.50
subtract_green_ns	5	candidate	441.43
subtract_green_ns	6	candidate	442.02
subtract_green_ns	6	baseline	451.77
subtract_green_ns	7	baseline	450.91
subtract_green_ns	7	candidate	441.38
```
