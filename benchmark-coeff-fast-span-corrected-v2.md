# Corrected VP8 coefficient fast-span benchmark v2

- baseline: `461e27548e54e5c8973a2db5dd8b96b5619d6c5b`
- candidate: `fcdbeb90e8e675db3dd7ab6e3fe1bd4ce002750e`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- normal release target; safe Rust; MSRV 1.80.1

| Workload | baseline | candidate | ratio | paired median | range |
|---|---:|---:|---:|---:|---:|
| issue119 | 302244.745 us | 303727.442 us | 0.995x | 0.994x | 0.992–1.001x |
| issue136 | 29821.001 us | 30607.182 us | 0.974x | 0.975x | 0.917–0.986x |

```tsv
workload	round	variant	us
issue119	1	baseline	302359.351
issue136	1	baseline	29821.001
issue119	1	candidate	304287.783
issue136	1	candidate	30496.655
issue119	2	candidate	304612.757
issue136	2	candidate	30654.163
issue119	2	baseline	303711.591
issue136	2	baseline	29879.670
issue119	3	baseline	302028.969
issue136	3	baseline	29838.792
issue119	3	candidate	303727.442
issue136	3	candidate	30627.955
issue119	4	candidate	303333.117
issue136	4	candidate	30603.850
issue119	4	baseline	302625.419
issue136	4	baseline	29900.894
issue119	5	baseline	301963.487
issue136	5	baseline	30105.573
issue119	5	candidate	304456.445
issue136	5	candidate	30547.609
issue119	6	candidate	303222.186
issue136	6	candidate	30635.642
issue119	6	baseline	301416.075
issue136	6	baseline	29783.689
issue119	7	baseline	302244.745
issue136	7	baseline	29805.862
issue119	7	candidate	303193.109
issue136	7	candidate	30700.947
issue119	8	candidate	302733.065
issue136	8	candidate	30532.731
issue119	8	baseline	302973.858
issue136	8	baseline	29834.260
issue119	9	baseline	301655.190
issue136	9	baseline	29748.380
issue119	9	candidate	304186.158
issue136	9	candidate	30607.182
issue119	10	candidate	302985.747
issue136	10	candidate	32458.369
issue119	10	baseline	302357.826
issue136	10	baseline	29752.989
issue119	11	baseline	302239.004
issue136	11	baseline	29761.940
issue119	11	candidate	304570.377
issue136	11	candidate	30525.832
```
