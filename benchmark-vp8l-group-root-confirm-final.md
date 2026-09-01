# Final VP8L group-static Huffman root confirmation

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- composed base: `4cd194935d100a09acf24eb24d8c1343c7844844`
- candidate: exact composed base materialized with group-static 9/11-bit Huffman roots
- CPU: `AMD EPYC 7763 64-Core Processor`
- release native, CPU 0 pinned, 21 alternating/reversed 3-way rounds
- candidate hashes == composed-base hashes on repository VP8L corpus, every generated stream, and issue119 when available
- selector: 11-bit group when any implicit tree has >=256 non-zero symbols and >=1/8 have code length >9; otherwise 9-bit

| workload | main us | base us | candidate us | candidate/main | candidate/base | cand>main | cand>base |
|---|---:|---:|---:|---:|---:|---:|---:|
| repo-vp8l-corpus | 1680.439 | 1567.463 | 1536.566 | **1.0932x** | **1.0188x** | 21/21 | 21/21 |
| structured-z0 | 45728.047 | 45747.601 | 45709.720 | **1.0004x** | **1.0006x** | 12/21 | 15/21 |
| structured-z9 | 34552.456 | 31947.350 | 31797.518 | **1.0864x** | **1.0051x** | 21/21 | 18/21 |
| gradient-z0 | 45475.881 | 45539.164 | 45414.445 | **1.0009x** | **1.0025x** | 12/21 | 18/21 |
| gradient-z9 | 47216.485 | 44977.881 | 44856.594 | **1.0527x** | **1.0027x** | 20/21 | 17/21 |
| corr-z0 | 59074.743 | 58137.591 | 56735.079 | **1.0406x** | **1.0243x** | 21/21 | 21/21 |
| corr-z9 | 62233.961 | 57474.393 | 56494.178 | **1.1014x** | **1.0174x** | 21/21 | 21/21 |
| color-z0 | 45575.478 | 45608.425 | 45588.144 | **0.9991x** | **1.0003x** | 9/21 | 12/21 |
| color-z9 | 30679.617 | 28173.711 | 28091.989 | **1.0900x** | **1.0030x** | 21/21 | 15/21 |
| noise-z0 | 93766.199 | 99305.488 | 95532.021 | **0.9823x** | **1.0354x** | 0/21 | 21/21 |
| noise-z9 | 88937.304 | 116052.520 | 84205.175 | **1.0541x** | **1.3814x** | 21/21 | 21/21 |
| generated-z0-aggregate | 57365.951 | 58499.155 | 57565.580 | **0.9959x** | **1.0155x** | 3/21 | 20/21 |
| generated-z9-aggregate | 52514.958 | 55487.779 | 48871.822 | **1.0747x** | **1.1346x** | 21/21 | 21/21 |
| issue119 | 25068.767 | 23048.636 | 23176.770 | **1.0785x** | **0.9969x** | 21/21 | 10/21 |
