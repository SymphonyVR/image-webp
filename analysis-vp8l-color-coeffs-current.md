# VP8L color coefficient sparsity

- baseline: `4f322d44fb38747659451db3d7f1dac7ff8ff21f`
- transform pixels observed: 911493
- red→blue zero: 727669/911493 (79.8%)
- green→blue zero: 752845/911493 (82.6%)
- green→red zero: 654005/911493 (71.8%)
- all three zero: 584461/911493 (64.1%)

| file | pixels | rtb=0 | gtb=0 | gtr=0 | all=0 |
|---|---:|---:|---:|---:|---:|
| tests/images/gallery2/1_webp_ll.webp | 120400 | 83840 | 90456 | 87296 | 62680 |
| tests/images/gallery2/2_webp_ll.webp | 152470 | 147606 | 140246 | 136470 | 133398 |
| tests/images/gallery2/3_webp_ll.webp | 480000 | 385280 | 407040 | 327168 | 308224 |
| tests/images/gallery2/4_webp_ll.webp | 68623 | 54927 | 46607 | 51599 | 43855 |
| tests/images/gallery2/5_webp_ll.webp | 90000 | 56016 | 68496 | 51472 | 36304 |
