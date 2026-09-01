# image-webp final performance scorecard

- main: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- final candidate: `4cd194935d100a09acf24eb24d8c1343c7844844`
- CPU: `AMD EPYC 7763 64-Core Processor`
- release builds, `-C target-cpu=native`, CPU 0 pinned
- 25 alternating paired rounds

- repository files whose decoded hash differs between historical main and validated final: **1/23**
- generated VP8L decoded hashes main==final: **True**
- issue119 decoded hash main==final: **False**
- final candidate correctness is independently established by the 458-stream libwebp byte-for-byte differential; historical-main hash differences are therefore reported rather than treated as a benchmark failure.

| workload | files | main us/file | final us/file | speedup | positive | range |
|---|---:|---:|---:|---:|---:|---:|
| vp8l-static | 10 | 1694.055 | 1545.358 | **1.0965x** | 25/25 | 1.0849–1.1005x |
| vp8-static | 11 | 9894.125 | 8570.616 | **1.1531x** | 25/25 | 1.1414–1.1588x |
| animated | 2 | 1283.345 | 1084.210 | **1.1840x** | 25/25 | 1.1759–1.1974x |
| generated-vp8l-z9 | 4 | 57196.876 | 60520.698 | **0.9469x** | 0/25 | 0.9416–0.9500x |
| issue119-large-vp8l | 1 | 493224.949 | 369905.968 | **1.3342x** | 25/25 | 1.3166–1.3715x |

## Historical-main output differences

- `tests/images/animated/random_lossless.webp`
