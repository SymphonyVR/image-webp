# Final VP8L composed-v3 profile

- candidate source: `4cd194935d100a09acf24eb24d8c1343c7844844`
- workload: issue #119 VP8L sample, 3 decodes under Callgrind
- total instructions: **538,755,219**

## Relevant inclusive functions

| Ir | % total | function |
|---:|---:|---|

## Stop-rule assessment

The exhaustive sweep has already tested the entropy loop, Huffman construction/layout, color cache, LZ copy engine, inverse-color kernels, predictor kernels, palette/subtract-green, input staging, output stores, distance decoding, and transform batching families. Remaining >=2% functions in those families are therefore closed unless this profile exposes a distinct bounded mechanism.
