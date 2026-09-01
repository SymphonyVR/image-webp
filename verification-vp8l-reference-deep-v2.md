# Deep VP8L libwebp differential verification v2

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- total streams: **282**
- generated streams: **272**
- generated streams use `cwebp -lossless -exact` at z0/z3/z6/z9
- hard oracle: Rust RGBA output must equal libwebp `dwebp` RGBA output byte-for-byte
- source fidelity: alpha must match; RGB must match wherever alpha != 0

## Result

- Rust vs libwebp mismatches: **0**
- generated-source semantic mismatches: **0**

## Sample records

| stream | size | bytes | sha256 prefix | libwebp | source |
|---|---:|---:|---|---|---|
| repo/tests/images/gallery2/1_webp_ll.webp | 400x301 | 481600 | `d06797de8b764c39` | True | True |
| repo/tests/images/gallery2/2_webp_ll.webp | 386x395 | 609880 | `1d85e1ae043937b7` | True | True |
| repo/tests/images/gallery2/3_webp_ll.webp | 800x600 | 1920000 | `00ee223581bac147` | True | True |
| repo/tests/images/gallery2/4_webp_ll.webp | 421x163 | 274492 | `7a322a61cff113e4` | True | True |
| repo/tests/images/gallery2/5_webp_ll.webp | 300x300 | 360000 | `5dd0c5c1b186340a` | True | True |
| repo/tests/images/regression/color_index.webp | 30x30 | 3600 | `50dc7412a505fc4e` | True | True |
| repo/tests/images/regression/lossless_indexed_1bit_palette.webp | 230x128 | 117760 | `f894ae5c5497aa16` | True | True |
| repo/tests/images/regression/lossless_indexed_2bit_palette.webp | 230x128 | 117760 | `fec1ea2cdbd0d25e` | True | True |
| repo/tests/images/regression/lossless_indexed_4bit_palette.webp | 500x300 | 600000 | `7c997f4a8e868f84` | True | True |
| repo/tests/images/regression/tiny.webp | 10x7 | 280 | `96f34efd5f950714` | True | True |
| gen/1x1/solid/None/z0 | 1x1 | 4 | `f0806bf3dffb5dc3` | True | True |
| gen/1x1/solid/None/z3 | 1x1 | 4 | `f0806bf3dffb5dc3` | True | True |
| gen/1x1/solid/None/z6 | 1x1 | 4 | `f0806bf3dffb5dc3` | True | True |
| gen/1x1/solid/None/z9 | 1x1 | 4 | `f0806bf3dffb5dc3` | True | True |
| gen/1x1/palette/binary/z0 | 1x1 | 4 | `df3f619804a92fdb` | True | True |
| gen/1x1/palette/binary/z3 | 1x1 | 4 | `df3f619804a92fdb` | True | True |
| gen/1x1/palette/binary/z6 | 1x1 | 4 | `df3f619804a92fdb` | True | True |
| gen/1x1/palette/binary/z9 | 1x1 | 4 | `df3f619804a92fdb` | True | True |
| gen/1x7/gradient/binary/z0 | 1x7 | 28 | `453f81e10ccf4c06` | True | True |
| gen/1x7/gradient/binary/z3 | 1x7 | 28 | `453f81e10ccf4c06` | True | True |
| gen/1x7/gradient/binary/z6 | 1x7 | 28 | `453f81e10ccf4c06` | True | True |
| gen/1x7/gradient/binary/z9 | 1x7 | 28 | `453f81e10ccf4c06` | True | True |
| gen/1x7/corr/gradient/z0 | 1x7 | 28 | `d1094ad1d4756183` | True | True |
| gen/1x7/corr/gradient/z3 | 1x7 | 28 | `d1094ad1d4756183` | True | True |
| gen/1x7/corr/gradient/z6 | 1x7 | 28 | `d1094ad1d4756183` | True | True |
| gen/1x7/corr/gradient/z9 | 1x7 | 28 | `d1094ad1d4756183` | True | True |
| gen/2x2/checker/gradient/z0 | 2x2 | 16 | `73b81760a370a2b1` | True | True |
| gen/2x2/checker/gradient/z3 | 2x2 | 16 | `73b81760a370a2b1` | True | True |
| gen/2x2/checker/gradient/z6 | 2x2 | 16 | `73b81760a370a2b1` | True | True |
| gen/2x2/checker/gradient/z9 | 2x2 | 16 | `73b81760a370a2b1` | True | True |
| gen/2x2/anticorr/noise/z0 | 2x2 | 16 | `17e42295ec179f98` | True | True |
| gen/2x2/anticorr/noise/z3 | 2x2 | 16 | `17e42295ec179f98` | True | True |
| gen/2x2/anticorr/noise/z6 | 2x2 | 16 | `17e42295ec179f98` | True | True |
| gen/2x2/anticorr/noise/z9 | 2x2 | 16 | `17e42295ec179f98` | True | True |
| gen/3x5/palette/noise/z0 | 3x5 | 60 | `8913a9380624d975` | True | True |
| gen/3x5/palette/noise/z3 | 3x5 | 60 | `8913a9380624d975` | True | True |
| gen/3x5/palette/noise/z6 | 3x5 | 60 | `8913a9380624d975` | True | True |
| gen/3x5/palette/noise/z9 | 3x5 | 60 | `8913a9380624d975` | True | True |
| gen/3x5/stripes/None/z0 | 3x5 | 60 | `d79d9f6940f32643` | True | True |
| gen/3x5/stripes/None/z3 | 3x5 | 60 | `d79d9f6940f32643` | True | True |
