# VP8L Huffman root-width v4 matrix

- color-only baseline lineage: `58dba70a93fef7883c934e28465e04534278fb80`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- 15 alternating rounds; hashes/tests/MSRV passed

| workload | root | median | speedup vs 9-bit | positive vs 9 |
|---|---:|---:|---:|---:|
| corpus | 8 | 1071.829 us | 0.9955x | 2/15 |
| corpus | 9 | 1066.665 us | 1.0000x | 0/15 |
| corpus | 10 | 1096.183 us | 0.9729x | 0/15 |
| corpus | 11 | 1136.747 us | 0.9380x | 0/15 |
| gen_z9 | 8 | 16727.611 us | 0.8870x | 0/15 |
| gen_z9 | 9 | 14841.534 us | 1.0000x | 0/15 |
| gen_z9 | 10 | 12273.489 us | 1.2088x | 15/15 |
| gen_z9 | 11 | 11961.532 us | 1.2405x | 15/15 |
| large | 8 | 7330.127 us | 1.0089x | 14/15 |
| large | 9 | 7401.488 us | 1.0000x | 0/15 |
| large | 10 | 7380.428 us | 1.0038x | 12/15 |
| large | 11 | 7442.677 us | 0.9950x | 1/15 |
