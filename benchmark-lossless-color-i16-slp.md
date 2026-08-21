# Safe i16 color-transform SLP benchmark

- branch baseline: `bf617551f41bf911b4434ce8b8939b596e8244ff`
- ephemeral candidate: `1e23e31a36058ae736836db1e1e442a032389224`
- CPU: `AMD EPYC 7763 64-Core Processor`
- architecture / vCPUs: `x86_64` / `4`
- static VP8L fixtures: `10`
- 100% safe Rust; MSRV 1.80.1; normal release target

| Workload | baseline median | candidate median | ratio | paired median | paired range |
|---|---:|---:|---:|---:|---:|
| VP8L corpus (us/decode) | 1222.120 | 1218.447 | 1.003x | 1.001x | 0.991–1.008x |
| color_transform (ns/iter) | 123941.940 | 124542.080 | 0.995x | 0.995x | 0.985–0.998x |

## Corpus raw

```tsv
workload	round	variant	value
vp8l	1	baseline	1223.415
vp8l	1	candidate	1219.090
vp8l	2	candidate	1215.883
vp8l	2	baseline	1216.670
vp8l	3	baseline	1217.110
vp8l	3	candidate	1221.595
vp8l	4	candidate	1222.334
vp8l	4	baseline	1223.058
vp8l	5	baseline	1222.539
vp8l	5	candidate	1218.447
vp8l	6	candidate	1216.228
vp8l	6	baseline	1216.784
vp8l	7	baseline	1217.204
vp8l	7	candidate	1217.263
vp8l	8	candidate	1233.392
vp8l	8	baseline	1222.411
vp8l	9	baseline	1219.151
vp8l	9	candidate	1218.653
vp8l	10	candidate	1217.044
vp8l	10	baseline	1226.391
vp8l	11	baseline	1222.120
vp8l	11	candidate	1218.189
vp8l	12	candidate	1218.398
vp8l	12	baseline	1224.580
vp8l	13	baseline	1221.889
vp8l	13	candidate	1218.498
```

## Micro raw

```tsv
workload	round	variant	value
color_transform	1	baseline	123950.34
color_transform	1	candidate	124251.65
color_transform	2	candidate	124566.36
color_transform	2	baseline	123998.94
color_transform	3	baseline	123945.76
color_transform	3	candidate	124373.75
color_transform	4	candidate	125727.42
color_transform	4	baseline	123935.44
color_transform	5	baseline	123858.54
color_transform	5	candidate	124542.08
color_transform	6	candidate	124363.23
color_transform	6	baseline	123848.77
color_transform	7	baseline	123941.94
color_transform	7	candidate	125784.66
```
