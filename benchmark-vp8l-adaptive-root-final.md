# VP8L adaptive Huffman root matrix

- base: `4cd194935d100a09acf24eb24d8c1343c7844844`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- 11 alternating/reversed paired rounds; hashes/tests/MSRV passed
- `dyn9` measures the cost of storing/reading a per-tree root width while always selecting 9 bits.

| workload | variant | median us | speedup vs r9 | positive rounds |
|---|---|---:|---:|---:|
| corpus | r9 | 1665.030 | 1.0000x | 0/11 |
| corpus | dyn9 | 1683.345 | 0.9894x | 1/11 |
| corpus | m15r11 | 1673.162 | 0.9956x | 1/11 |
| corpus | m14r11 | 1690.736 | 0.9840x | 0/11 |
| corpus | m13r11 | 1699.330 | 0.9805x | 0/11 |
| corpus | m14r10 | 1687.140 | 0.9888x | 0/11 |
| corpus | q25r11 | 1674.806 | 0.9944x | 1/11 |
| corpus | q50r11 | 1674.752 | 0.9942x | 1/11 |
| z0 | r9 | 35242.129 | 1.0000x | 0/11 |
| z0 | dyn9 | 35340.463 | 0.9972x | 2/11 |
| z0 | m15r11 | 35323.418 | 0.9980x | 3/11 |
| z0 | m14r11 | 35228.583 | 1.0001x | 6/11 |
| z0 | m13r11 | 35255.951 | 0.9988x | 2/11 |
| z0 | m14r10 | 35244.185 | 0.9997x | 5/11 |
| z0 | q25r11 | 35247.783 | 0.9995x | 3/11 |
| z0 | q50r11 | 35329.280 | 0.9975x | 2/11 |
| z9 | r9 | 34047.896 | 1.0000x | 0/11 |
| z9 | dyn9 | 34415.051 | 0.9889x | 1/11 |
| z9 | m15r11 | 34247.734 | 0.9933x | 1/11 |
| z9 | m14r11 | 34406.242 | 0.9889x | 1/11 |
| z9 | m13r11 | 34252.283 | 0.9934x | 1/11 |
| z9 | m14r10 | 34370.390 | 0.9900x | 1/11 |
| z9 | q25r11 | 34214.979 | 0.9943x | 1/11 |
| z9 | q50r11 | 34211.479 | 0.9941x | 1/11 |
| noise-z0 | r9 | 58295.252 | 1.0000x | 0/11 |
| noise-z0 | dyn9 | 58578.397 | 0.9951x | 0/11 |
| noise-z0 | m15r11 | 58546.766 | 0.9961x | 0/11 |
| noise-z0 | m14r11 | 58041.827 | 1.0043x | 9/11 |
| noise-z0 | m13r11 | 58155.597 | 1.0033x | 9/11 |
| noise-z0 | m14r10 | 57965.620 | 1.0056x | 11/11 |
| noise-z0 | q25r11 | 58175.473 | 1.0020x | 8/11 |
| noise-z0 | q50r11 | 58590.134 | 0.9946x | 0/11 |
| noise-z9 | r9 | 71341.023 | 1.0000x | 0/11 |
| noise-z9 | dyn9 | 72185.566 | 0.9883x | 0/11 |
| noise-z9 | m15r11 | 72238.311 | 0.9873x | 0/11 |
| noise-z9 | m14r11 | 72209.880 | 0.9887x | 0/11 |
| noise-z9 | m13r11 | 72129.949 | 0.9895x | 0/11 |
| noise-z9 | m14r10 | 72137.545 | 0.9896x | 0/11 |
| noise-z9 | q25r11 | 72258.774 | 0.9878x | 0/11 |
| noise-z9 | q50r11 | 72257.888 | 0.9876x | 0/11 |
| corr-z9 | r9 | 34709.188 | 1.0000x | 0/11 |
| corr-z9 | dyn9 | 35067.892 | 0.9897x | 0/11 |
| corr-z9 | m15r11 | 35048.366 | 0.9910x | 0/11 |
| corr-z9 | m14r11 | 35308.341 | 0.9830x | 0/11 |
| corr-z9 | m13r11 | 35224.096 | 0.9853x | 0/11 |
| corr-z9 | m14r10 | 35133.099 | 0.9884x | 0/11 |
| corr-z9 | q25r11 | 34993.009 | 0.9930x | 0/11 |
| corr-z9 | q50r11 | 34927.717 | 0.9945x | 0/11 |
| structured-z9 | r9 | 20396.881 | 1.0000x | 0/11 |
| structured-z9 | dyn9 | 20390.275 | 0.9998x | 5/11 |
| structured-z9 | m15r11 | 20383.230 | 0.9999x | 5/11 |
| structured-z9 | m14r11 | 20432.213 | 0.9981x | 5/11 |
| structured-z9 | m13r11 | 20316.788 | 1.0041x | 10/11 |
| structured-z9 | m14r10 | 20376.974 | 0.9998x | 5/11 |
| structured-z9 | q25r11 | 20350.289 | 1.0018x | 9/11 |
| structured-z9 | q50r11 | 20334.183 | 1.0026x | 10/11 |

## Selectors

- `r9`: `unmodified static 9`
- `dyn9`: `9u8`
- `m15r11`: `if max_length >= 15 { 11 } else { 9 }`
- `m14r11`: `if max_length >= 14 { 11 } else { 9 }`
- `m13r11`: `if max_length >= 13 { 11 } else { 9 }`
- `m14r10`: `if max_length >= 14 { 10 } else { 9 }`
- `q25r11`: `if max_length >= 13 && num_symbols >= 128 && long_symbols * 4 >= num_symbols { 11 } else { 9 }`
- `q50r11`: `if max_length >= 13 && num_symbols >= 128 && long_symbols * 2 >= num_symbols { 11 } else { 9 }`
