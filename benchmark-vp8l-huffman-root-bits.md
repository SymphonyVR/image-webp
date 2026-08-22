# VP8L Huffman root-width benchmark

- baseline source: `0fdcb2f57d1d7dd272ee45d08e26fc80cb3f2aa8`
- CPU: `AMD EPYC 7763 64-Core Processor`
- static VP8L corpus; normal release; CPU 0; rotating 15-round order

| Root bits | median us/decode | vs 10-bit |
|---:|---:|---:|
| 10 | 1222.069 | 1.0000x |
| 9 | 1209.838 | 1.0101x |
| 8 | 1227.467 | 0.9956x |
