# VP8L v4 clean candidate matrix

- v3 baseline: `4cd194935d100a09acf24eb24d8c1343c7844844`
- CPU: `AMD EPYC 7763 64-Core Processor`
- 17 alternating paired rounds; all candidate hashes/tests/docs/Clippy/fmt/MSRV passed

| workload | candidate | v3 median | candidate median | speedup vs v3 | positive | range |
|---|---|---:|---:|---:|---:|---:|
| corpus | color_only | 1024.694 us | 1011.732 us | 1.0142x | 17/17 | 1.0062–1.0242x |
| corpus | color_root10 | 1024.694 us | 1029.975 us | 0.9957x | 2/17 | 0.9742–1.0113x |
| corpus | color_pred1main | 1024.694 us | 1026.498 us | 1.0001x | 9/17 | 0.9929–1.0116x |
| corpus | color_root10_pred1main | 1024.694 us | 1039.545 us | 0.9844x | 1/17 | 0.9812–1.0013x |
| gen_z9 | color_only | 10912.320 us | 11065.962 us | 0.9864x | 0/17 | 0.9675–0.9979x |
| gen_z9 | color_root10 | 10912.320 us | 9359.456 us | 1.1649x | 17/17 | 1.1220–1.1776x |
| gen_z9 | color_pred1main | 10912.320 us | 11044.179 us | 0.9878x | 0/17 | 0.9758–0.9967x |
| gen_z9 | color_root10_pred1main | 10912.320 us | 9369.185 us | 1.1617x | 17/17 | 1.1327–1.1744x |
| structured | color_only | 6407.211 us | 7076.488 us | 0.9045x | 0/17 | 0.8709–0.9308x |
| structured | color_root10 | 6407.211 us | 7091.227 us | 0.9023x | 0/17 | 0.8730–0.9288x |
| structured | color_pred1main | 6407.211 us | 7360.859 us | 0.8698x | 0/17 | 0.6457–0.8983x |
| structured | color_root10_pred1main | 6407.211 us | 7369.056 us | 0.8694x | 0/17 | 0.8369–0.8927x |
| noise | color_only | 42221.622 us | 41870.992 us | 1.0070x | 15/17 | 0.9661–1.0191x |
| noise | color_root10 | 42221.622 us | 30102.751 us | 1.4017x | 17/17 | 1.3885–1.4160x |
| noise | color_pred1main | 42221.622 us | 41919.655 us | 1.0061x | 14/17 | 0.9309–1.0156x |
| noise | color_root10_pred1main | 42221.622 us | 30112.930 us | 1.4006x | 17/17 | 1.3805–1.4211x |
