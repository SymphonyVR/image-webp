# Combined VP8 tree/range benchmark

- baseline: `701897eec8d4b23dce74208b4b018af7be1de21f`
- candidate: `8ed34c9fac477c5974900cdd0a1ccd1db9a8e73a`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- safe Rust; MSRV 1.80.1; normal release target

| Workload | baseline | candidate | ratio | paired median | range |
|---|---:|---:|---:|---:|---:|
| issue119 | 333526.399 us | 334902.229 us | 0.996x | 0.988x | 0.974–1.032x |
| issue136 | 32953.366 us | 33372.215 us | 0.987x | 0.987x | 0.951–1.048x |

```tsv
workload	round	variant	us
issue119	1	baseline	324401.176
issue136	1	baseline	32317.104
issue119	1	candidate	329572.673
issue136	1	candidate	32753.806
issue119	2	candidate	326228.025
issue136	2	candidate	33174.114
issue119	2	baseline	332066.253
issue136	2	baseline	32819.940
issue119	3	baseline	327209.280
issue136	3	baseline	32595.303
issue119	3	candidate	331762.857
issue136	3	candidate	33406.168
issue119	4	candidate	340574.053
issue136	4	candidate	33650.161
issue119	4	baseline	338206.029
issue136	4	baseline	32905.338
issue119	5	baseline	327578.593
issue136	5	baseline	32708.465
issue119	5	candidate	333106.349
issue136	5	candidate	32185.776
issue119	6	candidate	334902.229
issue136	6	candidate	32959.345
issue119	6	baseline	334203.533
issue136	6	baseline	32953.366
issue119	7	baseline	339430.833
issue136	7	baseline	33582.507
issue119	7	candidate	332497.801
issue136	7	candidate	32035.733
issue119	8	candidate	330152.640
issue136	8	candidate	34494.477
issue119	8	baseline	340616.591
issue136	8	baseline	33435.658
issue119	9	baseline	336533.345
issue136	9	baseline	33688.745
issue119	9	candidate	340531.043
issue136	9	candidate	34976.080
issue119	10	candidate	342557.427
issue136	10	candidate	34258.075
issue119	10	baseline	333526.399
issue136	10	baseline	32575.531
issue119	11	baseline	331739.951
issue136	11	baseline	33127.042
issue119	11	candidate	338144.781
issue136	11	candidate	33372.215
issue119	12	candidate	336328.318
issue136	12	candidate	32809.430
issue119	12	baseline	335037.025
issue136	12	baseline	33491.940
issue119	13	baseline	331812.422
issue136	13	baseline	33397.747
issue119	13	candidate	336067.017
issue136	13	candidate	34068.438
```
