# Final VP8L wide-root confirmation

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- composed base: `4cd194935d100a09acf24eb24d8c1343c7844844`
- candidate: `888f7a558f35c4c1975c7e5c048b56450233283c`
- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- release native, CPU 0 pinned, 17 alternating/reversed 3-way rounds
- candidate hashes == validated composed-base hashes on repository VP8L corpus and every generated stream

| workload | main us | base us | candidate us | candidate/main | candidate/base | cand>main | cand>base |
|---|---:|---:|---:|---:|---:|---:|---:|
| structured-z0 | 45753.408 | 45421.119 | 45442.097 | **1.0053x** | **0.9942x** | 10/17 | 7/17 |
| structured-z9 | 40452.997 | 38453.938 | 38421.843 | **1.0583x** | **1.0045x** | 17/17 | 11/17 |
| gradient-z0 | 45485.149 | 45586.869 | 45301.373 | **1.0034x** | **1.0027x** | 11/17 | 11/17 |
| gradient-z9 | 46537.249 | 44507.097 | 44396.714 | **1.0467x** | **1.0023x** | 17/17 | 10/17 |
| corr-z0 | 59754.830 | 59163.133 | 61324.080 | **0.9734x** | **0.9655x** | 0/17 | 0/17 |
| corr-z9 | 71390.331 | 65231.565 | 66681.386 | **1.0712x** | **0.9753x** | 17/17 | 1/17 |
| color-z0 | 45455.825 | 45204.383 | 45418.320 | **0.9975x** | **0.9980x** | 7/17 | 8/17 |
| color-z9 | 36202.365 | 34005.635 | 34157.847 | **1.0573x** | **0.9929x** | 16/17 | 4/17 |
| noise-z0 | 91342.386 | 93119.764 | 99489.304 | **0.9149x** | **0.9384x** | 0/17 | 0/17 |
| noise-z9 | 91460.358 | 123482.534 | 125930.550 | **0.7272x** | **0.9824x** | 0/17 | 2/17 |
| generated-z0-aggregate | 58813.027 | 58757.370 | 60350.318 | **0.9734x** | **0.9740x** | 0/17 | 1/17 |
| generated-z9-aggregate | 57531.118 | 61232.417 | 62057.754 | **0.9251x** | **0.9888x** | 0/17 | 1/17 |
| repo-vp8l-corpus | 1668.275 | 1582.667 | 1650.441 | **1.0127x** | **0.9594x** | 15/17 | 0/17 |
| issue119 | 23956.791 | 22759.095 | 22660.004 | **1.0533x** | **1.0099x** | 17/17 | 11/17 |
