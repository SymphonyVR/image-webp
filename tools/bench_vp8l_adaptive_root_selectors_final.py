#!/usr/bin/env python3
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('basebench','tools/bench_vp8l_adaptive_root_final.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.TMP=Path('/tmp/vp8l-adaptive-root-selectors-final')
m.VARIANTS=[
 ('r9',None),
 ('dyn9','9u8'),
 ('n256q8r10','if num_symbols >= 256 && long_symbols * 8 >= num_symbols { 10 } else { 9 }'),
 ('n256q8r11','if num_symbols >= 256 && long_symbols * 8 >= num_symbols { 11 } else { 9 }'),
 ('n256q4r10','if num_symbols >= 256 && long_symbols * 4 >= num_symbols { 10 } else { 9 }'),
 ('n256q4r11','if num_symbols >= 256 && long_symbols * 4 >= num_symbols { 11 } else { 9 }'),
 ('n192q8r10','if num_symbols >= 192 && long_symbols * 8 >= num_symbols { 10 } else { 9 }'),
 ('n192q8r11','if num_symbols >= 192 && long_symbols * 8 >= num_symbols { 11 } else { 9 }'),
]
m.main()
