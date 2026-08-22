# VP8L cache-presence specialization benchmark

- CPU: `AMD EPYC 7763 64-Core Processor`
- fixed refs; full hashes match

| workload | baseline | candidate | paired median | range |
|---|---:|---:|---:|---:|
| corpus | 1176.667 us | 1219.783 us | 0.9651x | 0.9582–0.9689x |
| large | 22406.622 us | 22863.077 us | 0.9751x | 0.9603–0.9890x |
