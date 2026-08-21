# Safe lossless color-transform benchmark

- branch baseline: `0a90358526c12e604514c19e247225385056700e`
- ephemeral candidate: `108962515064d8f6936dc22ce998e48f3ef9e2fd`
- CPU: `Intel(R) Xeon(R) 6973P-C`
- architecture / vCPUs: `x86_64` / `4`
- static VP8L fixtures: `10`
- candidate remains 100% safe Rust; crate-level `forbid(unsafe_code)` is unchanged
- candidate source is intentionally not retained on the branch pending benchmark review
- runner: `ubuntu-latest`, release, `-C target-cpu=native`, pinned to CPU 0
- method: 11 alternating A/B rounds over the full static VP8L fixture corpus

| Workload | baseline median | candidate median | ratio of medians | paired median | paired range |
|---|---:|---:|---:|---:|---:|
| VP8L corpus | 963.874 us | 970.929 us | 0.993x | 0.992x | 0.829–0.999x |

## Raw samples

```tsv
workload	round	variant	us_per_decode
vp8l_corpus	1	baseline	994.889
vp8l_corpus	1	candidate	1199.905
vp8l_corpus	2	candidate	973.846
vp8l_corpus	2	baseline	963.874
vp8l_corpus	3	baseline	959.756
vp8l_corpus	3	candidate	969.884
vp8l_corpus	4	candidate	975.237
vp8l_corpus	4	baseline	967.732
vp8l_corpus	5	baseline	968.213
vp8l_corpus	5	candidate	970.929
vp8l_corpus	6	candidate	982.924
vp8l_corpus	6	baseline	981.934
vp8l_corpus	7	baseline	965.144
vp8l_corpus	7	candidate	972.632
vp8l_corpus	8	candidate	969.511
vp8l_corpus	8	baseline	961.444
vp8l_corpus	9	baseline	951.464
vp8l_corpus	9	candidate	964.632
vp8l_corpus	10	candidate	893.105
vp8l_corpus	10	baseline	851.861
vp8l_corpus	11	baseline	853.181
vp8l_corpus	11	candidate	854.732
```
