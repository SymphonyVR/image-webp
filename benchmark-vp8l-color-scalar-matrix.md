# VP8L color scalar matrix

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `Intel(R) Xeon(R) 6973P-C`
- all candidates: VP8L hashes match, cargo test passes, MSRV 1.80.1 builds

| workload | candidate | base median | candidate median | paired median | positive rounds | range |
|---|---|---:|---:|---:|---:|---:|
| corpus | hoist | 804.921 us | 812.177 us | 0.9910x | 2/13 | 0.9297–1.0638x |
| corpus | signed | 804.921 us | 818.346 us | 0.9831x | 3/13 | 0.9244–1.0764x |
| corpus | incremental | 804.921 us | 807.126 us | 0.9985x | 6/13 | 0.9626–1.0445x |
| corpus | combined | 804.921 us | 817.415 us | 0.9865x | 2/13 | 0.9563–1.0313x |
| corpus | exact | 804.921 us | 797.552 us | 1.0094x | 10/13 | 0.9537–1.0880x |
| large | hoist | 14447.363 us | 15096.246 us | 0.9530x | 2/13 | 0.9152–1.0503x |
| large | signed | 14447.363 us | 15543.417 us | 0.9343x | 2/13 | 0.8993–1.0304x |
| large | incremental | 14447.363 us | 14826.633 us | 0.9851x | 6/13 | 0.9499–1.0568x |
| large | combined | 14447.363 us | 15583.220 us | 0.9321x | 1/13 | 0.8829–1.0215x |
| large | exact | 14447.363 us | 14290.045 us | 1.0198x | 9/13 | 0.9024–1.0936x |
