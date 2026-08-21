# Direct VP8 tree leaf benchmark

- baseline: `97d2d9a00444d297784060886719d58c69a3b898`
- candidate: `0d5e91362854c7f2972014eafa77ae5207e2db58`
- CPU: `AMD EPYC 7763 64-Core Processor`
- vCPUs: `4`
- candidate is 100% safe Rust; MSRV 1.80.1; normal release target

| Workload | baseline | candidate | ratio | paired median | paired range |
|---|---:|---:|---:|---:|---:|
| issue119 | 369825.422 us | 366810.293 us | 1.008x | 1.009x | 1.001–1.036x |
| issue136 | 35948.849 us | 35742.451 us | 1.006x | 1.006x | 1.001–1.060x |

```tsv
workload	round	variant	us
issue119	1	baseline	373501.780
issue136	1	baseline	37948.621
issue119	1	candidate	367109.464
issue136	1	candidate	35794.775
issue119	2	candidate	367387.709
issue136	2	candidate	35742.451
issue119	2	baseline	369491.058
issue136	2	baseline	36052.447
issue119	3	baseline	369911.328
issue136	3	baseline	36000.812
issue119	3	candidate	366164.811
issue136	3	candidate	35709.281
issue119	4	candidate	368476.665
issue136	4	candidate	35861.219
issue119	4	baseline	368890.412
issue136	4	baseline	35938.821
issue119	5	baseline	369825.422
issue136	5	baseline	35928.577
issue119	5	candidate	366810.293
issue136	5	candidate	35708.034
issue119	6	candidate	366789.841
issue136	6	candidate	35710.055
issue119	6	baseline	369964.683
issue136	6	baseline	35978.858
issue119	7	baseline	379617.198
issue136	7	baseline	35975.182
issue119	7	candidate	366364.560
issue136	7	candidate	35752.967
issue119	8	candidate	365969.820
issue136	8	candidate	35700.340
issue119	8	baseline	369810.099
issue136	8	baseline	35891.768
issue119	9	baseline	369897.201
issue136	9	baseline	35948.849
issue119	9	candidate	367129.433
issue136	9	candidate	35731.267
issue119	10	candidate	366847.343
issue136	10	candidate	35848.031
issue119	10	baseline	369173.002
issue136	10	baseline	35870.812
issue119	11	baseline	369710.321
issue136	11	baseline	35854.652
issue119	11	candidate	365902.850
issue136	11	candidate	35767.089
```
