# VP8L direct predictors on composed-v3

- baseline: `4cd194935d100a09acf24eb24d8c1343c7844844`
- candidate: `7eeb7200cbee067f2ee66deb708e47be2037314f`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- candidate adds only packed direct-neighbor predictor modes 2–4 to composed color+meta tree
- hashes match; tests/docs/Clippy/fmt/MSRV build pass
- aggregate: 25 alternating paired rounds; per-file: 17 rounds

## Aggregate

| workload | base us | candidate us | paired median | positive | range |
|---|---:|---:|---:|---:|---:|
| repo-corpus | 1070.467 | 1040.486 | 1.0297x | 25/25 | 1.0057–1.0506x |
| stripes-all-z | 5898.269 | 4942.281 | 1.1934x | 25/25 | 1.1884–1.1997x |
| tiles-all-z | 8213.066 | 7745.623 | 1.0604x | 25/25 | 1.0267–1.0647x |
| generated-z9 | 14424.721 | 13860.325 | 1.0404x | 25/25 | 1.0310–1.0854x |

## Per-file

| file | base us | candidate us | paired median | positive | range |
|---|---:|---:|---:|---:|---:|
| repo/1_webp_ll.webp | 1559.772 | 1529.598 | 1.0171x | 17/17 | 1.0002–1.0281x |
| repo/2_webp_ll.webp | 1306.012 | 1229.618 | 1.0640x | 17/17 | 1.0429–1.0909x |
| repo/3_webp_ll.webp | 4408.679 | 4348.349 | 1.0139x | 17/17 | 1.0051–1.0223x |
| repo/4_webp_ll.webp | 675.130 | 610.768 | 1.1020x | 17/17 | 1.0846–1.1207x |
| repo/5_webp_ll.webp | 1830.831 | 1726.691 | 1.0607x | 17/17 | 1.0340–1.0631x |
| repo/color_index.webp | 8.883 | 8.657 | 1.0261x | 17/17 | 1.0053–1.0586x |
| repo/lossless_indexed_1bit_palette.webp | 35.213 | 35.241 | 0.9999x | 8/17 | 0.9792–1.0098x |
| repo/lossless_indexed_2bit_palette.webp | 42.240 | 42.246 | 0.9996x | 8/17 | 0.9894–1.0204x |
| repo/lossless_indexed_4bit_palette.webp | 631.750 | 639.648 | 0.9877x | 1/17 | 0.9763–1.0203x |
| repo/tiny.webp | 7.672 | 7.746 | 0.9899x | 4/17 | 0.9329–1.0184x |
| gen/gradient-z0 | 12287.932 | 12294.210 | 1.0006x | 9/17 | 0.9759–1.0127x |
| gen/gradient-z3 | 12879.923 | 12879.903 | 0.9997x | 8/17 | 0.9764–1.0185x |
| gen/gradient-z6 | 12950.763 | 12943.837 | 0.9997x | 7/17 | 0.9744–1.1734x |
| gen/gradient-z9 | 13173.098 | 13170.719 | 1.0005x | 10/17 | 0.9079–1.0121x |
| gen/corr-z0 | 16575.382 | 16632.569 | 0.9966x | 2/17 | 0.9707–1.0096x |
| gen/corr-z3 | 14085.822 | 14080.131 | 0.9982x | 7/17 | 0.9748–1.0158x |
| gen/corr-z6 | 13377.237 | 13367.052 | 1.0027x | 13/17 | 0.9720–1.0196x |
| gen/corr-z9 | 14697.466 | 14414.562 | 1.0201x | 15/17 | 0.9732–1.1005x |
| gen/stripes-z0 | 12339.043 | 12328.177 | 0.9980x | 7/17 | 0.9774–1.0216x |
| gen/stripes-z3 | 3022.063 | 2079.223 | 1.4543x | 17/17 | 1.4238–1.4874x |
| gen/stripes-z6 | 3027.910 | 2074.089 | 1.4611x | 17/17 | 1.4235–1.4949x |
| gen/stripes-z9 | 5894.259 | 3990.920 | 1.4758x | 17/17 | 1.4235–1.5030x |
| gen/tiles-z0 | 12275.056 | 12267.916 | 0.9997x | 8/17 | 0.9861–1.0214x |
| gen/tiles-z3 | 7337.354 | 7347.591 | 0.9988x | 5/17 | 0.9774–1.0200x |
| gen/tiles-z6 | 7288.081 | 7305.420 | 0.9969x | 4/17 | 0.9792–1.0165x |
| gen/tiles-z9 | 7015.917 | 5140.244 | 1.3649x | 17/17 | 1.3099–1.3888x |
| gen/smooth-z0 | 12214.472 | 12214.763 | 1.0001x | 9/17 | 0.9851–1.3023x |
| gen/smooth-z3 | 7167.614 | 7178.369 | 0.9999x | 8/17 | 0.9740–1.0172x |
| gen/smooth-z6 | 7245.570 | 7269.426 | 0.9986x | 5/17 | 0.9405–1.0166x |
| gen/smooth-z9 | 7553.800 | 7637.545 | 0.9985x | 8/17 | 0.9829–1.0144x |
| gen/noise-z0 | 32601.424 | 32844.540 | 0.9929x | 6/17 | 0.9752–1.0731x |
| gen/noise-z3 | 40056.447 | 40533.398 | 0.9887x | 1/17 | 0.9721–1.0863x |
| gen/noise-z6 | 40150.411 | 40630.422 | 0.9861x | 0/17 | 0.9649–0.9986x |
| gen/noise-z9 | 40380.937 | 40860.643 | 0.9892x | 2/17 | 0.9720–1.0096x |

## Breadth

- repository median: **1.0155x**, positive **6/10**
- generated median: **0.9997x**, positive **9/24**
- overall median: **0.9998x**, positive **15/34**
