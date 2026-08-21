# VP8 range normalization benchmark

- baseline: `ace0415fcce012f7ccf2d036cbc678ed3f630f52`
- candidate: `cda8426ed80e1c9a95f9fa66799bf5fee9e8715c`
- CPU: `AMD EPYC 7763 64-Core Processor`
- safe Rust; MSRV 1.80.1; normal release target

| Workload | baseline | candidate | ratio | paired median | range |
|---|---:|---:|---:|---:|---:|
| issue119 | 366013.098 us | 361153.492 us | 1.013x | 1.014x | 1.012–1.015x |
| issue136 | 35817.983 us | 35605.110 us | 1.006x | 1.006x | 0.999–1.014x |

```tsv
workload	round	variant	us
issue119	1	baseline	366013.098
issue136	1	baseline	35788.171
issue119	1	candidate	360927.295
issue136	1	candidate	35632.656
issue119	2	candidate	361195.635
issue136	2	candidate	35605.110
issue119	2	baseline	366302.511
issue136	2	baseline	35817.983
issue119	3	baseline	366415.914
issue136	3	baseline	35791.733
issue119	3	candidate	361467.842
issue136	3	candidate	35589.700
issue119	4	candidate	361153.492
issue136	4	candidate	35490.528
issue119	4	baseline	366708.585
issue136	4	baseline	35788.822
issue119	5	baseline	365959.885
issue136	5	baseline	35821.543
issue119	5	candidate	360446.641
issue136	5	candidate	35610.304
issue119	6	candidate	361447.575
issue136	6	candidate	35539.589
issue119	6	baseline	365824.381
issue136	6	baseline	35750.190
issue119	7	baseline	365423.905
issue136	7	baseline	35823.704
issue119	7	candidate	361127.365
issue136	7	candidate	35620.302
issue119	8	candidate	360527.438
issue136	8	candidate	35529.825
issue119	8	baseline	365916.610
issue136	8	baseline	35984.654
issue119	9	baseline	366184.617
issue136	9	baseline	35798.891
issue119	9	candidate	361591.444
issue136	9	candidate	35617.760
issue119	10	candidate	361313.710
issue136	10	candidate	35591.178
issue119	10	baseline	366294.264
issue136	10	baseline	36082.810
issue119	11	baseline	365569.750
issue136	11	baseline	36233.574
issue119	11	candidate	360633.876
issue136	11	candidate	36270.608
```
