# Final VP8L wide-root confirmation

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- composed base: `4cd194935d100a09acf24eb24d8c1343c7844844`
- candidate: `87f1f0c625b5169bd9162aaa02d1c97e68a20cf4`
- CPU: `Intel(R) Xeon(R) 6973P-C`
- release native, CPU 0 pinned, 17 alternating/reversed 3-way rounds
- candidate hashes == validated composed-base hashes on repository VP8L corpus and every generated stream

| workload | main us | base us | candidate us | candidate/main | candidate/base | cand>main | cand>base |
|---|---:|---:|---:|---:|---:|---:|---:|
| structured-z0 | 33070.608 | 33055.035 | 33015.774 | **1.0007x** | **0.9992x** | 11/17 | 8/17 |
| structured-z9 | 31371.956 | 30617.317 | 30537.683 | **1.0245x** | **1.0008x** | 15/17 | 9/17 |
| gradient-z0 | 32930.429 | 33013.002 | 32979.177 | **0.9962x** | **1.0016x** | 6/17 | 9/17 |
| gradient-z9 | 34329.660 | 33489.094 | 33519.025 | **1.0222x** | **0.9994x** | 17/17 | 8/17 |
| corr-z0 | 43379.271 | 43229.175 | 44833.591 | **0.9708x** | **0.9611x** | 4/17 | 3/17 |
| corr-z9 | 53500.595 | 48479.905 | 49287.233 | **1.0855x** | **0.9852x** | 15/17 | 0/17 |
| color-z0 | 32820.433 | 32907.827 | 32951.120 | **0.9966x** | **1.0000x** | 5/17 | 9/17 |
| color-z9 | 29000.690 | 27673.540 | 28112.422 | **1.0426x** | **0.9963x** | 13/17 | 6/17 |
| noise-z0 | 68591.072 | 69856.292 | 75631.610 | **0.9145x** | **0.9262x** | 1/17 | 2/17 |
| noise-z9 | 68913.361 | 92620.744 | 71487.673 | **0.9647x** | **1.2940x** | 3/17 | 17/17 |
| generated-z0-aggregate | 41808.904 | 42043.829 | 43645.559 | **0.9578x** | **0.9649x** | 1/17 | 2/17 |
| generated-z9-aggregate | 43730.261 | 47238.460 | 42656.482 | **1.0289x** | **1.1095x** | 16/17 | 17/17 |
| repo-vp8l-corpus | 1249.128 | 1187.710 | 1236.080 | **1.0097x** | **0.9633x** | 15/17 | 1/17 |
| issue119 | 17589.575 | 16426.044 | 16687.937 | **1.0555x** | **0.9977x** | 16/17 | 5/17 |
