# VP8L transform closure matrix

- baseline: `509d11c2bf102929ded4be05d3c54b06032fdc44`
- CPU: `Intel(R) Xeon(R) 6973P-C`
- static VP8L fixtures: `10`
- all candidates: decoded hashes match; cargo test and Rust 1.80.1 build pass

| workload | candidate | paired median | positive | range |
|---|---|---:|---:|---:|
| corpus | color_exact | 1.0182x | 10/11 | 0.9530–1.0782x |
| corpus | color_inc | 1.0217x | 10/11 | 0.9877–1.0941x |
| corpus | color_packed | 1.0620x | 11/11 | 1.0467–1.1324x |
| corpus | green | 0.9991x | 4/11 | 0.9876–1.0618x |
| corpus | palette_stack | 1.0088x | 9/11 | 0.9299–1.0787x |
| corpus | palette_noscratch | 0.9925x | 3/11 | 0.9784–1.0521x |
| corpus | palette_both | 1.0069x | 9/11 | 0.9904–1.0704x |
| corpus | all | 1.0036x | 9/11 | 0.9862–1.0709x |
| large | color_exact | 1.0312x | 11/11 | 1.0047–1.0910x |
| large | color_inc | 1.0289x | 10/11 | 0.9994–1.1592x |
| large | color_packed | 1.0959x | 11/11 | 1.0659–1.2184x |
| large | green | 1.0061x | 7/11 | 0.9354–1.0888x |
| large | palette_stack | 0.9919x | 5/11 | 0.9208–1.1124x |
| large | palette_noscratch | 0.9598x | 2/11 | 0.9319–1.0754x |
| large | palette_both | 1.0069x | 6/11 | 0.9617–1.0974x |
| large | all | 0.9885x | 4/11 | 0.9617–1.0691x |
| green | green | 0.9170x | 0/11 | 0.8734–0.9700x |
| green | all | 0.9107x | 0/11 | 0.8728–0.9944x |
| palette | palette_stack | 0.9929x | 4/11 | 0.8939–1.1030x |
| palette | palette_noscratch | 0.9230x | 1/11 | 0.8307–1.0307x |
| palette | palette_both | 0.9300x | 1/11 | 0.8938–1.0379x |
| palette | all | 0.9346x | 1/11 | 0.9143–1.0401x |
