# Direct libwebp-style DC-only IDCT benchmark

- baseline: `bdbacda46d7575bca2e783b92194b5e6ec5865a1`
- candidate: `c4b68c9cbde0e0d227e7bba28370a48478f0dbcd`
- CPU: `AMD EPYC 7763 64-Core Processor`
- full decoded output hashes match before timing

| Workload | baseline | candidate | ratio | paired median | range |
|---|---:|---:|---:|---:|---:|
| issue119 | 465450.537 us | 468312.862 us | 0.994x | 0.994x | 0.980–1.024x |
| issue136 | 43835.060 us | 43081.905 us | 1.017x | 1.022x | 1.007–1.030x |

```tsv
issue119	1	base	465450.537
issue136	1	base	43562.852
issue119	1	cand	461019.753
issue136	1	cand	42454.956
issue119	2	cand	461109.868
issue136	2	cand	43127.664
issue119	2	base	461232.579
issue136	2	base	43848.296
issue119	3	base	468835.634
issue136	3	base	43826.838
issue119	3	cand	468551.209
issue136	3	cand	42711.101
issue119	4	cand	459194.031
issue136	4	cand	43513.899
issue119	4	base	470046.407
issue136	4	base	43913.205
issue119	5	base	468498.182
issue136	5	base	44583.305
issue119	5	cand	471399.919
issue136	5	cand	43271.329
issue119	6	cand	469761.450
issue136	6	cand	43081.905
issue119	6	base	464879.283
issue136	6	base	44191.040
issue119	7	base	462741.398
issue136	7	base	43227.401
issue119	7	cand	465837.777
issue136	7	cand	42908.817
issue119	8	cand	466336.288
issue136	8	cand	42889.829
issue119	8	base	473974.441
issue136	8	base	43835.060
issue119	9	base	463919.588
issue136	9	base	43629.883
issue119	9	cand	468312.862
issue136	9	cand	43099.403
issue119	10	cand	470053.227
issue136	10	cand	43248.010
issue119	10	base	460498.248
issue136	10	base	43979.409
issue119	11	base	465775.853
issue136	11	base	43756.891
issue119	11	cand	470589.161
issue136	11	cand	42751.752
```
