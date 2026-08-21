# Compact VP8 coefficient probability benchmark

- baseline: `1da3bd21d181ccea007132a575e5feac742de82b`
- candidate: `5fd4abd788f8e448f650e0cfcc9b15e7c5daa2c3`
- CPU: `AMD EPYC 7763 64-Core Processor`
- raw 11-byte probability rows + fixed DCT topology; safe Rust; MSRV 1.80.1

| Workload | baseline | candidate | ratio | paired median | range |
|---|---:|---:|---:|---:|---:|
| issue119 | 370604.630 us | 370196.435 us | 1.001x | 1.006x | 0.988–1.017x |
| issue136 | 36038.315 us | 35550.302 us | 1.014x | 1.015x | 0.988–1.030x |

```tsv
issue119	1	base	369837.826
issue136	1	base	36280.461
issue119	1	cand	365186.483
issue136	1	cand	35462.095
issue119	2	cand	378514.340
issue136	2	cand	35622.994
issue119	2	base	373787.985
issue136	2	base	36024.909
issue119	3	base	370806.865
issue136	3	base	36013.773
issue119	3	cand	367739.731
issue136	3	cand	35489.535
issue119	4	cand	370196.435
issue136	4	cand	35643.995
issue119	4	base	369280.584
issue136	4	base	36050.195
issue119	5	base	369318.916
issue136	5	base	36605.296
issue119	5	cand	372815.522
issue136	5	cand	35550.302
issue119	6	cand	365968.031
issue136	6	cand	35469.959
issue119	6	base	369626.041
issue136	6	base	35993.559
issue119	7	base	369178.598
issue136	7	base	36038.315
issue119	7	cand	370722.689
issue136	7	cand	36473.482
issue119	8	cand	366610.193
issue136	8	cand	35539.846
issue119	8	base	370604.630
issue136	8	base	36060.514
issue119	9	base	372623.592
issue136	9	base	35937.084
issue119	9	cand	366236.714
issue136	9	cand	35975.604
issue119	10	cand	373498.586
issue136	10	cand	35619.019
issue119	10	base	370903.956
issue136	10	base	35992.397
issue119	11	base	373900.963
issue136	11	base	36141.071
issue119	11	cand	371550.007
issue136	11	cand	35513.518
```
