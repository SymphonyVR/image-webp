# VP8L meta-Huffman run-skip matrix

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- hashes + tests + Rust 1.80.1 pass
- 17 alternating paired rounds/file; ~50 ms target/sample

| file | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus/1_webp_ll.webp | scan | 1.0067x | 15/17 | 0.9964–1.0241x |
| corpus/1_webp_ll.webp | pre | 0.9736x | 0/17 | 0.8812–0.9813x |
| corpus/1_webp_ll.webp | pre_const | 0.9681x | 1/17 | 0.9330–1.0052x |
| corpus/2_webp_ll.webp | scan | 1.0355x | 17/17 | 1.0167–1.0413x |
| corpus/2_webp_ll.webp | pre | 1.0267x | 17/17 | 1.0176–1.0306x |
| corpus/2_webp_ll.webp | pre_const | 0.9964x | 5/17 | 0.9896–1.0028x |
| corpus/3_webp_ll.webp | scan | 1.0224x | 17/17 | 1.0144–1.0466x |
| corpus/3_webp_ll.webp | pre | 1.0108x | 15/17 | 0.9972–1.0364x |
| corpus/3_webp_ll.webp | pre_const | 0.9695x | 0/17 | 0.9101–0.9838x |
| corpus/4_webp_ll.webp | scan | 1.0242x | 17/17 | 1.0121–1.0315x |
| corpus/4_webp_ll.webp | pre | 0.9965x | 2/17 | 0.9783–1.0119x |
| corpus/4_webp_ll.webp | pre_const | 0.9832x | 2/17 | 0.9434–1.0232x |
| corpus/5_webp_ll.webp | scan | 1.0098x | 17/17 | 1.0057–1.0735x |
| corpus/5_webp_ll.webp | pre | 1.0080x | 14/17 | 0.9889–1.0225x |
| corpus/5_webp_ll.webp | pre_const | 0.9815x | 0/17 | 0.9643–0.9883x |
| corpus/color_index.webp | scan | 1.0342x | 17/17 | 1.0058–1.0920x |
| corpus/color_index.webp | pre | 1.0192x | 17/17 | 1.0013–1.0353x |
| corpus/color_index.webp | pre_const | 0.9636x | 0/17 | 0.6596–0.9819x |
| corpus/lossless_indexed_1bit_palette.webp | scan | 1.0173x | 17/17 | 1.0072–1.0230x |
| corpus/lossless_indexed_1bit_palette.webp | pre | 0.9995x | 7/17 | 0.9725–1.0357x |
| corpus/lossless_indexed_1bit_palette.webp | pre_const | 0.9743x | 0/17 | 0.9707–0.9889x |
| corpus/lossless_indexed_2bit_palette.webp | scan | 1.0092x | 16/17 | 0.9964–1.0550x |
| corpus/lossless_indexed_2bit_palette.webp | pre | 0.9946x | 2/17 | 0.9386–1.0056x |
| corpus/lossless_indexed_2bit_palette.webp | pre_const | 0.9738x | 0/17 | 0.9520–0.9886x |
| corpus/lossless_indexed_4bit_palette.webp | scan | 1.0210x | 17/17 | 1.0138–1.0332x |
| corpus/lossless_indexed_4bit_palette.webp | pre | 1.0355x | 17/17 | 1.0263–1.0487x |
| corpus/lossless_indexed_4bit_palette.webp | pre_const | 1.0197x | 16/17 | 0.9912–1.0320x |
| corpus/tiny.webp | scan | 1.0069x | 13/17 | 0.9846–1.0408x |
| corpus/tiny.webp | pre | 1.0030x | 12/17 | 0.9856–1.0520x |
| corpus/tiny.webp | pre_const | 0.9883x | 2/17 | 0.9704–1.0068x |
| gen/structured | scan | 1.1057x | 17/17 | 1.0721–1.1300x |
| gen/structured | pre | 1.0367x | 16/17 | 0.9848–1.0444x |
| gen/structured | pre_const | 0.9836x | 1/17 | 0.9748–1.0683x |
| gen/tiles | scan | 1.0149x | 17/17 | 1.0042–1.0336x |
| gen/tiles | pre | 1.0182x | 17/17 | 1.0119–1.0307x |
| gen/tiles | pre_const | 0.9742x | 0/17 | 0.9686–0.9810x |
| gen/noise | scan | 1.0177x | 17/17 | 1.0070–1.0559x |
| gen/noise | pre | 0.9848x | 0/17 | 0.9078–0.9966x |
| gen/noise | pre_const | 0.9781x | 0/17 | 0.9515–0.9862x |

## Aggregate

| set | candidate | median file ratio | files >1 |
|---|---|---:|---:|
| corpus | scan | 1.0191x | 10/10 |
| corpus | pre | 1.0055x | 6/10 |
| corpus | pre_const | 0.9779x | 1/10 |
| generated | scan | 1.0177x | 3/3 |
| generated | pre | 1.0182x | 2/3 |
| generated | pre_const | 0.9781x | 0/3 |
| all | scan | 1.0177x | 13/13 |
| all | pre | 1.0080x | 8/13 |
| all | pre_const | 0.9781x | 1/13 |
