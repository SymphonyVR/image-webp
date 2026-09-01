# VP8L Huffman tree-shape analysis

- candidate lineage: `4cd194935d100a09acf24eb24d8c1343c7844844`
- each stream decoded once; Huffman build histograms instrumented

| workload | trees | median symbols | max code len | median >9-symbol share | max>=10 | max>=11 | >9 share >=12.5% |
|---|---:|---:|---:|---:|---:|---:|---:|
| structured-z0 | 30 | 8.0 | 11 | 0.00% | 2 | 1 | 2 |
| structured-z9 | 14 | 8.5 | 9 | 0.00% | 0 | 0 | 0 |
| gradient-z0 | 22 | 10.0 | 9 | 0.00% | 0 | 0 | 0 |
| gradient-z9 | 22 | 8.5 | 9 | 0.00% | 0 | 0 | 0 |
| corr-z0 | 34 | 8.5 | 13 | 0.00% | 7 | 7 | 3 |
| corr-z9 | 112 | 12.0 | 14 | 0.00% | 27 | 20 | 20 |
| color-z0 | 18 | 5.0 | 9 | 0.00% | 0 | 0 | 0 |
| color-z9 | 6 | 3.0 | 4 | 0.00% | 0 | 0 | 0 |
| noise-z0 | 34 | 14.0 | 14 | 0.00% | 6 | 6 | 3 |
| noise-z9 | 22 | 13.0 | 15 | 0.00% | 7 | 5 | 7 |
| repo-vp8l-corpus | 591 | 19.0 | 14 | 0.00% | 195 | 147 | 187 |
| issue119 | 0 | - | - | - | - | - | - |

## High-entropy candidate selectors

| workload | long>=1/16 | long>=1/8 | long>=1/4 | long>=1/2 | max>=12 | max>=13 |
|---|---:|---:|---:|---:|---:|---:|
| structured-z0 | 2 | 2 | 1 | 0 | 0 | 0 |
| structured-z9 | 0 | 0 | 0 | 0 | 0 | 0 |
| gradient-z0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gradient-z9 | 0 | 0 | 0 | 0 | 0 | 0 |
| corr-z0 | 7 | 3 | 0 | 0 | 3 | 1 |
| corr-z9 | 24 | 20 | 15 | 7 | 10 | 4 |
| color-z0 | 0 | 0 | 0 | 0 | 0 | 0 |
| color-z9 | 0 | 0 | 0 | 0 | 0 | 0 |
| noise-z0 | 5 | 3 | 1 | 0 | 4 | 4 |
| noise-z9 | 7 | 7 | 6 | 4 | 2 | 2 |
| repo-vp8l-corpus | 193 | 187 | 181 | 117 | 92 | 30 |
| issue119 | 0 | 0 | 0 | 0 | 0 | 0 |
