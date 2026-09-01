# VP8L historical regression diagnosis

- CPU: `AMD EPYC 7763 64-Core Processor`
- release, `-C target-cpu=native`, CPU 0 pinned
- 17 alternating/reversed milestone rounds per workload

## Milestones

- `main`: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- `root9`: `fc8b701a3cba33887e47768c7b1e5e6a44de239d`
- `predictor1`: `00c9bf309f8286509832948a67d4fbcdb2933adc`
- `cache_tail`: `a062200e32527c73b4a4e5a3de0f087f61b64337`
- `single_group`: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- `final`: `4cd194935d100a09acf24eb24d8c1343c7844844`

- generated/issue output mismatches vs validated final: **0**

## Runtime medians

| workload | main | root9 | predictor1 | cache_tail | single_group | final | final/main |
|---|---:|---:|---:|---:|---:|---:|---:|
| structured-z0 | 45836.881 | 45813.294 | 45748.938 | 45924.369 | 46107.851 | 45831.875 | 1.0001x |
| structured-z9 | 34797.103 | 34822.104 | 34781.267 | 34591.146 | 34834.235 | 32205.050 | 1.0805x |
| gradient-z0 | 45573.214 | 45620.918 | 45583.458 | 45728.228 | 45915.946 | 45656.503 | 0.9982x |
| gradient-z9 | 47347.737 | 47357.664 | 47348.660 | 47498.399 | 47656.086 | 45064.567 | 1.0507x |
| corr-z0 | 59479.387 | 59623.554 | 59325.055 | 59359.755 | 58770.266 | 58585.481 | 1.0153x |
| corr-z9 | 62882.791 | 62773.802 | 62534.179 | 60970.069 | 60636.361 | 58031.449 | 1.0836x |
| color-z0 | 45585.814 | 45620.598 | 45586.499 | 45714.517 | 45875.829 | 45639.717 | 0.9988x |
| color-z9 | 30555.182 | 30686.646 | 30661.551 | 30512.796 | 30524.231 | 28127.656 | 1.0863x |
| noise-z0 | 93327.899 | 95117.146 | 97017.829 | 95010.281 | 94781.266 | 98951.542 | 0.9432x |
| noise-z9 | 88565.399 | 119832.751 | 119710.980 | 119410.044 | 116395.997 | 115651.274 | 0.7658x |
| repo-vp8l-corpus | 1670.987 | 1660.003 | 1647.238 | 1627.318 | 1597.352 | 1554.457 | 1.0750x |
| issue119 | 24729.563 | 22876.693 | 22900.763 | 22561.831 | 22857.518 | 22899.469 | 1.0799x |

## Step ratios (previous/current; >1 faster)

| workload | main→root9 | root9→predictor1 | predictor1→cache-tail | cache-tail→single-group | single-group→final |
|---|---:|---:|---:|---:|---:|
| structured-z0 | 1.0005x | 1.0014x | 0.9962x | 0.9960x | 1.0060x |
| structured-z9 | 0.9993x | 1.0012x | 1.0055x | 0.9930x | 1.0816x |
| gradient-z0 | 0.9990x | 1.0008x | 0.9968x | 0.9959x | 1.0057x |
| gradient-z9 | 0.9998x | 1.0002x | 0.9968x | 0.9967x | 1.0575x |
| corr-z0 | 0.9976x | 1.0050x | 0.9994x | 1.0100x | 1.0032x |
| corr-z9 | 1.0017x | 1.0038x | 1.0257x | 1.0055x | 1.0449x |
| color-z0 | 0.9992x | 1.0007x | 0.9972x | 0.9965x | 1.0052x |
| color-z9 | 0.9957x | 1.0008x | 1.0049x | 0.9996x | 1.0852x |
| noise-z0 | 0.9812x | 0.9804x | 1.0211x | 1.0024x | 0.9579x |
| noise-z9 | 0.7391x | 1.0010x | 1.0025x | 1.0259x | 1.0064x |
| repo-vp8l-corpus | 1.0066x | 1.0077x | 1.0122x | 1.0188x | 1.0276x |
| issue119 | 1.0810x | 0.9989x | 1.0150x | 0.9871x | 0.9982x |
