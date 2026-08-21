# VP8 hot-path cross-runner matrix

- normal release target; CPU 0; 7 rotating-order rounds per runner
- all candidates are safe Rust and keep MSRV 1.80.1

## Runner 1: `AMD EPYC 7763 64-Core Processor`

| Workload | Variant | median | ratio vs baseline median | paired baseline/variant median | paired range |
|---|---|---:|---:|---:|---:|
| issue119 | baseline | 375786.015 us | 1.000x | 1.000x | — |
| issue119 | leaf | 369681.370 us | 1.017x | 1.013x | 1.002–1.036x |
| issue119 | range | 374229.811 us | 1.004x | 0.998x | 0.977–1.021x |
| issue119 | combined | 366540.313 us | 1.025x | 1.021x | 0.960–1.041x |
| issue136 | baseline | 36170.255 us | 1.000x | 1.000x | — |
| issue136 | leaf | 36057.973 us | 1.003x | 1.003x | 0.995–1.013x |
| issue136 | range | 36086.939 us | 1.002x | 1.002x | 0.996–1.007x |
| issue136 | combined | 35865.370 us | 1.009x | 1.011x | 1.003–1.015x |

## Runner 2: `AMD EPYC 9V74 80-Core Processor`

| Workload | Variant | median | ratio vs baseline median | paired baseline/variant median | paired range |
|---|---|---:|---:|---:|---:|
| issue119 | baseline | 389736.946 us | 1.000x | 1.000x | — |
| issue119 | leaf | 384585.788 us | 1.013x | 1.014x | 1.009–1.016x |
| issue119 | range | 382826.465 us | 1.018x | 1.017x | 1.015–1.020x |
| issue119 | combined | 382461.393 us | 1.019x | 1.018x | 1.009–1.023x |
| issue136 | baseline | 38352.320 us | 1.000x | 1.000x | — |
| issue136 | leaf | 38180.260 us | 1.005x | 1.002x | 0.999–1.011x |
| issue136 | range | 38157.052 us | 1.005x | 1.005x | 0.982–1.010x |
| issue136 | combined | 38077.961 us | 1.007x | 1.009x | 1.004–1.011x |

## Runner 3: `AMD EPYC 7763 64-Core Processor`

| Workload | Variant | median | ratio vs baseline median | paired baseline/variant median | paired range |
|---|---|---:|---:|---:|---:|
| issue119 | baseline | 370258.053 us | 1.000x | 1.000x | — |
| issue119 | leaf | 369317.274 us | 1.003x | 1.003x | 0.996–1.009x |
| issue119 | range | 371917.351 us | 0.996x | 0.996x | 0.987–1.012x |
| issue119 | combined | 366049.720 us | 1.011x | 1.012x | 1.007–1.029x |
| issue136 | baseline | 35994.346 us | 1.000x | 1.000x | — |
| issue136 | leaf | 35894.617 us | 1.003x | 1.005x | 0.998–1.009x |
| issue136 | range | 35982.428 us | 1.000x | 1.002x | 0.999–1.004x |
| issue136 | combined | 35840.334 us | 1.004x | 1.005x | 1.002–1.011x |

## Runner 4: `AMD EPYC 9V74 80-Core Processor`

| Workload | Variant | median | ratio vs baseline median | paired baseline/variant median | paired range |
|---|---|---:|---:|---:|---:|
| issue119 | baseline | 387725.321 us | 1.000x | 1.000x | — |
| issue119 | leaf | 382533.171 us | 1.014x | 1.012x | 1.009–1.019x |
| issue119 | range | 382047.709 us | 1.015x | 1.015x | 1.013–1.022x |
| issue119 | combined | 379807.328 us | 1.021x | 1.020x | 1.014–1.024x |
| issue136 | baseline | 38284.550 us | 1.000x | 1.000x | — |
| issue136 | leaf | 38106.611 us | 1.005x | 1.005x | 0.999–1.007x |
| issue136 | range | 38027.885 us | 1.007x | 1.009x | 1.000–1.011x |
| issue136 | combined | 37917.464 us | 1.010x | 1.008x | 0.999–1.015x |

