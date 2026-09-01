# VP8L deep color-transform matrix

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- all decoded hashes match; candidates pass tests + Rust 1.80.1
- 13 alternating paired rounds per file; adaptive iterations target ~35 ms/sample

| file | candidate | base us | cand us | median | positive | range |
|---|---|---:|---:|---:|---:|---:|
| corpus/tests/images/gallery2/1_webp_ll.webp | packed_outer | 1598.041 | 1464.892 | 1.0857x | 13/13 | 1.0552–1.0975x |
| corpus/tests/images/gallery2/1_webp_ll.webp | packed_current | 1592.549 | 1437.513 | 1.1062x | 13/13 | 1.1003–1.1513x |
| corpus/tests/images/gallery2/1_webp_ll.webp | packed_inc | 1591.480 | 1472.009 | 1.0825x | 13/13 | 1.0703–1.0954x |
| corpus/tests/images/gallery2/1_webp_ll.webp | scalar_inc | 1594.483 | 1605.938 | 0.9943x | 2/13 | 0.9785–1.0067x |
| corpus/tests/images/gallery2/2_webp_ll.webp | packed_outer | 1472.584 | 1253.790 | 1.1765x | 13/13 | 1.1696–1.1841x |
| corpus/tests/images/gallery2/2_webp_ll.webp | packed_current | 1471.408 | 1269.699 | 1.1573x | 13/13 | 1.1421–1.1694x |
| corpus/tests/images/gallery2/2_webp_ll.webp | packed_inc | 1467.208 | 1276.546 | 1.1512x | 13/13 | 1.1398–1.1598x |
| corpus/tests/images/gallery2/2_webp_ll.webp | scalar_inc | 1473.368 | 1468.090 | 1.0044x | 9/13 | 0.9918–1.0099x |
| corpus/tests/images/gallery2/3_webp_ll.webp | packed_outer | 4610.712 | 4304.859 | 1.0702x | 13/13 | 1.0667–1.0875x |
| corpus/tests/images/gallery2/3_webp_ll.webp | packed_current | 4613.102 | 4242.666 | 1.0843x | 13/13 | 1.0303–1.1017x |
| corpus/tests/images/gallery2/3_webp_ll.webp | packed_inc | 4583.304 | 4311.361 | 1.0613x | 12/13 | 0.9972–1.0734x |
| corpus/tests/images/gallery2/3_webp_ll.webp | scalar_inc | 4593.195 | 4550.690 | 1.0086x | 13/13 | 1.0012–1.0180x |
| corpus/tests/images/gallery2/4_webp_ll.webp | packed_outer | 759.991 | 674.452 | 1.1267x | 13/13 | 1.1196–1.1489x |
| corpus/tests/images/gallery2/4_webp_ll.webp | packed_current | 755.177 | 663.814 | 1.1369x | 13/13 | 1.1279–1.1535x |
| corpus/tests/images/gallery2/4_webp_ll.webp | packed_inc | 759.985 | 687.596 | 1.1056x | 13/13 | 1.0909–1.3512x |
| corpus/tests/images/gallery2/4_webp_ll.webp | scalar_inc | 758.236 | 757.466 | 0.9995x | 6/13 | 0.9866–1.0044x |
| corpus/tests/images/gallery2/5_webp_ll.webp | packed_outer | 1958.224 | 1881.495 | 1.0421x | 13/13 | 1.0273–1.0469x |
| corpus/tests/images/gallery2/5_webp_ll.webp | packed_current | 1954.128 | 1852.195 | 1.0549x | 13/13 | 1.0454–1.0604x |
| corpus/tests/images/gallery2/5_webp_ll.webp | packed_inc | 1965.064 | 1894.894 | 1.0363x | 13/13 | 1.0160–1.1009x |
| corpus/tests/images/gallery2/5_webp_ll.webp | scalar_inc | 1955.431 | 1964.562 | 0.9970x | 3/13 | 0.9861–1.0086x |
| corpus/tests/images/regression/color_index.webp | packed_outer | 9.537 | 9.498 | 1.0043x | 8/13 | 0.8578–1.0333x |
| corpus/tests/images/regression/color_index.webp | packed_current | 9.556 | 9.534 | 0.9996x | 6/13 | 0.9303–1.0686x |
| corpus/tests/images/regression/color_index.webp | packed_inc | 9.481 | 9.434 | 1.0063x | 10/13 | 0.9967–1.0438x |
| corpus/tests/images/regression/color_index.webp | scalar_inc | 9.456 | 9.570 | 0.9883x | 2/13 | 0.9560–1.0364x |
| corpus/tests/images/regression/lossless_indexed_1bit_palette.webp | packed_outer | 37.778 | 37.131 | 1.0173x | 13/13 | 1.0103–1.0213x |
| corpus/tests/images/regression/lossless_indexed_1bit_palette.webp | packed_current | 37.802 | 37.392 | 1.0092x | 12/13 | 0.9907–1.0271x |
| corpus/tests/images/regression/lossless_indexed_1bit_palette.webp | packed_inc | 37.809 | 37.158 | 1.0158x | 13/13 | 1.0096–1.0296x |
| corpus/tests/images/regression/lossless_indexed_1bit_palette.webp | scalar_inc | 37.734 | 37.261 | 1.0140x | 13/13 | 1.0056–1.0243x |
| corpus/tests/images/regression/lossless_indexed_2bit_palette.webp | packed_outer | 44.906 | 44.824 | 1.0029x | 8/13 | 0.9923–1.1613x |
| corpus/tests/images/regression/lossless_indexed_2bit_palette.webp | packed_current | 44.758 | 44.818 | 0.9978x | 4/13 | 0.9902–1.0061x |
| corpus/tests/images/regression/lossless_indexed_2bit_palette.webp | packed_inc | 44.486 | 44.423 | 1.0014x | 9/13 | 0.9966–1.0083x |
| corpus/tests/images/regression/lossless_indexed_2bit_palette.webp | scalar_inc | 44.867 | 44.930 | 0.9997x | 6/13 | 0.9822–1.0287x |
| corpus/tests/images/regression/lossless_indexed_4bit_palette.webp | packed_outer | 651.594 | 632.838 | 1.0265x | 13/13 | 1.0223–1.0412x |
| corpus/tests/images/regression/lossless_indexed_4bit_palette.webp | packed_current | 651.674 | 650.748 | 1.0019x | 8/13 | 0.9944–1.0114x |
| corpus/tests/images/regression/lossless_indexed_4bit_palette.webp | packed_inc | 651.029 | 630.056 | 1.0326x | 13/13 | 1.0197–1.0544x |
| corpus/tests/images/regression/lossless_indexed_4bit_palette.webp | scalar_inc | 650.119 | 648.687 | 0.9996x | 6/13 | 0.9946–1.0187x |
| corpus/tests/images/regression/tiny.webp | packed_outer | 8.158 | 8.110 | 1.0048x | 8/13 | 0.9016–1.0309x |
| corpus/tests/images/regression/tiny.webp | packed_current | 8.168 | 8.083 | 1.0053x | 11/13 | 0.9977–1.0628x |
| corpus/tests/images/regression/tiny.webp | packed_inc | 8.158 | 8.084 | 1.0093x | 13/13 | 1.0022–1.0211x |
| corpus/tests/images/regression/tiny.webp | scalar_inc | 8.148 | 8.129 | 1.0006x | 8/13 | 0.9893–1.0197x |
| gen/structured-z0.webp | packed_outer | 23764.297 | 23819.610 | 0.9973x | 3/13 | 0.9917–1.0147x |
| gen/structured-z0.webp | packed_current | 23727.439 | 23723.124 | 0.9995x | 6/13 | 0.9916–1.0044x |
| gen/structured-z0.webp | packed_inc | 23726.853 | 23819.775 | 0.9963x | 0/13 | 0.9937–0.9992x |
| gen/structured-z0.webp | scalar_inc | 23743.629 | 23726.853 | 1.0001x | 7/13 | 0.9901–1.0062x |
| gen/structured-z3.webp | packed_outer | 11132.053 | 8543.926 | 1.3020x | 13/13 | 1.2863–1.3175x |
| gen/structured-z3.webp | packed_current | 11130.019 | 9023.841 | 1.2345x | 13/13 | 1.2277–1.2636x |
| gen/structured-z3.webp | packed_inc | 11121.734 | 8540.818 | 1.3014x | 13/13 | 1.2976–1.3102x |
| gen/structured-z3.webp | scalar_inc | 11141.676 | 10653.023 | 1.0450x | 13/13 | 1.0409–1.0840x |
| gen/structured-z6.webp | packed_outer | 10758.308 | 8173.867 | 1.3172x | 13/13 | 1.3115–1.3254x |
| gen/structured-z6.webp | packed_current | 10764.018 | 8633.851 | 1.2471x | 13/13 | 1.2381–1.2961x |
| gen/structured-z6.webp | packed_inc | 10772.506 | 8177.126 | 1.3168x | 13/13 | 1.3052–1.3467x |
| gen/structured-z6.webp | scalar_inc | 10753.563 | 10262.703 | 1.0489x | 13/13 | 1.0412–1.0862x |
| gen/structured-z9.webp | packed_outer | 10720.561 | 8417.298 | 1.2733x | 13/13 | 1.2661–1.2857x |
| gen/structured-z9.webp | packed_current | 10743.867 | 8872.508 | 1.2117x | 13/13 | 1.1971–1.7377x |
| gen/structured-z9.webp | packed_inc | 10746.900 | 8571.852 | 1.2529x | 12/13 | 0.8712–1.9226x |
| gen/structured-z9.webp | scalar_inc | 10729.383 | 10430.317 | 1.0281x | 13/13 | 1.0222–1.0310x |
| gen/color-z0.webp | packed_outer | 17633.468 | 17627.402 | 1.0012x | 8/13 | 0.9805–1.0090x |
| gen/color-z0.webp | packed_current | 17634.199 | 17716.528 | 0.9950x | 0/13 | 0.9882–0.9983x |
| gen/color-z0.webp | packed_inc | 17633.619 | 17657.362 | 0.9987x | 3/13 | 0.9957–1.0027x |
| gen/color-z0.webp | scalar_inc | 17636.412 | 17632.905 | 1.0006x | 8/13 | 0.9977–1.0027x |
| gen/color-z3.webp | packed_outer | 8309.544 | 5849.973 | 1.4207x | 13/13 | 1.4086–1.4322x |
| gen/color-z3.webp | packed_current | 8315.210 | 6087.488 | 1.3658x | 13/13 | 1.3504–1.3760x |
| gen/color-z3.webp | packed_inc | 8315.970 | 5870.392 | 1.4174x | 13/13 | 1.3942–1.4878x |
| gen/color-z3.webp | scalar_inc | 8334.150 | 7792.690 | 1.0695x | 13/13 | 1.0486–1.0760x |
| gen/color-z6.webp | packed_outer | 7833.088 | 5431.701 | 1.4417x | 13/13 | 1.4259–1.4612x |
| gen/color-z6.webp | packed_current | 7807.435 | 5690.001 | 1.3729x | 13/13 | 1.3537–1.3858x |
| gen/color-z6.webp | packed_inc | 7820.852 | 5440.783 | 1.4359x | 13/13 | 1.4210–1.4482x |
| gen/color-z6.webp | scalar_inc | 7825.269 | 7322.838 | 1.0677x | 13/13 | 1.0594–1.0737x |
| gen/color-z9.webp | packed_outer | 9411.021 | 7288.968 | 1.2901x | 13/13 | 1.2740–1.2940x |
| gen/color-z9.webp | packed_current | 9434.149 | 7651.778 | 1.2324x | 13/13 | 1.2262–1.2798x |
| gen/color-z9.webp | packed_inc | 9441.535 | 7474.039 | 1.2643x | 13/13 | 1.2537–1.2735x |
| gen/color-z9.webp | scalar_inc | 9436.360 | 9118.377 | 1.0331x | 12/13 | 0.9566–1.0410x |
| gen/gradient-z9.webp | packed_outer | 12513.192 | 11623.838 | 1.0776x | 13/13 | 1.0722–1.0826x |
| gen/gradient-z9.webp | packed_current | 12499.975 | 11585.887 | 1.0794x | 13/13 | 1.0755–1.0889x |
| gen/gradient-z9.webp | packed_inc | 12470.683 | 11683.953 | 1.0685x | 13/13 | 1.0667–1.0726x |
| gen/gradient-z9.webp | scalar_inc | 12478.084 | 12612.632 | 0.9885x | 0/13 | 0.9743–0.9991x |
| gen/corr-z0.webp | packed_outer | 16322.276 | 16333.036 | 0.9991x | 3/13 | 0.9966–1.0031x |
| gen/corr-z0.webp | packed_current | 16328.661 | 16268.859 | 1.0036x | 12/13 | 1.0000–1.0048x |
| gen/corr-z0.webp | packed_inc | 16334.539 | 16324.917 | 1.0003x | 9/13 | 0.9974–1.0024x |
| gen/corr-z0.webp | scalar_inc | 16323.081 | 16336.105 | 0.9990x | 5/13 | 0.9964–1.0019x |
| gen/corr-z3.webp | packed_outer | 7803.107 | 5291.462 | 1.4728x | 13/13 | 1.4627–1.4852x |
| gen/corr-z3.webp | packed_current | 7807.864 | 5602.742 | 1.3944x | 13/13 | 1.3839–1.4131x |
| gen/corr-z3.webp | packed_inc | 7800.865 | 5304.112 | 1.4718x | 13/13 | 1.4602–1.4817x |
| gen/corr-z3.webp | scalar_inc | 7832.666 | 7288.662 | 1.0743x | 13/13 | 1.0663–1.0793x |
| gen/corr-z6.webp | packed_outer | 7695.609 | 5270.390 | 1.4636x | 13/13 | 1.4438–1.4771x |
| gen/corr-z6.webp | packed_current | 7725.745 | 5622.909 | 1.3712x | 13/13 | 1.3497–1.5406x |
| gen/corr-z6.webp | packed_inc | 7707.080 | 5279.044 | 1.4598x | 13/13 | 1.4538–1.4810x |
| gen/corr-z6.webp | scalar_inc | 7706.858 | 7215.868 | 1.0714x | 13/13 | 1.0438–1.1884x |
| gen/corr-z9.webp | packed_outer | 7712.622 | 5887.577 | 1.3101x | 13/13 | 1.2892–1.3257x |
| gen/corr-z9.webp | packed_current | 7717.794 | 5793.722 | 1.3338x | 13/13 | 1.3214–1.3384x |
| gen/corr-z9.webp | packed_inc | 7697.835 | 6021.171 | 1.2792x | 13/13 | 1.2664–1.2941x |
| gen/corr-z9.webp | scalar_inc | 7708.211 | 7416.766 | 1.0410x | 13/13 | 1.0354–1.0499x |
| gen/anticorr-z9.webp | packed_outer | 7571.684 | 6541.870 | 1.1573x | 13/13 | 1.1520–1.1667x |
| gen/anticorr-z9.webp | packed_current | 7591.591 | 6144.249 | 1.2342x | 13/13 | 1.2213–1.2425x |
| gen/anticorr-z9.webp | packed_inc | 7606.531 | 6702.915 | 1.1351x | 13/13 | 1.0380–1.1451x |
| gen/anticorr-z9.webp | scalar_inc | 7595.795 | 8128.428 | 0.9345x | 0/13 | 0.8523–0.9430x |
| gen/tiles-z9.webp | packed_outer | 11249.767 | 9903.719 | 1.1364x | 13/13 | 1.1315–1.1441x |
| gen/tiles-z9.webp | packed_current | 11257.018 | 9837.160 | 1.1445x | 13/13 | 1.1407–1.1480x |
| gen/tiles-z9.webp | packed_inc | 11252.279 | 10055.569 | 1.1178x | 13/13 | 1.1125–1.1278x |
| gen/tiles-z9.webp | scalar_inc | 11277.651 | 11756.386 | 0.9602x | 0/13 | 0.9534–0.9709x |
| gen/noise-z9.webp | packed_outer | 26352.948 | 25813.158 | 1.0210x | 13/13 | 1.0134–1.0324x |
| gen/noise-z9.webp | packed_current | 26344.807 | 25682.329 | 1.0253x | 13/13 | 1.0128–1.0315x |
| gen/noise-z9.webp | packed_inc | 26322.228 | 25891.656 | 1.0175x | 13/13 | 1.0107–1.0261x |
| gen/noise-z9.webp | scalar_inc | 26323.029 | 26394.282 | 0.9970x | 3/13 | 0.9909–1.0127x |
| gen/photoish-z9.webp | packed_outer | 9863.479 | 7617.078 | 1.2942x | 13/13 | 1.2832–1.3119x |
| gen/photoish-z9.webp | packed_current | 9842.237 | 7993.611 | 1.2357x | 13/13 | 1.2218–1.2403x |
| gen/photoish-z9.webp | packed_inc | 9843.244 | 7770.567 | 1.2723x | 13/13 | 1.2560–1.2800x |
| gen/photoish-z9.webp | scalar_inc | 9870.701 | 9555.507 | 1.0326x | 13/13 | 1.0267–1.0455x |

## Aggregate medians

| set | candidate | median file ratio | files >1 |
|---|---|---:|---:|
| corpus | packed_outer | 1.0343x | 10/10 |
| corpus | packed_current | 1.0320x | 8/10 |
| corpus | packed_inc | 1.0345x | 10/10 |
| corpus | scalar_inc | 0.9997x | 4/10 |
| generated | packed_outer | 1.2901x | 15/17 |
| generated | packed_current | 1.2342x | 15/17 |
| generated | packed_inc | 1.2643x | 15/17 |
| generated | scalar_inc | 1.0326x | 12/17 |
| all | packed_outer | 1.1267x | 25/27 |
| all | packed_current | 1.1369x | 23/27 |
| all | packed_inc | 1.1056x | 25/27 |
| all | scalar_inc | 1.0006x | 16/27 |
