# Safe subtract-green SLP benchmark

- branch baseline: `531903907c125e14fd9a5eb5cebe7dc567bab9c4`
- ephemeral candidate: `baa95efe11bf7eb909260237fe2ce5801d407901`
- CPU: `AMD EPYC 7763 64-Core Processor`
- architecture / vCPUs: `x86_64` / `4`
- static VP8L fixtures: `10`
- candidate remains 100% safe Rust; crate-level `forbid(unsafe_code)` and MSRV are unchanged
- candidate source is intentionally not retained on the branch pending benchmark review
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 11 alternating A/B rounds, 100 corpus iterations per variant per round

| Workload | baseline median | candidate median | ratio of medians | paired median | paired range |
|---|---:|---:|---:|---:|---:|
| VP8L corpus | 1142.352 us | 1135.096 us | 1.006x | 1.006x | 1.001–1.021x |

## Raw samples

```tsv
workload	round	variant	us_per_decode
vp8l_corpus	1	baseline	1144.039
vp8l_corpus	1	candidate	1134.726
vp8l_corpus	2	candidate	1134.114
vp8l_corpus	2	baseline	1141.674
vp8l_corpus	3	baseline	1154.436
vp8l_corpus	3	candidate	1130.526
vp8l_corpus	4	candidate	1135.096
vp8l_corpus	4	baseline	1141.070
vp8l_corpus	5	baseline	1140.873
vp8l_corpus	5	candidate	1133.354
vp8l_corpus	6	candidate	1139.513
vp8l_corpus	6	baseline	1144.044
vp8l_corpus	7	baseline	1142.352
vp8l_corpus	7	candidate	1135.700
vp8l_corpus	8	candidate	1136.482
vp8l_corpus	8	baseline	1141.096
vp8l_corpus	9	baseline	1140.950
vp8l_corpus	9	candidate	1140.292
vp8l_corpus	10	candidate	1131.281
vp8l_corpus	10	baseline	1144.312
vp8l_corpus	11	baseline	1143.286
vp8l_corpus	11	candidate	1139.760
```
