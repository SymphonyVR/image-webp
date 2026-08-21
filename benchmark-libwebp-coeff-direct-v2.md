# Libwebp-style VP8 coefficient benchmark v2

- baseline: `7500528697e481992e096897c0fa642f834e0e5f`
- candidate: `66f88d253ed67a30edf0fa1d34f37b4edf734195`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- full-output hashes verified outside timed region
- issue119 hash: `bc15e6a2fda9b057`
- issue136 hash: `9172fbf3bfcd3f5a`

| Workload | baseline | candidate | ratio | paired median | range |
|---|---:|---:|---:|---:|---:|
| issue119 | 357831.041 us | 329726.902 us | 1.085x | 1.087x | 1.060–1.106x |
| issue136 | 36263.078 us | 34818.288 us | 1.041x | 1.041x | 1.008–1.060x |

```tsv
issue119	1	base	359496.482
issue136	1	base	36155.127
issue119	1	cand	329726.902
issue136	1	cand	34825.499
issue119	2	cand	336649.374
issue136	2	cand	34815.744
issue119	2	base	356994.435
issue136	2	base	36410.819
issue119	3	base	361928.736
issue136	3	base	36196.605
issue119	3	cand	328324.679
issue136	3	cand	34982.767
issue119	4	cand	336005.389
issue136	4	cand	34759.250
issue119	4	base	357256.643
issue136	4	base	36522.266
issue119	5	base	357831.041
issue136	5	base	36186.542
issue119	5	cand	328920.871
issue136	5	cand	34855.156
issue119	6	cand	327271.738
issue136	6	cand	34912.692
issue119	6	base	361941.175
issue136	6	base	37001.549
issue119	7	base	356556.797
issue136	7	base	36255.517
issue119	7	cand	330327.130
issue136	7	cand	34817.517
issue119	8	cand	336442.582
issue136	8	cand	36036.164
issue119	8	base	358083.005
issue136	8	base	36310.086
issue119	9	base	362181.660
issue136	9	base	36263.078
issue119	9	cand	335386.595
issue136	9	cand	34818.288
issue119	10	cand	335895.431
issue136	10	cand	34789.763
issue119	10	base	358516.602
issue136	10	base	36306.809
issue119	11	base	357609.751
issue136	11	base	36274.406
issue119	11	cand	329115.910
issue136	11	cand	34780.567
issue119	12	cand	329132.220
issue136	12	cand	34848.690
issue119	12	base	357802.683
issue136	12	base	36204.296
issue119	13	base	357716.966
issue136	13	base	36218.783
issue119	13	cand	328287.751
issue136	13	cand	34796.796
```
