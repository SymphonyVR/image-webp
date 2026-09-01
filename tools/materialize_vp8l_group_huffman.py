#!/usr/bin/env python3
from pathlib import Path

p = Path('src/lossless/decoder/huffman.rs')
s = p.read_text()
s = s.replace('const MAX_TABLE_BITS: u8 = 9;\n', '', 1)
old = 'pub(crate) struct HuffmanTree(HuffmanTreeInner);'
new = '''pub(crate) struct HuffmanTree<const TABLE_BITS: u8>(HuffmanTreeInner);

pub(crate) type HuffmanTree9 = HuffmanTree<9>;
pub(crate) type HuffmanTree11 = HuffmanTree<11>;'''
assert old in s
s = s.replace(old, new, 1)
s = s.replace('impl Default for HuffmanTree {', 'impl<const TABLE_BITS: u8> Default for HuffmanTree<TABLE_BITS> {', 1)
s = s.replace('impl HuffmanTree {', 'impl<const TABLE_BITS: u8> HuffmanTree<TABLE_BITS> {', 1)
s = s.replace('MAX_TABLE_BITS', 'TABLE_BITS')
p.write_text(s)
