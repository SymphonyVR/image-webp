# VP8L deep predictor matrix

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- candidates: direct packed modes 2–4; average packed modes 5–10; combined packed modes 2–10
- hashes + tests + Rust 1.80.1 pass
- 13 alternating paired rounds/file; ~45 ms/sample

| file | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus/1_webp_ll.webp | direct | 1.0262x | 13/13 | 1.0007–1.0637x |
| corpus/1_webp_ll.webp | avg | 1.0070x | 10/13 | 0.9593–1.0397x |
| corpus/1_webp_ll.webp | packed | 1.0223x | 13/13 | 1.0015–1.0566x |
| corpus/2_webp_ll.webp | direct | 1.0403x | 13/13 | 1.0149–1.0608x |
| corpus/2_webp_ll.webp | avg | 1.0090x | 9/13 | 0.9881–1.0218x |
| corpus/2_webp_ll.webp | packed | 1.0553x | 13/13 | 1.0253–1.0741x |
| corpus/3_webp_ll.webp | direct | 1.0159x | 11/13 | 0.9800–1.0686x |
| corpus/3_webp_ll.webp | avg | 1.0171x | 8/13 | 0.9719–1.0357x |
| corpus/3_webp_ll.webp | packed | 1.0363x | 11/13 | 0.9965–1.0579x |
| corpus/4_webp_ll.webp | direct | 1.0580x | 13/13 | 1.0054–1.0947x |
| corpus/4_webp_ll.webp | avg | 1.0055x | 10/13 | 0.9916–1.0296x |
| corpus/4_webp_ll.webp | packed | 1.0816x | 13/13 | 1.0639–1.0998x |
| corpus/5_webp_ll.webp | direct | 1.0400x | 13/13 | 1.0073–1.0610x |
| corpus/5_webp_ll.webp | avg | 1.0023x | 7/13 | 0.9664–1.0164x |
| corpus/5_webp_ll.webp | packed | 1.0578x | 13/13 | 1.0264–1.0912x |
| corpus/color_index.webp | direct | 1.2048x | 13/13 | 1.1139–1.2350x |
| corpus/color_index.webp | avg | 0.9819x | 4/13 | 0.9241–1.0809x |
| corpus/color_index.webp | packed | 1.2025x | 13/13 | 1.1112–1.3137x |
| corpus/lossless_indexed_1bit_palette.webp | direct | 0.9998x | 6/13 | 0.9259–1.0431x |
| corpus/lossless_indexed_1bit_palette.webp | avg | 0.9975x | 4/13 | 0.9511–1.0365x |
| corpus/lossless_indexed_1bit_palette.webp | packed | 0.9950x | 5/13 | 0.9645–1.0447x |
| corpus/lossless_indexed_2bit_palette.webp | direct | 1.0049x | 7/13 | 0.9864–1.0267x |
| corpus/lossless_indexed_2bit_palette.webp | avg | 0.9965x | 6/13 | 0.9762–1.0507x |
| corpus/lossless_indexed_2bit_palette.webp | packed | 1.0035x | 9/13 | 0.9689–1.0181x |
| corpus/lossless_indexed_4bit_palette.webp | direct | 1.0000x | 6/13 | 0.9796–1.0381x |
| corpus/lossless_indexed_4bit_palette.webp | avg | 0.9940x | 1/13 | 0.9515–1.0173x |
| corpus/lossless_indexed_4bit_palette.webp | packed | 1.0085x | 7/13 | 0.9705–1.0265x |
| corpus/tiny.webp | direct | 1.0070x | 9/13 | 0.8636–1.0528x |
| corpus/tiny.webp | avg | 1.0007x | 7/13 | 0.9472–1.0877x |
| corpus/tiny.webp | packed | 0.9899x | 2/13 | 0.9469–1.0224x |
| gen/gradient-z0 | direct | 1.0046x | 9/13 | 0.9467–1.0508x |
| gen/gradient-z0 | avg | 0.9883x | 6/13 | 0.9251–1.0446x |
| gen/gradient-z0 | packed | 0.9994x | 6/13 | 0.9197–1.0309x |
| gen/gradient-z3 | direct | 1.0070x | 11/13 | 0.9531–1.0303x |
| gen/gradient-z3 | avg | 1.0030x | 8/13 | 0.9471–1.0361x |
| gen/gradient-z3 | packed | 0.9892x | 3/13 | 0.9383–1.0372x |
| gen/gradient-z6 | direct | 1.0022x | 7/13 | 0.9909–1.0253x |
| gen/gradient-z6 | avg | 1.0088x | 11/13 | 0.9879–1.0830x |
| gen/gradient-z6 | packed | 0.9925x | 5/13 | 0.9641–1.0201x |
| gen/gradient-z9 | direct | 0.9918x | 4/13 | 0.9465–1.0174x |
| gen/gradient-z9 | avg | 1.0001x | 7/13 | 0.9574–1.0559x |
| gen/gradient-z9 | packed | 0.9853x | 3/13 | 0.9565–1.0068x |
| gen/corr-z0 | direct | 1.0065x | 8/13 | 0.9534–1.0463x |
| gen/corr-z0 | avg | 0.9816x | 2/13 | 0.9545–1.0353x |
| gen/corr-z0 | packed | 0.9991x | 5/13 | 0.9467–1.0291x |
| gen/corr-z3 | direct | 1.0049x | 7/13 | 0.9742–1.0448x |
| gen/corr-z3 | avg | 1.0220x | 9/13 | 0.9434–1.0656x |
| gen/corr-z3 | packed | 1.0406x | 13/13 | 1.0066–1.0866x |
| gen/corr-z6 | direct | 1.0178x | 9/13 | 0.9866–1.0280x |
| gen/corr-z6 | avg | 1.0302x | 12/13 | 0.9660–1.0647x |
| gen/corr-z6 | packed | 1.0447x | 11/13 | 0.9950–1.0704x |
| gen/corr-z9 | direct | 0.9984x | 6/13 | 0.9678–1.0392x |
| gen/corr-z9 | avg | 1.0498x | 13/13 | 1.0150–1.0885x |
| gen/corr-z9 | packed | 1.0576x | 13/13 | 1.0075–1.1039x |
| gen/stripes-z0 | direct | 0.9998x | 6/13 | 0.9500–1.0237x |
| gen/stripes-z0 | avg | 0.9923x | 5/13 | 0.9593–1.0453x |
| gen/stripes-z0 | packed | 1.0144x | 11/13 | 0.9826–1.0334x |
| gen/stripes-z3 | direct | 2.1241x | 13/13 | 2.0535–2.2493x |
| gen/stripes-z3 | avg | 0.9803x | 3/13 | 0.9327–1.0386x |
| gen/stripes-z3 | packed | 2.1301x | 13/13 | 2.0159–2.1869x |
| gen/stripes-z6 | direct | 2.1148x | 13/13 | 2.0126–2.1761x |
| gen/stripes-z6 | avg | 0.9920x | 3/13 | 0.9621–1.0492x |
| gen/stripes-z6 | packed | 2.1343x | 13/13 | 2.0843–2.1985x |
| gen/stripes-z9 | direct | 1.6974x | 13/13 | 1.6131–1.7273x |
| gen/stripes-z9 | avg | 0.9674x | 1/13 | 0.9526–1.0171x |
| gen/stripes-z9 | packed | 1.6552x | 13/13 | 1.5856–1.7368x |
| gen/tiles-z0 | direct | 0.9890x | 5/13 | 0.9606–1.0103x |
| gen/tiles-z0 | avg | 1.0188x | 9/13 | 0.9640–1.0368x |
| gen/tiles-z0 | packed | 1.0074x | 8/13 | 0.9497–1.0537x |
| gen/tiles-z3 | direct | 1.0037x | 7/13 | 0.9747–1.0443x |
| gen/tiles-z3 | avg | 0.9887x | 4/13 | 0.9561–1.0761x |
| gen/tiles-z3 | packed | 1.0089x | 7/13 | 0.9396–1.0443x |
| gen/tiles-z6 | direct | 0.9922x | 5/13 | 0.9621–1.0402x |
| gen/tiles-z6 | avg | 1.0027x | 8/13 | 0.9764–1.0237x |
| gen/tiles-z6 | packed | 1.0066x | 9/13 | 0.9352–1.0733x |
| gen/tiles-z9 | direct | 1.5408x | 13/13 | 1.4702–1.6002x |
| gen/tiles-z9 | avg | 0.9714x | 4/13 | 0.9556–1.0593x |
| gen/tiles-z9 | packed | 1.5333x | 13/13 | 1.4752–1.5698x |
| gen/smooth-z0 | direct | 1.0135x | 10/13 | 0.9733–1.0880x |
| gen/smooth-z0 | avg | 1.0052x | 8/13 | 0.9658–1.0316x |
| gen/smooth-z0 | packed | 0.9946x | 6/13 | 0.9676–1.0457x |
| gen/smooth-z3 | direct | 1.0009x | 8/13 | 0.9536–1.0242x |
| gen/smooth-z3 | avg | 1.0000x | 7/13 | 0.9691–1.0388x |
| gen/smooth-z3 | packed | 1.0043x | 9/13 | 0.9685–1.0303x |
| gen/smooth-z6 | direct | 1.0082x | 11/13 | 0.9771–1.0416x |
| gen/smooth-z6 | avg | 0.9818x | 1/13 | 0.9536–1.0104x |
| gen/smooth-z6 | packed | 0.9825x | 2/13 | 0.9483–1.0162x |
| gen/smooth-z9 | direct | 1.0034x | 7/13 | 0.9346–1.0405x |
| gen/smooth-z9 | avg | 0.9986x | 5/13 | 0.9418–1.0352x |
| gen/smooth-z9 | packed | 0.9865x | 4/13 | 0.9645–1.0477x |
| gen/noise-z0 | direct | 0.9966x | 6/13 | 0.8946–1.0242x |
| gen/noise-z0 | avg | 1.0123x | 8/13 | 0.9924–1.0456x |
| gen/noise-z0 | packed | 1.0041x | 7/13 | 0.9828–1.0181x |
| gen/noise-z3 | direct | 1.0111x | 8/13 | 0.9312–1.0699x |
| gen/noise-z3 | avg | 0.9983x | 6/13 | 0.9589–1.0251x |
| gen/noise-z3 | packed | 1.0057x | 9/13 | 0.9864–1.0378x |
| gen/noise-z6 | direct | 1.0198x | 10/13 | 0.9857–1.0448x |
| gen/noise-z6 | avg | 0.9965x | 6/13 | 0.9607–1.0653x |
| gen/noise-z6 | packed | 1.0192x | 13/13 | 1.0051–1.0441x |
| gen/noise-z9 | direct | 1.0159x | 9/13 | 0.9787–1.0503x |
| gen/noise-z9 | avg | 1.0087x | 8/13 | 0.9610–1.0423x |
| gen/noise-z9 | packed | 1.0085x | 10/13 | 0.9659–1.0916x |

## Aggregate

| set | candidate | median file ratio | files >1 |
|---|---|---:|---:|
| corpus | direct | 1.0211x | 8/10 |
| corpus | avg | 1.0015x | 6/10 |
| corpus | packed | 1.0293x | 8/10 |
| generated | direct | 1.0057x | 18/24 |
| generated | avg | 0.9993x | 12/24 |
| generated | packed | 1.0070x | 16/24 |
| all | direct | 1.0070x | 26/34 |
| all | avg | 1.0001x | 18/34 |
| all | packed | 1.0085x | 24/34 |
