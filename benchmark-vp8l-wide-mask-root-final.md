# VP8L adaptive Huffman root matrix

- base: `4cd194935d100a09acf24eb24d8c1343c7844844`
- CPU: `Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz`
- 11 alternating/reversed paired rounds; hashes/tests/MSRV passed
- `dyn9` measures the cost of storing/reading a per-tree root width while always selecting 9 bits.

| workload | variant | median us | speedup vs r9 | positive rounds |
|---|---|---:|---:|---:|
| corpus | r9 | 1622.725 | 1.0000x | 0/11 |
| corpus | n256q16w10 | 1669.493 | 0.9713x | 0/11 |
| corpus | n256q16w11 | 1671.769 | 0.9689x | 0/11 |
| corpus | n256q8w10 | 1669.490 | 0.9717x | 0/11 |
| corpus | n256q8w11 | 1669.088 | 0.9723x | 0/11 |
| corpus | n192q8w11 | 1672.895 | 0.9702x | 0/11 |
| z0 | r9 | 34100.069 | 1.0000x | 0/11 |
| z0 | n256q16w10 | 34270.047 | 0.9980x | 4/11 |
| z0 | n256q16w11 | 34240.419 | 0.9957x | 3/11 |
| z0 | n256q8w10 | 34233.616 | 0.9963x | 3/11 |
| z0 | n256q8w11 | 34240.944 | 0.9950x | 3/11 |
| z0 | n192q8w11 | 34180.428 | 0.9963x | 2/11 |
| z9 | r9 | 33805.015 | 1.0000x | 0/11 |
| z9 | n256q16w10 | 34660.981 | 0.9775x | 0/11 |
| z9 | n256q16w11 | 34254.969 | 0.9882x | 0/11 |
| z9 | n256q8w10 | 34709.194 | 0.9785x | 0/11 |
| z9 | n256q8w11 | 34272.086 | 0.9879x | 1/11 |
| z9 | n192q8w11 | 34244.961 | 0.9903x | 0/11 |
| noise-z0 | r9 | 59789.945 | 1.0000x | 0/11 |
| noise-z0 | n256q16w10 | 60534.268 | 0.9901x | 0/11 |
| noise-z0 | n256q16w11 | 60664.582 | 0.9848x | 0/11 |
| noise-z0 | n256q8w10 | 60646.892 | 0.9873x | 0/11 |
| noise-z0 | n256q8w11 | 60580.702 | 0.9868x | 0/11 |
| noise-z0 | n192q8w11 | 60879.135 | 0.9834x | 0/11 |
| noise-z9 | r9 | 71843.249 | 1.0000x | 0/11 |
| noise-z9 | n256q16w10 | 75055.197 | 0.9593x | 0/11 |
| noise-z9 | n256q16w11 | 73436.580 | 0.9797x | 0/11 |
| noise-z9 | n256q8w10 | 74873.645 | 0.9614x | 0/11 |
| noise-z9 | n256q8w11 | 73300.389 | 0.9817x | 0/11 |
| noise-z9 | n192q8w11 | 73411.933 | 0.9784x | 0/11 |
| corr-z9 | r9 | 34193.832 | 1.0000x | 0/11 |
| corr-z9 | n256q16w10 | 34281.735 | 0.9933x | 1/11 |
| corr-z9 | n256q16w11 | 34404.486 | 0.9948x | 2/11 |
| corr-z9 | n256q8w10 | 34577.756 | 0.9895x | 2/11 |
| corr-z9 | n256q8w11 | 34278.081 | 0.9958x | 3/11 |
| corr-z9 | n192q8w11 | 34223.415 | 0.9965x | 4/11 |
| structured-z9 | r9 | 22734.187 | 1.0000x | 0/11 |
| structured-z9 | n256q16w10 | 22643.632 | 1.0040x | 7/11 |
| structured-z9 | n256q16w11 | 22890.939 | 0.9901x | 4/11 |
| structured-z9 | n256q8w10 | 22770.250 | 0.9995x | 5/11 |
| structured-z9 | n256q8w11 | 22679.498 | 0.9997x | 5/11 |
| structured-z9 | n192q8w11 | 22643.019 | 0.9982x | 5/11 |

## Selectors

- `r9`: `unmodified static 9`
- `n256q16w10`: `10|num_symbols >= 256 && long_symbols * 16 >= num_symbols`
- `n256q16w11`: `11|num_symbols >= 256 && long_symbols * 16 >= num_symbols`
- `n256q8w10`: `10|num_symbols >= 256 && long_symbols * 8 >= num_symbols`
- `n256q8w11`: `11|num_symbols >= 256 && long_symbols * 8 >= num_symbols`
- `n192q8w11`: `11|num_symbols >= 192 && long_symbols * 8 >= num_symbols`
