# VP8L group-static root selector matrix

- base: `4cd194935d100a09acf24eb24d8c1343c7844844`
- CPU: `AMD EPYC 7763 64-Core Processor`
- 11 alternating/reversed rounds; hashes equal base
- `never`: group-static architecture but never selects 11-bit root
- `q16/q8/q4`: require >=256 non-zero symbols and at least 1/16, 1/8, or 1/4 of them longer than 9 bits

| workload | variant | median us | speedup vs base | positive rounds |
|---|---|---:|---:|---:|
| repo-vp8l-corpus | base | 1560.245 | 1.0000x | 0/11 |
| repo-vp8l-corpus | never | 1521.585 | **1.0255x** | 11/11 |
| repo-vp8l-corpus | q16 | 1530.372 | **1.0179x** | 11/11 |
| repo-vp8l-corpus | q8 | 1530.485 | **1.0189x** | 11/11 |
| repo-vp8l-corpus | q4 | 1531.396 | **1.0182x** | 11/11 |
| structured-z9 | base | 18434.939 | 1.0000x | 0/11 |
| structured-z9 | never | 18322.843 | **1.0056x** | 10/11 |
| structured-z9 | q16 | 18388.527 | **1.0035x** | 7/11 |
| structured-z9 | q8 | 18460.311 | **0.9981x** | 3/11 |
| structured-z9 | q4 | 18466.432 | **0.9987x** | 2/11 |
| corr-z9 | base | 30970.489 | 1.0000x | 0/11 |
| corr-z9 | never | 30615.215 | **1.0111x** | 10/11 |
| corr-z9 | q16 | 30612.572 | **1.0114x** | 11/11 |
| corr-z9 | q8 | 30613.863 | **1.0112x** | 10/11 |
| corr-z9 | q4 | 30648.746 | **1.0105x** | 10/11 |
| noise-z9 | base | 64662.419 | 1.0000x | 0/11 |
| noise-z9 | never | 65694.350 | **0.9843x** | 0/11 |
| noise-z9 | q16 | 47156.491 | **1.3733x** | 11/11 |
| noise-z9 | q8 | 47135.048 | **1.3731x** | 11/11 |
| noise-z9 | q4 | 47081.328 | **1.3779x** | 11/11 |
| generated-z0-aggregate | base | 32079.053 | 1.0000x | 0/11 |
| generated-z0-aggregate | never | 31531.431 | **1.0173x** | 11/11 |
| generated-z0-aggregate | q16 | 31513.590 | **1.0171x** | 11/11 |
| generated-z0-aggregate | q8 | 31645.146 | **1.0135x** | 11/11 |
| generated-z0-aggregate | q4 | 31657.325 | **1.0130x** | 11/11 |
| generated-z9-aggregate | base | 30706.945 | 1.0000x | 0/11 |
| generated-z9-aggregate | never | 30711.301 | **0.9989x** | 5/11 |
| generated-z9-aggregate | q16 | 26996.134 | **1.1352x** | 11/11 |
| generated-z9-aggregate | q8 | 27011.969 | **1.1350x** | 11/11 |
| generated-z9-aggregate | q4 | 26994.136 | **1.1369x** | 11/11 |
