# VP8L group-static Huffman root benchmark

- base: `4cd194935d100a09acf24eb24d8c1343c7844844`
- CPU: `AMD EPYC 7763 64-Core Processor`
- 13 alternating/reversed paired rounds; candidate hashes equal base
- group selector: 11-bit root when any group tree has >=256 symbols and >=1/8 of non-zero symbols longer than 9 bits; otherwise 9-bit
- group width is dispatched once per meta-Huffman run; symbol decode remains const-generic/monomorphic
- validation: tests, docs, MSRV 1.80.1 library Clippy, and MSRV build passed

| workload | base median us | candidate median us | paired speedup | positive rounds |
|---|---:|---:|---:|---:|
| repo-vp8l-corpus | 1561.033 | 1538.725 | **1.0153x** | 11/13 |
| structured-z0 | 25461.429 | 25369.989 | **1.0021x** | 12/13 |
| structured-z9 | 18843.104 | 18681.100 | **1.0097x** | 11/13 |
| gradient-z0 | 25388.802 | 25287.228 | **1.0033x** | 12/13 |
| gradient-z9 | 25034.671 | 25012.305 | **1.0031x** | 9/13 |
| corr-z0 | 32275.689 | 31588.274 | **1.0206x** | 13/13 |
| corr-z9 | 31284.775 | 30834.621 | **1.0151x** | 13/13 |
| color-z0 | 25322.451 | 25309.444 | **1.0000x** | 6/13 |
| color-z9 | 15852.244 | 15826.121 | **1.0016x** | 10/13 |
| noise-z0 | 55728.125 | 53916.383 | **1.0335x** | 13/13 |
| noise-z9 | 65696.243 | 47276.762 | **1.3887x** | 13/13 |
| generated-z0-aggregate | 32527.975 | 32025.549 | **1.0173x** | 13/13 |
| generated-z9-aggregate | 31044.385 | 27196.139 | **1.1421x** | 13/13 |

The candidate is promising but is not approved for promotion from this run alone. A longer paired confirmation and deeper correctness/platform validation are required against the composed base.
