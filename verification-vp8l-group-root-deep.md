# Deep VP8L group-static root differential verification

- composed base: `4cd194935d100a09acf24eb24d8c1343c7844844`
- candidate: base materialized with group-static 9/11-bit Huffman roots
- total streams: **502**
- generated streams: **492**
- hard oracle: candidate Rust decoder output must equal libwebp `dwebp` byte-for-byte
- generated fidelity: `cwebp -lossless -exact` output must round-trip to original RGBA bytes
- coverage: tiny/odd/power-of-two boundaries through 513px; palette/correlated/anti-correlated/stripes/tiles/noise; opaque/binary/gradient/sparse/noisy alpha; z0/z3/z6/z9

- Rust vs libwebp mismatches: **0**
- generated source-fidelity mismatches: **0**

## Sample records

| stream | size | bytes | sha256 prefix | oracle | source |
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
| gen/1x1/corr/gradient/z0 | 1x1 | 4 | `df3f619804a92fdb` | True | True |
| gen/1x1/corr/gradient/z3 | 1x1 | 4 | `df3f619804a92fdb` | True | True |
| gen/1x1/corr/gradient/z6 | 1x1 | 4 | `df3f619804a92fdb` | True | True |
| gen/1x1/corr/gradient/z9 | 1x1 | 4 | `df3f619804a92fdb` | True | True |
| gen/1x7/gradient/binary/z0 | 1x7 | 28 | `453f81e10ccf4c06` | True | True |
| gen/1x7/gradient/binary/z3 | 1x7 | 28 | `453f81e10ccf4c06` | True | True |
| gen/1x7/gradient/binary/z6 | 1x7 | 28 | `453f81e10ccf4c06` | True | True |
| gen/1x7/gradient/binary/z9 | 1x7 | 28 | `453f81e10ccf4c06` | True | True |
| gen/1x7/anticorr/sparse/z0 | 1x7 | 28 | `52ae84322d9eaa4d` | True | True |
| gen/1x7/anticorr/sparse/z3 | 1x7 | 28 | `52ae84322d9eaa4d` | True | True |
| gen/1x7/anticorr/sparse/z6 | 1x7 | 28 | `52ae84322d9eaa4d` | True | True |
| gen/1x7/anticorr/sparse/z9 | 1x7 | 28 | `52ae84322d9eaa4d` | True | True |
| gen/2x2/checker/gradient/z0 | 2x2 | 16 | `73b81760a370a2b1` | True | True |
| gen/2x2/checker/gradient/z3 | 2x2 | 16 | `73b81760a370a2b1` | True | True |
| gen/2x2/checker/gradient/z6 | 2x2 | 16 | `73b81760a370a2b1` | True | True |
| gen/2x2/checker/gradient/z9 | 2x2 | 16 | `73b81760a370a2b1` | True | True |
| gen/2x2/stripes/noise/z0 | 2x2 | 16 | `dcfdcf2123d2e22e` | True | True |
| gen/2x2/stripes/noise/z3 | 2x2 | 16 | `dcfdcf2123d2e22e` | True | True |
| gen/2x2/stripes/noise/z6 | 2x2 | 16 | `dcfdcf2123d2e22e` | True | True |
| gen/2x2/stripes/noise/z9 | 2x2 | 16 | `dcfdcf2123d2e22e` | True | True |
| gen/3x5/palette/sparse/z0 | 3x5 | 60 | `be5e811761aa5d5c` | True | True |
| gen/3x5/palette/sparse/z3 | 3x5 | 60 | `be5e811761aa5d5c` | True | True |
| gen/3x5/palette/sparse/z6 | 3x5 | 60 | `be5e811761aa5d5c` | True | True |
| gen/3x5/palette/sparse/z9 | 3x5 | 60 | `be5e811761aa5d5c` | True | True |
| gen/3x5/tiles/None/z0 | 3x5 | 60 | `384f38c1bd256b27` | True | True |
| gen/3x5/tiles/None/z3 | 3x5 | 60 | `384f38c1bd256b27` | True | True |
| gen/3x5/tiles/None/z6 | 3x5 | 60 | `384f38c1bd256b27` | True | True |
| gen/3x5/tiles/None/z9 | 3x5 | 60 | `384f38c1bd256b27` | True | True |
| gen/4x4/corr/noise/z0 | 4x4 | 64 | `c4111546edac44f4` | True | True |
| gen/4x4/corr/noise/z3 | 4x4 | 64 | `c4111546edac44f4` | True | True |
| gen/4x4/corr/noise/z6 | 4x4 | 64 | `c4111546edac44f4` | True | True |
| gen/4x4/corr/noise/z9 | 4x4 | 64 | `c4111546edac44f4` | True | True |
| gen/4x4/noise/binary/z0 | 4x4 | 64 | `a021fc0e630a1a87` | True | True |
| gen/4x4/noise/binary/z3 | 4x4 | 64 | `a021fc0e630a1a87` | True | True |
| gen/4x4/noise/binary/z6 | 4x4 | 64 | `a021fc0e630a1a87` | True | True |
| gen/4x4/noise/binary/z9 | 4x4 | 64 | `a021fc0e630a1a87` | True | True |
| gen/7x3/anticorr/None/z0 | 7x3 | 84 | `9a781fc035080d72` | True | True |
| gen/7x3/anticorr/None/z3 | 7x3 | 84 | `9a781fc035080d72` | True | True |
| gen/7x3/anticorr/None/z6 | 7x3 | 84 | `9a781fc035080d72` | True | True |
| gen/7x3/anticorr/None/z9 | 7x3 | 84 | `9a781fc035080d72` | True | True |
| gen/7x3/solid/gradient/z0 | 7x3 | 84 | `4c4e5467079de1e8` | True | True |
| gen/7x3/solid/gradient/z3 | 7x3 | 84 | `4c4e5467079de1e8` | True | True |
| gen/7x3/solid/gradient/z6 | 7x3 | 84 | `4c4e5467079de1e8` | True | True |
| gen/7x3/solid/gradient/z9 | 7x3 | 84 | `4c4e5467079de1e8` | True | True |
| gen/15x17/stripes/binary/z0 | 15x17 | 1020 | `a542a00811a72b06` | True | True |
| gen/15x17/stripes/binary/z3 | 15x17 | 1020 | `a542a00811a72b06` | True | True |
