# VP8L v3 regression-family isolation

- baseline: `4cd194935d100a09acf24eb24d8c1343c7844844`
- main reference: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- CPU: `AMD EPYC 7763 64-Core Processor`
- 17 paired rounds; candidate hashes/tests/docs/Clippy/fmt/MSRV passed

| workload | candidate | base median | candidate median | paired speedup | positive | range |
|---|---|---:|---:|---:|---:|---:|
| corpus | root10 | 1060.288 us | 1039.595 us | 1.0190x | 14/17 | 0.9857–1.0300x |
| corpus | pred1_main | 1060.288 us | 1046.883 us | 1.0120x | 16/17 | 0.9790–1.0211x |
| corpus | root10_pred1 | 1060.288 us | 1062.740 us | 0.9983x | 4/17 | 0.9875–1.0065x |
| gen_z9 | root10 | 10907.446 us | 9302.279 us | 1.1780x | 17/17 | 1.1643–1.2190x |
| gen_z9 | pred1_main | 10907.446 us | 11082.447 us | 0.9843x | 2/17 | 0.9003–1.0253x |
| gen_z9 | root10_pred1 | 10907.446 us | 9499.276 us | 1.1503x | 17/17 | 1.1424–1.2075x |
| large | root10 | 6387.919 us | 6386.439 us | 1.0003x | 9/17 | 0.9853–1.0261x |
| large | pred1_main | 6387.919 us | 7135.801 us | 0.8947x | 0/17 | 0.8851–0.9179x |
| large | root10_pred1 | 6387.919 us | 7143.215 us | 0.8940x | 0/17 | 0.8791–0.9072x |
