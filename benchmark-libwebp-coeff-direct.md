# Direct libwebp-style VP8 coefficient benchmark

- baseline: `148c60b8849222058e10bbadeac9f26aa2251275`
- candidate: `1aadb33ec11a2b67561f9750d45938ead996af32`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- full decoded output hashes match before timing
- issue119 hash: `bc15e6a2fda9b057`
- issue136 hash: `9172fbf3bfcd3f5a`

| Workload | baseline | candidate | ratio | paired median | range |
|---|---:|---:|---:|---:|---:|
| issue119 | 344465.511 us | 322592.183 us | 1.068x | 1.069x | 1.048–1.076x |
| issue136 | 32543.063 us | 31444.158 us | 1.035x | 1.035x | 1.029–1.056x |

```tsv
issue119	1	base	343916.197
issue136	1	base	33181.562
issue119	1	cand	321232.056
issue136	1	cand	31441.313
issue119	2	cand	321208.975
issue136	2	cand	31430.789
issue119	2	base	344605.881
issue136	2	base	32486.996
issue119	3	base	344410.010
issue136	3	base	32519.284
issue119	3	cand	320967.833
issue136	3	cand	31613.027
issue119	4	cand	327620.024
issue136	4	cand	31428.775
issue119	4	base	344126.747
issue136	4	base	32518.113
issue119	5	base	344850.701
issue136	5	base	32634.232
issue119	5	cand	322652.829
issue136	5	cand	31464.155
issue119	6	cand	322592.114
issue136	6	cand	31408.355
issue119	6	base	347221.430
issue136	6	base	32543.063
issue119	7	base	349348.064
issue136	7	base	32551.822
issue119	7	cand	327437.840
issue136	7	cand	31417.726
issue119	8	cand	322967.293
issue136	8	cand	31444.158
issue119	8	base	344534.539
issue136	8	base	32564.395
issue119	9	base	344410.813
issue136	9	base	32545.831
issue119	9	cand	326901.429
issue136	9	cand	31578.590
issue119	10	cand	322592.183
issue136	10	cand	31517.992
issue119	10	base	344186.641
issue136	10	base	32527.741
issue119	11	base	345198.462
issue136	11	base	33179.322
issue119	11	cand	321446.147
issue136	11	cand	31434.257
issue119	12	cand	320813.495
issue136	12	cand	31456.413
issue119	12	base	344465.511
issue136	12	base	32462.375
issue119	13	base	343996.183
issue136	13	base	32460.557
issue119	13	cand	328292.465
issue136	13	cand	31478.073
```
