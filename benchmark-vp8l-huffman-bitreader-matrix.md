# VP8L Huffman / BitReader matrix

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `AMD EPYC 7763 64-Core Processor`
- all candidates: hashes match, cargo test passes, MSRV 1.80.1 builds

| workload | candidate | base median | candidate median | paired median | positive | range |
|---|---|---:|---:|---:|---:|---:|
| corpus | sorted | 1063.702 us | 1071.438 us | 0.9934x | 2/13 | 0.9874–1.0125x |
| corpus | clen | 1063.702 us | 1079.422 us | 0.9869x | 1/13 | 0.9689–1.0020x |
| corpus | huff | 1063.702 us | 1061.090 us | 1.0029x | 10/13 | 0.9973–1.0164x |
| corpus | fill | 1063.702 us | 1112.948 us | 0.9553x | 0/13 | 0.9503–0.9711x |
| corpus | inline | 1063.702 us | 1207.270 us | 0.8810x | 0/13 | 0.8645–0.8973x |
| corpus | all | 1063.702 us | 1141.815 us | 0.9319x | 0/13 | 0.9259–0.9455x |
| large | sorted | 17827.540 us | 17889.212 us | 0.9974x | 4/13 | 0.9840–1.0452x |
| large | clen | 17827.540 us | 18618.814 us | 0.9602x | 0/13 | 0.9468–0.9974x |
| large | huff | 17827.540 us | 17657.742 us | 1.0092x | 11/13 | 0.9959–1.0517x |
| large | fill | 17827.540 us | 17916.826 us | 0.9981x | 4/13 | 0.9802–1.0589x |
| large | inline | 17827.540 us | 21753.378 us | 0.8195x | 0/13 | 0.8092–0.8551x |
| large | all | 17827.540 us | 18704.871 us | 0.9521x | 0/13 | 0.9267–0.9934x |
