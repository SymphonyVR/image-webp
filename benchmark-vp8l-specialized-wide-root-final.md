# VP8L adaptive Huffman root matrix

- base: `4cd194935d100a09acf24eb24d8c1343c7844844`
- CPU: `AMD EPYC 7763 64-Core Processor`
- 11 alternating/reversed paired rounds; hashes/tests/MSRV passed
- `dyn9` measures the cost of storing/reading a per-tree root width while always selecting 9 bits.

| workload | variant | median us | speedup vs r9 | positive rounds |
|---|---|---:|---:|---:|
| corpus | r9 | 1567.234 | 1.0000x | 0/11 |
| corpus | n256q8w10 | 1653.641 | 0.9480x | 0/11 |
| corpus | n256q8w11 | 1650.412 | 0.9483x | 0/11 |
| corpus | n256q4w10 | 1655.396 | 0.9464x | 0/11 |
| corpus | n256q4w11 | 1652.056 | 0.9475x | 0/11 |
| corpus | n192q8w10 | 1652.637 | 0.9483x | 0/11 |
| corpus | n192q8w11 | 1653.150 | 0.9497x | 0/11 |
| z0 | r9 | 32720.176 | 1.0000x | 0/11 |
| z0 | n256q8w10 | 33925.589 | 0.9640x | 0/11 |
| z0 | n256q8w11 | 33885.837 | 0.9660x | 0/11 |
| z0 | n256q4w10 | 33951.499 | 0.9640x | 0/11 |
| z0 | n256q4w11 | 33952.115 | 0.9636x | 0/11 |
| z0 | n192q8w10 | 33908.340 | 0.9654x | 0/11 |
| z0 | n192q8w11 | 33863.413 | 0.9662x | 0/11 |
| z9 | r9 | 31396.410 | 1.0000x | 0/11 |
| z9 | n256q8w10 | 29929.342 | 1.0489x | 11/11 |
| z9 | n256q8w11 | 29464.253 | 1.0655x | 11/11 |
| z9 | n256q4w10 | 30318.322 | 1.0351x | 11/11 |
| z9 | n256q4w11 | 29731.603 | 1.0563x | 11/11 |
| z9 | n192q8w10 | 29883.514 | 1.0486x | 11/11 |
| z9 | n192q8w11 | 29468.695 | 1.0642x | 11/11 |
| noise-z0 | r9 | 55486.278 | 1.0000x | 0/11 |
| noise-z0 | n256q8w10 | 60271.828 | 0.9197x | 0/11 |
| noise-z0 | n256q8w11 | 60198.854 | 0.9196x | 0/11 |
| noise-z0 | n256q4w10 | 60817.246 | 0.9147x | 0/11 |
| noise-z0 | n256q4w11 | 60626.041 | 0.9198x | 0/11 |
| noise-z0 | n192q8w10 | 60400.629 | 0.9246x | 0/11 |
| noise-z0 | n192q8w11 | 60407.597 | 0.9219x | 0/11 |
| noise-z9 | r9 | 65489.054 | 1.0000x | 0/11 |
| noise-z9 | n256q8w10 | 56186.533 | 1.1661x | 11/11 |
| noise-z9 | n256q8w11 | 53918.067 | 1.2143x | 11/11 |
| noise-z9 | n256q4w10 | 57776.949 | 1.1372x | 11/11 |
| noise-z9 | n256q4w11 | 55306.739 | 1.1815x | 11/11 |
| noise-z9 | n192q8w10 | 56137.576 | 1.1696x | 11/11 |
| noise-z9 | n192q8w11 | 53891.558 | 1.2179x | 11/11 |
| corr-z9 | r9 | 31666.771 | 1.0000x | 0/11 |
| corr-z9 | n256q8w10 | 33075.306 | 0.9561x | 0/11 |
| corr-z9 | n256q8w11 | 33056.639 | 0.9566x | 0/11 |
| corr-z9 | n256q4w10 | 33072.472 | 0.9573x | 0/11 |
| corr-z9 | n256q4w11 | 33003.635 | 0.9583x | 0/11 |
| corr-z9 | n192q8w10 | 33005.483 | 0.9567x | 0/11 |
| corr-z9 | n192q8w11 | 32978.736 | 0.9590x | 0/11 |
| structured-z9 | r9 | 19161.743 | 1.0000x | 0/11 |
| structured-z9 | n256q8w10 | 19680.887 | 0.9745x | 0/11 |
| structured-z9 | n256q8w11 | 19726.977 | 0.9718x | 0/11 |
| structured-z9 | n256q4w10 | 19655.898 | 0.9719x | 0/11 |
| structured-z9 | n256q4w11 | 19712.248 | 0.9707x | 0/11 |
| structured-z9 | n192q8w10 | 19672.078 | 0.9735x | 0/11 |
| structured-z9 | n192q8w11 | 19724.544 | 0.9694x | 0/11 |

## Selectors

- `r9`: `unmodified static 9`
- `n256q8w10`: `10|num_symbols >= 256 && long_symbols * 8 >= num_symbols`
- `n256q8w11`: `11|num_symbols >= 256 && long_symbols * 8 >= num_symbols`
- `n256q4w10`: `10|num_symbols >= 256 && long_symbols * 4 >= num_symbols`
- `n256q4w11`: `11|num_symbols >= 256 && long_symbols * 4 >= num_symbols`
- `n192q8w10`: `10|num_symbols >= 192 && long_symbols * 8 >= num_symbols`
- `n192q8w11`: `11|num_symbols >= 192 && long_symbols * 8 >= num_symbols`
