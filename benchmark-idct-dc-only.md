# Libwebp-style DC-only IDCT benchmark

- baseline: `6957634adf1004a358230db17ce1d404846ca4b0`
- candidate: `29c73d4c4b58ae1301e7bf3a26233e5c15a70707`
- CPU: `Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz`
- full output hashes match before timing

| Workload | baseline | candidate | ratio | paired median | range |
|---|---:|---:|---:|---:|---:|
| issue119 | 427851.557 us | 423423.557 us | 1.010x | 1.008x | 1.000–1.022x |
| issue136 | 39749.683 us | 39104.681 us | 1.016x | 1.016x | 1.013–1.021x |

```tsv
issue119	1	base	431229.163
issue136	1	base	39733.578
issue119	1	cand	423210.767
issue136	1	cand	39130.567
issue119	2	cand	424879.554
issue136	2	cand	39138.390
issue119	2	base	426696.203
issue136	2	base	39660.659
issue119	3	base	426869.564
issue136	3	base	39714.472
issue119	3	cand	426538.458
issue136	3	cand	39106.297
issue119	4	cand	423677.697
issue136	4	cand	39020.814
issue119	4	base	433127.658
issue136	4	base	39824.157
issue119	5	base	427984.221
issue136	5	base	39789.852
issue119	5	cand	421151.762
issue136	5	cand	39096.004
issue119	6	cand	422756.214
issue136	6	cand	39034.643
issue119	6	base	431771.938
issue136	6	base	39749.683
issue119	7	base	425835.523
issue136	7	base	39637.397
issue119	7	cand	423423.557
issue136	7	cand	39024.559
issue119	8	cand	422895.261
issue136	8	cand	39030.908
issue119	8	base	425825.206
issue136	8	base	39762.775
issue119	9	base	424886.317
issue136	9	base	39798.769
issue119	9	cand	421374.697
issue136	9	cand	39104.681
issue119	10	cand	423499.213
issue136	10	cand	39192.229
issue119	10	base	429398.829
issue136	10	base	39735.628
issue119	11	base	427851.557
issue136	11	base	39860.652
issue119	11	cand	427981.127
issue136	11	cand	39249.801
```
