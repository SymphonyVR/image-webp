# VP8L adaptive Huffman root matrix

- base: `4cd194935d100a09acf24eb24d8c1343c7844844`
- CPU: `AMD EPYC 7763 64-Core Processor`
- 11 alternating/reversed paired rounds; hashes/tests/MSRV passed
- `dyn9` measures the cost of storing/reading a per-tree root width while always selecting 9 bits.

| workload | variant | median us | speedup vs r9 | positive rounds |
|---|---|---:|---:|---:|
| corpus | r9 | 1563.240 | 1.0000x | 0/11 |
| corpus | dyn9 | 1573.312 | 0.9939x | 0/11 |
| corpus | n256q8r10 | 1566.827 | 0.9951x | 3/11 |
| corpus | n256q8r11 | 1568.263 | 0.9960x | 4/11 |
| corpus | n256q4r10 | 1571.772 | 0.9937x | 1/11 |
| corpus | n256q4r11 | 1574.591 | 0.9922x | 0/11 |
| corpus | n192q8r10 | 1567.443 | 0.9976x | 5/11 |
| corpus | n192q8r11 | 1565.279 | 0.9985x | 3/11 |
| z0 | r9 | 32612.980 | 1.0000x | 0/11 |
| z0 | dyn9 | 32346.292 | 1.0093x | 10/11 |
| z0 | n256q8r10 | 32219.459 | 1.0125x | 11/11 |
| z0 | n256q8r11 | 32185.191 | 1.0134x | 11/11 |
| z0 | n256q4r10 | 32338.310 | 1.0108x | 10/11 |
| z0 | n256q4r11 | 32241.155 | 1.0125x | 9/11 |
| z0 | n192q8r10 | 32235.227 | 1.0105x | 10/11 |
| z0 | n192q8r11 | 32451.587 | 1.0050x | 8/11 |
| z9 | r9 | 30956.292 | 1.0000x | 0/11 |
| z9 | dyn9 | 31259.382 | 0.9897x | 0/11 |
| z9 | n256q8r10 | 28074.094 | 1.1010x | 11/11 |
| z9 | n256q8r11 | 27725.769 | 1.1167x | 11/11 |
| z9 | n256q4r10 | 28374.061 | 1.0905x | 11/11 |
| z9 | n256q4r11 | 27892.610 | 1.1101x | 11/11 |
| z9 | n192q8r10 | 28068.553 | 1.0998x | 11/11 |
| z9 | n192q8r11 | 27745.475 | 1.1157x | 11/11 |
| noise-z0 | r9 | 55617.571 | 1.0000x | 0/11 |
| noise-z0 | dyn9 | 54682.497 | 1.0174x | 11/11 |
| noise-z0 | n256q8r10 | 53568.279 | 1.0305x | 11/11 |
| noise-z0 | n256q8r11 | 53958.937 | 1.0280x | 11/11 |
| noise-z0 | n256q4r10 | 54304.435 | 1.0267x | 10/11 |
| noise-z0 | n256q4r11 | 53961.161 | 1.0243x | 11/11 |
| noise-z0 | n192q8r10 | 53677.147 | 1.0295x | 11/11 |
| noise-z0 | n192q8r11 | 53686.050 | 1.0323x | 11/11 |
| noise-z9 | r9 | 65490.386 | 1.0000x | 0/11 |
| noise-z9 | dyn9 | 65657.780 | 0.9980x | 2/11 |
| noise-z9 | n256q8r10 | 49068.915 | 1.3366x | 11/11 |
| noise-z9 | n256q8r11 | 47287.237 | 1.3785x | 11/11 |
| noise-z9 | n256q4r10 | 51176.881 | 1.2797x | 11/11 |
| noise-z9 | n256q4r11 | 49018.820 | 1.3412x | 11/11 |
| noise-z9 | n192q8r10 | 49135.156 | 1.3239x | 11/11 |
| noise-z9 | n192q8r11 | 47718.204 | 1.3729x | 11/11 |
| corr-z9 | r9 | 31228.991 | 1.0000x | 0/11 |
| corr-z9 | dyn9 | 31622.934 | 0.9915x | 0/11 |
| corr-z9 | n256q8r10 | 31517.380 | 0.9915x | 1/11 |
| corr-z9 | n256q8r11 | 31576.679 | 0.9919x | 1/11 |
| corr-z9 | n256q4r10 | 31565.542 | 0.9886x | 1/11 |
| corr-z9 | n256q4r11 | 31644.982 | 0.9916x | 0/11 |
| corr-z9 | n192q8r10 | 31551.674 | 0.9940x | 0/11 |
| corr-z9 | n192q8r11 | 31583.431 | 0.9922x | 1/11 |
| structured-z9 | r9 | 18883.593 | 1.0000x | 0/11 |
| structured-z9 | dyn9 | 18960.571 | 0.9937x | 0/11 |
| structured-z9 | n256q8r10 | 19060.007 | 0.9925x | 0/11 |
| structured-z9 | n256q8r11 | 18954.899 | 0.9966x | 4/11 |
| structured-z9 | n256q4r10 | 19114.713 | 0.9917x | 1/11 |
| structured-z9 | n256q4r11 | 18944.990 | 0.9939x | 4/11 |
| structured-z9 | n192q8r10 | 18979.576 | 0.9951x | 2/11 |
| structured-z9 | n192q8r11 | 18996.288 | 0.9932x | 3/11 |

## Selectors

- `r9`: `unmodified static 9`
- `dyn9`: `9u8`
- `n256q8r10`: `if num_symbols >= 256 && long_symbols * 8 >= num_symbols { 10 } else { 9 }`
- `n256q8r11`: `if num_symbols >= 256 && long_symbols * 8 >= num_symbols { 11 } else { 9 }`
- `n256q4r10`: `if num_symbols >= 256 && long_symbols * 4 >= num_symbols { 10 } else { 9 }`
- `n256q4r11`: `if num_symbols >= 256 && long_symbols * 4 >= num_symbols { 11 } else { 9 }`
- `n192q8r10`: `if num_symbols >= 192 && long_symbols * 8 >= num_symbols { 10 } else { 9 }`
- `n192q8r11`: `if num_symbols >= 192 && long_symbols * 8 >= num_symbols { 11 } else { 9 }`
