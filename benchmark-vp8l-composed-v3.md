# Clean VP8L composed v3 benchmark

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- candidate: `4cd194935d100a09acf24eb24d8c1343c7844844`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- candidate tree differs from baseline in production `mod.rs` + `reverse_transform.rs` only
- hashes match; tests/docs/Clippy/fmt/MSRV build pass
- aggregate workloads: 25 alternating paired rounds; per-file: 13 rounds

## Aggregate

| workload | base us | candidate us | paired median | positive | range |
|---|---:|---:|---:|---:|---:|
| repo-corpus | 1141.572 | 1062.097 | 1.0748x | 25/25 | 1.0689–1.0808x |
| large-structured-z9 | 18423.240 | 15394.804 | 1.1970x | 25/25 | 1.1917–1.2243x |
| generated-z9 | 15882.058 | 14316.429 | 1.1102x | 25/25 | 1.1038–1.1256x |
| generated-z0-controls | 30521.664 | 30182.103 | 1.0111x | 25/25 | 1.0057–1.0309x |

## Per-file

| file | base us | candidate us | paired median | positive | range |
|---|---:|---:|---:|---:|---:|
| repo/1_webp_ll.webp | 1684.329 | 1576.184 | 1.0690x | 13/13 | 1.0633–1.0776x |
| repo/2_webp_ll.webp | 1477.384 | 1294.936 | 1.1379x | 13/13 | 1.1326–1.1491x |
| repo/3_webp_ll.webp | 4673.901 | 4389.137 | 1.0654x | 13/13 | 1.0558–1.0849x |
| repo/4_webp_ll.webp | 749.201 | 672.806 | 1.1128x | 13/13 | 1.0977–1.1345x |
| repo/5_webp_ll.webp | 1954.082 | 1846.034 | 1.0590x | 13/13 | 1.0507–1.0698x |
| repo/color_index.webp | 8.661 | 8.780 | 0.9818x | 0/13 | 0.9349–0.9927x |
| repo/lossless_indexed_1bit_palette.webp | 35.045 | 35.093 | 0.9970x | 5/13 | 0.9914–1.0085x |
| repo/lossless_indexed_2bit_palette.webp | 42.147 | 42.413 | 0.9948x | 0/13 | 0.9825–0.9981x |
| repo/lossless_indexed_4bit_palette.webp | 650.309 | 639.064 | 1.0202x | 13/13 | 1.0021–1.0243x |
| repo/tiny.webp | 7.743 | 7.835 | 0.9916x | 3/13 | 0.9142–1.0039x |
| gen/structured-z0 | 47104.743 | 46601.973 | 1.0109x | 11/13 | 0.9903–1.0143x |
| gen/structured-z9 | 18687.410 | 15643.053 | 1.1937x | 13/13 | 1.1604–1.2373x |
| gen/color-z0 | 20238.853 | 20077.985 | 1.0078x | 13/13 | 1.0062–1.0239x |
| gen/color-z9 | 9844.777 | 8159.195 | 1.2060x | 13/13 | 1.1974–1.2775x |
| gen/corr-z0 | 25937.390 | 25623.891 | 1.0118x | 12/13 | 0.9990–1.0292x |
| gen/corr-z9 | 27285.606 | 25328.226 | 1.0783x | 13/13 | 1.0667–1.0966x |
| gen/stripes-z9 | 7079.165 | 6008.983 | 1.1902x | 13/13 | 1.1645–1.2166x |
| gen/tiles-z9 | 8226.413 | 7097.256 | 1.1589x | 13/13 | 1.1352–1.1854x |
| gen/gradient-z9 | 14466.201 | 13361.225 | 1.0826x | 13/13 | 1.0692–1.0995x |
| gen/noise-z9 | 28644.490 | 27865.522 | 1.0284x | 13/13 | 1.0141–1.0569x |

## Breadth

- per-file median ratio: **1.0622x**
- files positive: **16/20**
