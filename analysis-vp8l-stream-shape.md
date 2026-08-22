# VP8L stream-shape analysis

Current optimized decoder instrumentation. Counts describe entropy events, not timed performance.

## Static fixtures

```text
FILE /home/runner/work/image-webp/image-webp/tests/images/gallery2/1_webp_ll.webp
VP8L_SHAPE width=50 height=38 cache=false groups=1 meta_bits=0 literals=734 backrefs=94 backref_pixels=1166 cache_refs=0 dist1=35 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=59
VP8L_SHAPE width=50 height=38 cache=false groups=1 meta_bits=0 literals=1039 backrefs=45 backref_pixels=861 cache_refs=0 dist1=17 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=28
VP8L_SHAPE width=50 height=38 cache=false groups=1 meta_bits=0 literals=699 backrefs=85 backref_pixels=1201 cache_refs=0 dist1=37 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=48
VP8L_SHAPE width=400 height=301 cache=false groups=8 meta_bits=3 literals=58219 backrefs=444 backref_pixels=62181 cache_refs=0 dist1=168 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=276
FILE /home/runner/work/image-webp/image-webp/tests/images/gallery2/2_webp_ll.webp
VP8L_SHAPE width=49 height=50 cache=false groups=1 meta_bits=0 literals=620 backrefs=131 backref_pixels=1830 cache_refs=0 dist1=30 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=101
VP8L_SHAPE width=49 height=50 cache=false groups=1 meta_bits=0 literals=329 backrefs=27 backref_pixels=2121 cache_refs=0 dist1=7 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=20
VP8L_SHAPE width=49 height=50 cache=false groups=1 meta_bits=0 literals=476 backrefs=136 backref_pixels=1974 cache_refs=0 dist1=62 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=74
VP8L_SHAPE width=386 height=395 cache=true groups=9 meta_bits=3 literals=2733 backrefs=3340 backref_pixels=118024 cache_refs=17945 dist1=1313 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=2027
FILE /home/runner/work/image-webp/image-webp/tests/images/gallery2/3_webp_ll.webp
VP8L_SHAPE width=50 height=38 cache=false groups=1 meta_bits=0 literals=600 backrefs=55 backref_pixels=1300 cache_refs=0 dist1=13 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=42
VP8L_SHAPE width=50 height=38 cache=false groups=1 meta_bits=0 literals=672 backrefs=46 backref_pixels=1228 cache_refs=0 dist1=11 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=35
VP8L_SHAPE width=50 height=38 cache=false groups=1 meta_bits=0 literals=626 backrefs=52 backref_pixels=1274 cache_refs=0 dist1=38 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=14
VP8L_SHAPE width=800 height=600 cache=true groups=36 meta_bits=4 literals=106789 backrefs=3654 backref_pixels=354166 cache_refs=14515 dist1=1778 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=1876
FILE /home/runner/work/image-webp/image-webp/tests/images/gallery2/4_webp_ll.webp
VP8L_SHAPE width=53 height=21 cache=false groups=1 meta_bits=0 literals=457 backrefs=52 backref_pixels=656 cache_refs=0 dist1=15 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=37
VP8L_SHAPE width=53 height=21 cache=false groups=1 meta_bits=0 literals=465 backrefs=32 backref_pixels=648 cache_refs=0 dist1=16 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=16
VP8L_SHAPE width=53 height=21 cache=false groups=1 meta_bits=0 literals=293 backrefs=64 backref_pixels=820 cache_refs=0 dist1=40 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=24
VP8L_SHAPE width=421 height=163 cache=false groups=5 meta_bits=3 literals=18039 backrefs=918 backref_pixels=50584 cache_refs=0 dist1=36 dist2=0 dist3_4=0 dist5_16=22 dist_gt16=860
FILE /home/runner/work/image-webp/image-webp/tests/images/gallery2/5_webp_ll.webp
VP8L_SHAPE width=38 height=38 cache=false groups=1 meta_bits=0 literals=862 backrefs=77 backref_pixels=582 cache_refs=0 dist1=29 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=48
VP8L_SHAPE width=38 height=38 cache=false groups=1 meta_bits=0 literals=855 backrefs=90 backref_pixels=589 cache_refs=0 dist1=19 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=71
VP8L_SHAPE width=38 height=38 cache=false groups=1 meta_bits=0 literals=824 backrefs=86 backref_pixels=620 cache_refs=0 dist1=50 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=36
VP8L_SHAPE width=300 height=300 cache=true groups=11 meta_bits=3 literals=40975 backrefs=3748 backref_pixels=46836 cache_refs=1820 dist1=47 dist2=9 dist3_4=29 dist5_16=59 dist_gt16=3604
FILE /home/runner/work/image-webp/image-webp/tests/images/regression/color_index.webp
VP8L_SHAPE width=1 height=1 cache=false groups=1 meta_bits=0 literals=0 backrefs=0 backref_pixels=0 cache_refs=0 dist1=0 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=0
VP8L_SHAPE width=16 height=1 cache=false groups=1 meta_bits=0 literals=0 backrefs=0 backref_pixels=0 cache_refs=0 dist1=0 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=0
VP8L_SHAPE width=15 height=30 cache=false groups=1 meta_bits=0 literals=450 backrefs=0 backref_pixels=0 cache_refs=0 dist1=0 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=0
FILE /home/runner/work/image-webp/image-webp/tests/images/regression/lossless_indexed_1bit_palette.webp
VP8L_SHAPE width=2 height=1 cache=false groups=1 meta_bits=0 literals=2 backrefs=0 backref_pixels=0 cache_refs=0 dist1=0 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=0
VP8L_SHAPE width=29 height=128 cache=false groups=1 meta_bits=0 literals=641 backrefs=146 backref_pixels=3071 cache_refs=0 dist1=6 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=140
FILE /home/runner/work/image-webp/image-webp/tests/images/regression/lossless_indexed_2bit_palette.webp
VP8L_SHAPE width=4 height=1 cache=false groups=1 meta_bits=0 literals=4 backrefs=0 backref_pixels=0 cache_refs=0 dist1=0 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=0
VP8L_SHAPE width=58 height=128 cache=false groups=1 meta_bits=0 literals=677 backrefs=207 backref_pixels=6747 cache_refs=0 dist1=17 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=190
FILE /home/runner/work/image-webp/image-webp/tests/images/regression/lossless_indexed_4bit_palette.webp
VP8L_SHAPE width=15 height=1 cache=false groups=1 meta_bits=0 literals=15 backrefs=0 backref_pixels=0 cache_refs=0 dist1=0 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=0
VP8L_SHAPE width=32 height=38 cache=false groups=1 meta_bits=0 literals=638 backrefs=90 backref_pixels=578 cache_refs=0 dist1=35 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=55
VP8L_SHAPE width=250 height=300 cache=true groups=2 meta_bits=3 literals=908 backrefs=7494 backref_pixels=71999 cache_refs=1734 dist1=74 dist2=13 dist3_4=23 dist5_16=9 dist_gt16=7375
FILE /home/runner/work/image-webp/image-webp/tests/images/regression/tiny.webp
VP8L_SHAPE width=27 height=1 cache=false groups=1 meta_bits=0 literals=27 backrefs=0 backref_pixels=0 cache_refs=0 dist1=0 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=0
VP8L_SHAPE width=10 height=7 cache=false groups=1 meta_bits=0 literals=70 backrefs=0 backref_pixels=0 cache_refs=0 dist1=0 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=0
```

## Generated 2048x2048 lossless image

```text
FILE /tmp/large.webp
VP8L_SHAPE width=128 height=128 cache=false groups=1 meta_bits=0 literals=4 backrefs=4 backref_pixels=16380 cache_refs=0 dist1=4 dist2=0 dist3_4=0 dist5_16=0 dist_gt16=0
VP8L_SHAPE width=128 height=128 cache=false groups=1 meta_bits=0 literals=172 backrefs=291 backref_pixels=16212 cache_refs=0 dist1=16 dist2=17 dist3_4=11 dist5_16=31 dist_gt16=216
VP8L_SHAPE width=32 height=32 cache=false groups=1 meta_bits=0 literals=137 backrefs=83 backref_pixels=887 cache_refs=0 dist1=11 dist2=6 dist3_4=6 dist5_16=4 dist_gt16=56
VP8L_SHAPE width=2048 height=2048 cache=true groups=18 meta_bits=6 literals=1711 backrefs=65688 backref_pixels=4171400 cache_refs=19479 dist1=1 dist2=1 dist3_4=6 dist5_16=718 dist_gt16=64962
```
