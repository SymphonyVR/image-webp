# Safe loop-filter threshold benchmark

- branch baseline: `e54f8753da87328365b9739745558454e485af09`
- ephemeral candidate: `1f573942636ebe5aba879292a7fb792f731ab5a5`
- CPU: `AMD EPYC 7763 64-Core Processor`
- architecture / vCPUs: `x86_64` / `4`
- candidate remains 100% safe Rust; crate-level `forbid(unsafe_code)` is unchanged
- candidate source is intentionally not retained on the branch pending benchmark review
- workload: issue #136 `honk.webp`, where loop filtering was profiled at roughly half of decode time
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 11 alternating A/B rounds; paired speedup is baseline/candidate in the same round

| Workload | baseline median | candidate median | ratio of medians | paired median | paired range |
|---|---:|---:|---:|---:|---:|
| issue136 | 34910.153 us | 35607.781 us | 0.980x | 0.980x | 0.975–1.038x |

## Raw samples

```tsv
workload	round	variant	us_per_decode
issue136	1	baseline	34809.302
issue136	1	candidate	35502.540
issue136	2	candidate	35497.438
issue136	2	baseline	34818.106
issue136	3	baseline	34669.019
issue136	3	candidate	35570.571
issue136	4	candidate	35470.242
issue136	4	baseline	34889.992
issue136	5	baseline	35284.396
issue136	5	candidate	35548.302
issue136	6	candidate	35624.948
issue136	6	baseline	34924.829
issue136	7	baseline	35001.897
issue136	7	candidate	35701.314
issue136	8	candidate	35756.406
issue136	8	baseline	37116.686
issue136	9	baseline	35154.547
issue136	9	candidate	35658.840
issue136	10	candidate	35685.308
issue136	10	baseline	34863.279
issue136	11	baseline	34910.153
issue136	11	candidate	35607.781
```
