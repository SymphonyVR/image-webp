# Deep VP8L libwebp differential verification

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- total streams: **282**
- generated streams: **272**
- oracle: libwebp `dwebp`; generated lossless files are additionally compared to original RGBA pixels
- generated coverage: tiny/odd/block-boundary dimensions, RGB/RGBA, binary/gradient/noisy alpha, solid/gradient/checker/palette/correlated/anti-correlated/stripes/noise, cwebp z0/z3/z6/z9

- mismatches: **187**

## Mismatches
- gen/1x7/gradient/binary/z0
- gen/1x7/gradient/binary/z3
- gen/1x7/gradient/binary/z6
- gen/1x7/gradient/binary/z9
- gen/2x2/checker/gradient/z0
- gen/2x2/checker/gradient/z3
- gen/2x2/checker/gradient/z6
- gen/2x2/checker/gradient/z9
- gen/2x2/anticorr/noise/z0
- gen/2x2/anticorr/noise/z3
- gen/2x2/anticorr/noise/z6
- gen/2x2/anticorr/noise/z9
- gen/7x3/noise/binary/z0
- gen/7x3/noise/binary/z3
- gen/7x3/noise/binary/z6
- gen/7x3/noise/binary/z9
- gen/15x17/anticorr/binary/z0
- gen/15x17/anticorr/binary/z3
- gen/15x17/anticorr/binary/z6
- gen/15x17/anticorr/binary/z9
- gen/15x17/solid/gradient/z0
- gen/15x17/solid/gradient/z3
- gen/15x17/solid/gradient/z6
- gen/15x17/solid/gradient/z9
- gen/16x16/stripes/gradient/z0
- gen/16x16/stripes/gradient/z3
- gen/16x16/stripes/gradient/z6
- gen/16x16/stripes/gradient/z9
- gen/17x15/noise/noise/z0
- gen/17x15/noise/noise/z3
- gen/17x15/noise/noise/z6
- gen/17x15/noise/noise/z9
- gen/31x33/palette/binary/z0
- gen/31x33/palette/binary/z3
- gen/31x33/palette/binary/z6
- gen/31x33/palette/binary/z9
- gen/32x32/gradient/binary/z0
- gen/32x32/gradient/binary/z3
- gen/32x32/gradient/binary/z6
- gen/32x32/gradient/binary/z9
- gen/32x32/corr/gradient/z0
- gen/32x32/corr/gradient/z3
- gen/32x32/corr/gradient/z6
- gen/32x32/corr/gradient/z9
- gen/33x31/checker/gradient/z0
- gen/33x31/checker/gradient/z3
- gen/33x31/checker/gradient/z6
- gen/33x31/checker/gradient/z9
- gen/33x31/anticorr/noise/z0
- gen/33x31/anticorr/noise/z3
- gen/33x31/anticorr/noise/z6
- gen/33x31/anticorr/noise/z9
- gen/63x65/palette/noise/z0
- gen/63x65/palette/noise/z3
- gen/63x65/palette/noise/z6
- gen/63x65/palette/noise/z9
- gen/64x64/noise/binary/z0
- gen/64x64/noise/binary/z3
- gen/64x64/noise/binary/z6
- gen/64x64/noise/binary/z9
- gen/65x63/anticorr/binary/z0
- gen/65x63/anticorr/binary/z3
- gen/65x63/anticorr/binary/z6
- gen/65x63/anticorr/binary/z9
- gen/65x63/solid/gradient/z0
- gen/65x63/solid/gradient/z3
- gen/65x63/solid/gradient/z6
- gen/65x63/solid/gradient/z9
- gen/127x129/stripes/gradient/z0
- gen/127x129/stripes/gradient/z3
- gen/127x129/stripes/gradient/z6
- gen/127x129/stripes/gradient/z9
- gen/127x129/gradient/noise/z0
- gen/127x129/gradient/noise/z3
- gen/127x129/gradient/noise/z6
- gen/127x129/gradient/noise/z9
- gen/128x128/noise/noise/z0
- gen/128x128/noise/noise/z3
- gen/128x128/noise/noise/z6
- gen/128x128/noise/noise/z9
- gen/129x127/palette/binary/z0
- gen/129x127/palette/binary/z3
- gen/129x127/palette/binary/z6
- gen/129x127/palette/binary/z9
- gen/257x193/gradient/binary/z0
- gen/257x193/gradient/binary/z3
- gen/257x193/gradient/binary/z6
- gen/257x193/gradient/binary/z9
- gen/257x193/corr/gradient/z0
- gen/257x193/corr/gradient/z3
- gen/257x193/corr/gradient/z6
- gen/257x193/corr/gradient/z9
- gen/73x59/solid/binary/z0
- gen/73x59/solid/binary/z3
- gen/73x59/solid/binary/z6
- gen/73x59/solid/binary/z9
- gen/73x59/solid/gradient/z0
- gen/73x59/solid/gradient/z3
- gen/73x59/solid/gradient/z6
- gen/73x59/solid/gradient/z9
- gen/73x59/solid/noise/z0
- gen/73x59/solid/noise/z3
- gen/73x59/solid/noise/z6
- gen/73x59/solid/noise/z9
- gen/73x59/gradient/binary/z0
- gen/73x59/gradient/binary/z3
- gen/73x59/gradient/binary/z6
- gen/73x59/gradient/binary/z9
- gen/73x59/gradient/gradient/z0
- gen/73x59/gradient/gradient/z3
- gen/73x59/gradient/gradient/z6
- gen/73x59/gradient/gradient/z9
- gen/73x59/gradient/noise/z0
- gen/73x59/gradient/noise/z3
- gen/73x59/gradient/noise/z6
- gen/73x59/gradient/noise/z9
- gen/73x59/checker/binary/z0
- gen/73x59/checker/binary/z3
- gen/73x59/checker/binary/z6
- gen/73x59/checker/binary/z9
- gen/73x59/checker/gradient/z0
- gen/73x59/checker/gradient/z3
- gen/73x59/checker/gradient/z6
- gen/73x59/checker/gradient/z9
- gen/73x59/checker/noise/z0
- gen/73x59/checker/noise/z3
- gen/73x59/checker/noise/z6
- gen/73x59/checker/noise/z9
- gen/73x59/palette/binary/z0
- gen/73x59/palette/binary/z3
- gen/73x59/palette/binary/z6
- gen/73x59/palette/binary/z9
- gen/73x59/palette/gradient/z0
- gen/73x59/palette/gradient/z3
- gen/73x59/palette/gradient/z6
- gen/73x59/palette/gradient/z9
- gen/73x59/palette/noise/z0
- gen/73x59/palette/noise/z3
- gen/73x59/palette/noise/z6
- gen/73x59/palette/noise/z9
- gen/73x59/corr/binary/z0
- gen/73x59/corr/binary/z3
- gen/73x59/corr/binary/z6
- gen/73x59/corr/binary/z9
- gen/73x59/corr/gradient/z0
- gen/73x59/corr/gradient/z3
- gen/73x59/corr/gradient/z6
- gen/73x59/corr/gradient/z9
- gen/73x59/corr/noise/z0
- gen/73x59/corr/noise/z3
- gen/73x59/corr/noise/z6
- gen/73x59/corr/noise/z9
- gen/73x59/anticorr/binary/z0
- gen/73x59/anticorr/binary/z3
- gen/73x59/anticorr/binary/z6
- gen/73x59/anticorr/binary/z9
- gen/73x59/anticorr/gradient/z0
- gen/73x59/anticorr/gradient/z3
- gen/73x59/anticorr/gradient/z6
- gen/73x59/anticorr/gradient/z9
- gen/73x59/anticorr/noise/z0
- gen/73x59/anticorr/noise/z3
- gen/73x59/anticorr/noise/z6
- gen/73x59/anticorr/noise/z9
- gen/73x59/stripes/binary/z0
- gen/73x59/stripes/binary/z3
- gen/73x59/stripes/binary/z6
- gen/73x59/stripes/binary/z9
- gen/73x59/stripes/gradient/z0
- gen/73x59/stripes/gradient/z3
- gen/73x59/stripes/gradient/z6
- gen/73x59/stripes/gradient/z9
- gen/73x59/stripes/noise/z0
- gen/73x59/stripes/noise/z6
- gen/73x59/stripes/noise/z9
- gen/73x59/noise/binary/z0
- gen/73x59/noise/binary/z3
- gen/73x59/noise/binary/z6
- gen/73x59/noise/binary/z9
- gen/73x59/noise/gradient/z0
- gen/73x59/noise/gradient/z3
- gen/73x59/noise/gradient/z6
- gen/73x59/noise/gradient/z9
- gen/73x59/noise/noise/z0
- gen/73x59/noise/noise/z3
- gen/73x59/noise/noise/z6
- gen/73x59/noise/noise/z9

## Sample verification records

| stream | size | bytes | sha256 prefix | ok |
|---|---:|---:|---|---|
| repo/tests/images/gallery2/1_webp_ll.webp | 400x301 | 481600 | `d06797de8b764c39` | True |
| repo/tests/images/gallery2/2_webp_ll.webp | 386x395 | 609880 | `1d85e1ae043937b7` | True |
| repo/tests/images/gallery2/3_webp_ll.webp | 800x600 | 1920000 | `00ee223581bac147` | True |
| repo/tests/images/gallery2/4_webp_ll.webp | 421x163 | 274492 | `7a322a61cff113e4` | True |
| repo/tests/images/gallery2/5_webp_ll.webp | 300x300 | 360000 | `5dd0c5c1b186340a` | True |
| repo/tests/images/regression/color_index.webp | 30x30 | 3600 | `50dc7412a505fc4e` | True |
| repo/tests/images/regression/lossless_indexed_1bit_palette.webp | 230x128 | 117760 | `f894ae5c5497aa16` | True |
| repo/tests/images/regression/lossless_indexed_2bit_palette.webp | 230x128 | 117760 | `fec1ea2cdbd0d25e` | True |
| repo/tests/images/regression/lossless_indexed_4bit_palette.webp | 500x300 | 600000 | `7c997f4a8e868f84` | True |
| repo/tests/images/regression/tiny.webp | 10x7 | 280 | `96f34efd5f950714` | True |
| gen/1x1/solid/None/z0 | 1x1 | 4 | `f0806bf3dffb5dc3` | True |
| gen/1x1/solid/None/z3 | 1x1 | 4 | `f0806bf3dffb5dc3` | True |
| gen/1x1/solid/None/z6 | 1x1 | 4 | `f0806bf3dffb5dc3` | True |
| gen/1x1/solid/None/z9 | 1x1 | 4 | `f0806bf3dffb5dc3` | True |
| gen/1x1/palette/binary/z0 | 1x1 | 4 | `df3f619804a92fdb` | True |
| gen/1x1/palette/binary/z3 | 1x1 | 4 | `df3f619804a92fdb` | True |
| gen/1x1/palette/binary/z6 | 1x1 | 4 | `df3f619804a92fdb` | True |
| gen/1x1/palette/binary/z9 | 1x1 | 4 | `df3f619804a92fdb` | True |
| gen/1x7/gradient/binary/z0 | 1x7 | 28 | `4807f03aef8299b7` | False |
| gen/1x7/gradient/binary/z3 | 1x7 | 28 | `4807f03aef8299b7` | False |
| gen/1x7/gradient/binary/z6 | 1x7 | 28 | `4807f03aef8299b7` | False |
| gen/1x7/gradient/binary/z9 | 1x7 | 28 | `4807f03aef8299b7` | False |
| gen/1x7/corr/gradient/z0 | 1x7 | 28 | `d1094ad1d4756183` | True |
| gen/1x7/corr/gradient/z3 | 1x7 | 28 | `d1094ad1d4756183` | True |
| gen/1x7/corr/gradient/z6 | 1x7 | 28 | `d1094ad1d4756183` | True |
| gen/1x7/corr/gradient/z9 | 1x7 | 28 | `d1094ad1d4756183` | True |
| gen/2x2/checker/gradient/z0 | 2x2 | 16 | `f38aea534c8f5f4b` | False |
| gen/2x2/checker/gradient/z3 | 2x2 | 16 | `f38aea534c8f5f4b` | False |
| gen/2x2/checker/gradient/z6 | 2x2 | 16 | `f38aea534c8f5f4b` | False |
| gen/2x2/checker/gradient/z9 | 2x2 | 16 | `f38aea534c8f5f4b` | False |
