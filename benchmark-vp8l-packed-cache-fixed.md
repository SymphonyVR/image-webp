# VP8L packed color-cache benchmark

- CPU: `INTEL(R) XEON(R) PLATINUM 8573C`
- fixed refs; full hashes match

| workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| corpus | 1075.650 us | 1067.665 us | 1.0052x | 0.9734–1.0554x |
| large | 21028.204 us | 20224.436 us | 0.9967x | 0.9266–1.0886x |
