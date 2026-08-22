# Current optimization scorecard

- original: `f4d80bd965df2c81e65b6f43c1f70e0750bd4b0f`
- current: `0fdcb2f57d1d7dd272ee45d08e26fc80cb3f2aa8`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- same-run native release, CPU 0, paired medians

| Workload | original | current | paired speedup |
|---|---:|---:|---:|
| issue119 | 415295.177 us | 291423.067 us | 1.428x |
| issue136 | 36469.618 us | 33302.703 us | 1.096x |
| vp8l | 1223.896 us | 1228.235 us | 0.996x |
