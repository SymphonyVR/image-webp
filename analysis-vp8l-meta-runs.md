# VP8L meta-Huffman horizontal-run analysis

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`

| file | bits | groups | grid | cells | runs | same-right | dispatch reduction |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1_webp_ll.webp | 3 | 8 | 50x38 | 1900 | 568 | 1332 | 70.1% |
| 2_webp_ll.webp | 3 | 9 | 49x50 | 2450 | 468 | 1982 | 80.9% |
| 3_webp_ll.webp | 4 | 36 | 50x38 | 1900 | 554 | 1346 | 70.8% |
| 4_webp_ll.webp | 3 | 5 | 53x21 | 1113 | 234 | 879 | 79.0% |
| 5_webp_ll.webp | 3 | 11 | 38x38 | 1444 | 607 | 837 | 58.0% |
| color_index.webp | 0 | 1 | 1x1 | 0 | 0 | 0 | 0.0% |
| lossless_indexed_1bit_palette.webp | 0 | 1 | 1x1 | 0 | 0 | 0 | 0.0% |
| lossless_indexed_2bit_palette.webp | 0 | 1 | 1x1 | 0 | 0 | 0 | 0.0% |
| lossless_indexed_4bit_palette.webp | 3 | 2 | 32x38 | 1216 | 534 | 682 | 56.1% |
| tiny.webp | 0 | 1 | 1x1 | 0 | 0 | 0 | 0.0% |
| structured.webp | 6 | 15 | 32x24 | 768 | 427 | 341 | 44.4% |
| tiles.webp | 6 | 2 | 32x24 | 768 | 89 | 679 | 88.4% |
| noise.webp | 6 | 2 | 32x24 | 768 | 48 | 720 | 93.8% |
