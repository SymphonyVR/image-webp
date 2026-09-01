# VP8L decoder-stream lineage v4

- baseline: `58dba70a93fef7883c934e28465e04534278fb80`
- CPU: `AMD EPYC 7763 64-Core Processor`
- mainmod restores upstream main `mod.rs` while retaining packed-color + 9-bit Huffman root
- 17 paired rounds; hashes/tests/MSRV passed

| workload | current | mainmod | current/mainmod | mainmod wins |
|---|---:|---:|---:|---:|
| corpus | 1017.354 us | 1027.621 us | 0.9904x | 0/17 |
| gen_z9 | 16752.860 us | 17206.503 us | 0.9735x | 0/17 |
| structured | 7069.205 us | 7101.283 us | 0.9949x | 3/17 |
