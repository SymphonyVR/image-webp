#!/usr/bin/env python3
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("orig_meta_run_skip", HERE / "bench_vp8l_meta_run_skip.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def add_precompute(s):
    marker = '''        let huffman_mask = if huffman_bits == 0 {\n'''
    add = '''        let mut run_ends = vec![0u16; entropy_image.len()];\n        if huffman_bits != 0 {\n            let w = usize::from(huffman_xsize);\n            for (row_idx, row) in entropy_image.chunks_exact(w).enumerate() {\n                let mut end = w as u16;\n                for x in (0..w).rev() {\n                    if x + 1 == w || row[x] != row[x + 1] {\n                        end = (x + 1) as u16;\n                    }\n                    run_ends[row_idx * w + x] = end;\n                }\n            }\n        }\n\n'''
    if marker not in s:
        raise SystemExit('mask marker')
    s = s.replace(marker, add + marker, 1)

    old = '''            huffman_code_groups: hufftree_groups,\n        };\n'''
    new = '''            huffman_code_groups: hufftree_groups,\n            run_ends,\n        };\n'''
    if old not in s:
        raise SystemExit('info init marker')
    s = s.replace(old, new, 1)

    old = '''    huffman_code_groups: Vec<HuffmanCodeGroup>,\n}\n'''
    new = '''    huffman_code_groups: Vec<HuffmanCodeGroup>,\n    run_ends: Vec<u16>,\n}\n'''
    if old not in s:
        raise SystemExit('info struct marker')
    return s.replace(old, new, 1)


def add_const(s, root):
    hp = root / 'src/lossless/decoder/huffman.rs'
    h = hp.read_text()
    marker = '''    pub(crate) const fn is_single_node(&self) -> bool {\n        matches!(self.0, HuffmanTreeInner::Single(_))\n    }\n'''
    helper = '''    pub(crate) const fn single_symbol(&self) -> Option<u16> {\n        match self.0 {\n            HuffmanTreeInner::Single(symbol) => Some(symbol),\n            HuffmanTreeInner::Tree { .. } => None,\n        }\n    }\n\n'''
    if marker not in h:
        raise SystemExit('single marker')
    hp.write_text(h.replace(marker, helper + marker, 1))

    old = '''        let mut hufftree_groups = Vec::new();\n\n        for _i in 0..num_huff_groups {\n'''
    new = '''        let mut hufftree_groups = Vec::new();\n        let mut single_pixels = Vec::new();\n\n        for _i in 0..num_huff_groups {\n'''
    if old not in s:
        raise SystemExit('group vector marker')
    s = s.replace(old, new, 1)

    old = '''            hufftree_groups.push(group);\n        }\n\n'''
    new = '''            let single_pixel = match (\n                group[RED].single_symbol(),\n                group[GREEN].single_symbol(),\n                group[BLUE].single_symbol(),\n                group[ALPHA].single_symbol(),\n            ) {\n                (Some(r), Some(g), Some(b), Some(a))\n                    if r < 256 && g < 256 && b < 256 && a < 256 =>\n                {\n                    Some([r as u8, g as u8, b as u8, a as u8])\n                }\n                _ => None,\n            };\n            single_pixels.push(single_pixel);\n            hufftree_groups.push(group);\n        }\n\n'''
    if old not in s:
        raise SystemExit('group end marker')
    s = s.replace(old, new, 1)

    old = '''            huffman_code_groups: hufftree_groups,\n            run_ends,\n'''
    new = '''            huffman_code_groups: hufftree_groups,\n            run_ends,\n            single_pixels,\n'''
    if old not in s:
        raise SystemExit('single pixels init marker')
    s = s.replace(old, new, 1)

    old = '''    run_ends: Vec<u16>,\n}\n'''
    new = '''    run_ends: Vec<u16>,\n    single_pixels: Vec<Option<[u8; 4]>>,\n}\n'''
    if old not in s:
        raise SystemExit('single pixels struct marker')
    s = s.replace(old, new, 1)

    oldfast = '''                if tree[..4].iter().all(|t| t.is_single_node()) {\n                    let code = tree[GREEN].read_symbol(&mut self.bit_reader)?;\n                    if code < 256 {\n                        let n = if huffman_info.bits == 0 {\n                            num_values\n                        } else {\n                            next_block_start - index\n                        };\n\n                        let red = tree[RED].read_symbol(&mut self.bit_reader)?;\n                        let blue = tree[BLUE].read_symbol(&mut self.bit_reader)?;\n                        let alpha = tree[ALPHA].read_symbol(&mut self.bit_reader)?;\n                        let value = [red as u8, code as u8, blue as u8, alpha as u8];\n\n                        for i in 0..n {\n                            data[index * 4 + i * 4..][..4].copy_from_slice(&value);\n                        }\n\n                        if let Some(color_cache) = huffman_info.color_cache.as_mut() {\n                            color_cache.insert(value);\n                        }\n\n                        index += n;\n                        continue;\n                    }\n                }\n'''
    newfast = '''                if let Some(value) = huffman_info.single_pixels[huff_index] {\n                    let n = if huffman_info.bits == 0 {\n                        num_values\n                    } else {\n                        next_block_start - index\n                    };\n                    for i in 0..n {\n                        data[index * 4 + i * 4..][..4].copy_from_slice(&value);\n                    }\n                    if let Some(color_cache) = huffman_info.color_cache.as_mut() {\n                        color_cache.insert(value);\n                    }\n                    index += n;\n                    continue;\n                }\n'''
    if oldfast not in s:
        raise SystemExit('fast marker')
    return s.replace(oldfast, newfast, 1)


def patch(n, r):
    p = r / 'src/lossless/decoder/mod.rs'
    s = p.read_text()
    if n == 'scan':
        if m.OLD_ELSE not in s:
            raise SystemExit('scan else marker')
        s = s.replace(m.OLD_ELSE, m.SCAN_ELSE, 1)
    else:
        s = add_precompute(s)
        if m.OLD_ELSE not in s:
            raise SystemExit('pre else marker')
        s = s.replace(m.OLD_ELSE, m.PRE_ELSE, 1)
        if n == 'pre_const':
            s = add_const(s, r)
    p.write_text(s)


m.add_precompute = add_precompute
m.add_const = add_const
m.patch = patch
m.main()
