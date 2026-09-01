#!/usr/bin/env python3
from pathlib import Path
import runpy
src=Path('tools/bench_vp8l_predictor_closure.py').read_text()
src=src.replace("VS=['index','fuse','traverse','direct','avg','packed','p11','all']","VS=['packed']",1)
src=src.replace("for rnd in range(1,12):","for rnd in range(1,26):",1)
src=src.replace("bench',45","bench',70",1)
src=src.replace("bench',3","bench',5",1)
src=src.replace("# VP8L predictor closure matrix","# Strict VP8L packed-predictor confirmation",1)
src=src.replace("benchmark-vp8l-predictor-closure-v2.md","benchmark-vp8l-packed-predictor-confirm.md",1)
src=src.replace("'- hashes + tests + MSRV passed'","'- 25 alternating paired rounds; hashes + tests + MSRV passed'",1)
Path('/tmp/confirm_vp8l_packed_predictors_impl.py').write_text(src)
runpy.run_path('/tmp/confirm_vp8l_packed_predictors_impl.py',run_name='__main__')
