# Safe lossless color-transform SLP benchmark

- branch baseline: `1a0d0ff547834d984df10049955218eabf9ddd02`
- ephemeral candidate: `df0a985f38df8c4ee4ebef2ef17204d94ed6c7ce`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- architecture / vCPUs: `x86_64` / `4`
- static VP8L fixtures: `10`
- candidate remains 100% safe Rust, preserves existing transform arithmetic, and builds on MSRV 1.80.1
- corpus uses normal release target (no `target-cpu=native`)

| Workload | baseline median | candidate median | ratio of medians | paired median | paired range |
|---|---:|---:|---:|---:|---:|
| VP8L default-target corpus (us/decode) | 1142.000 | 1136.222 | 1.005x | 1.005x | 0.995–1.021x |
| color_transform microbench (ns/iter) | 86164.770 | 84971.910 | 1.014x | 1.015x | 1.011–1.036x |

## Corpus raw samples

```tsv
workload	round	variant	value
vp8l_default	1	baseline	1155.451
vp8l_default	1	candidate	1131.771
vp8l_default	2	candidate	1137.365
vp8l_default	2	baseline	1143.003
vp8l_default	3	baseline	1141.211
vp8l_default	3	candidate	1140.882
vp8l_default	4	candidate	1134.563
vp8l_default	4	baseline	1154.753
vp8l_default	5	baseline	1149.473
vp8l_default	5	candidate	1136.222
vp8l_default	6	candidate	1138.999
vp8l_default	6	baseline	1143.708
vp8l_default	7	baseline	1138.259
vp8l_default	7	candidate	1143.919
vp8l_default	8	candidate	1133.049
vp8l_default	8	baseline	1142.000
vp8l_default	9	baseline	1140.123
vp8l_default	9	candidate	1133.979
vp8l_default	10	candidate	1135.446
vp8l_default	10	baseline	1139.028
vp8l_default	11	baseline	1141.254
vp8l_default	11	candidate	1145.195
```

## Microbenchmark raw samples

```tsv
workload	round	variant	value
color_transform_ns	1	baseline	86877.50
color_transform_ns	1	candidate	83895.38
color_transform_ns	2	candidate	84788.30
color_transform_ns	2	baseline	86164.77
color_transform_ns	3	baseline	85997.63
color_transform_ns	3	candidate	84753.04
color_transform_ns	4	candidate	84999.98
color_transform_ns	4	baseline	86400.59
color_transform_ns	5	baseline	86202.33
color_transform_ns	5	candidate	85006.31
color_transform_ns	6	candidate	84971.91
color_transform_ns	6	baseline	85970.38
color_transform_ns	7	baseline	85969.17
color_transform_ns	7	candidate	85060.21
```
