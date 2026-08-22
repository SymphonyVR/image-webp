from pathlib import Path

p = Path("src/lossless/decoder/huffman.rs")
s = p.read_text()
marker = '''    pub(crate) const fn is_single_node(&self) -> bool {
        matches!(self.0, HuffmanTreeInner::Single(_))
    }

'''
insert = marker + '''    /// Returns the symbol for a tree that contains exactly one symbol.
    pub(crate) const fn single_symbol(&self) -> Option<u16> {
        match self.0 {
            HuffmanTreeInner::Single(symbol) => Some(symbol),
            HuffmanTreeInner::Tree { .. } => None,
        }
    }

'''
if marker not in s:
    raise SystemExit("single-node marker missing")
p.write_text(s.replace(marker, insert, 1))

p = Path("src/lossless/decoder/mod.rs")
s = p.read_text()
old = '''        let mut hufftree_groups = Vec::new();

        for _i in 0..num_huff_groups {
            let mut group: HuffmanCodeGroup = Default::default();
'''
new = '''        let mut hufftree_groups = Vec::new();
        let mut trivial_literals = Vec::new();

        for _i in 0..num_huff_groups {
            let mut group: HuffmanCodeGroup = Default::default();
'''
if old not in s:
    raise SystemExit("huffman group vector marker missing")
s = s.replace(old, new, 1)

old = '''                let tree = self.read_huffman_code(alphabet_size)?;
                group[j] = tree;
            }
            hufftree_groups.push(group);
        }
'''
new = '''                let tree = self.read_huffman_code(alphabet_size)?;
                group[j] = tree;
            }
            let trivial_literal = match (
                group[RED].single_symbol(),
                group[BLUE].single_symbol(),
                group[ALPHA].single_symbol(),
            ) {
                (Some(red), Some(blue), Some(alpha)) => {
                    debug_assert!(red < 256 && blue < 256 && alpha < 256);
                    Some([red as u8, blue as u8, alpha as u8])
                }
                _ => None,
            };
            trivial_literals.push(trivial_literal);
            hufftree_groups.push(group);
        }
'''
if old not in s:
    raise SystemExit("group completion marker missing")
s = s.replace(old, new, 1)

old = '''            huffman_code_groups: hufftree_groups,
        };
'''
new = '''            huffman_code_groups: hufftree_groups,
            trivial_literals,
        };
'''
if old not in s:
    raise SystemExit("HuffmanInfo construction marker missing")
s = s.replace(old, new, 1)

old = '''        let huff_index = huffman_info.get_huff_index(0, 0);
        let mut tree = &huffman_info.huffman_code_groups[huff_index];
        let mut index = 0;
'''
new = '''        let huff_index = huffman_info.get_huff_index(0, 0);
        let mut tree = &huffman_info.huffman_code_groups[huff_index];
        let mut trivial_literal = huffman_info.trivial_literals[huff_index];
        let mut index = 0;
'''
if old not in s:
    raise SystemExit("initial huffman group marker missing")
s = s.replace(old, new, 1)

old = '''                let huff_index = huffman_info.get_huff_index(x as u16, y as u16);
                tree = &huffman_info.huffman_code_groups[huff_index];

                // Fast path: If all the codes each contain only a single
'''
new = '''                let huff_index = huffman_info.get_huff_index(x as u16, y as u16);
                tree = &huffman_info.huffman_code_groups[huff_index];
                trivial_literal = huffman_info.trivial_literals[huff_index];

                // Fast path: If all the codes each contain only a single
'''
if old not in s:
    raise SystemExit("huffman group switch marker missing")
s = s.replace(old, new, 1)

old = '''                let green = code as u8;
                let red = tree[RED].read_symbol(&mut self.bit_reader)? as u8;
                let blue = tree[BLUE].read_symbol(&mut self.bit_reader)? as u8;
                if self.bit_reader.nbits < 15 {
                    self.bit_reader.fill()?;
                }
                let alpha = tree[ALPHA].read_symbol(&mut self.bit_reader)? as u8;

                data[index * 4] = red;
                data[index * 4 + 1] = green;
                data[index * 4 + 2] = blue;
                data[index * 4 + 3] = alpha;

                if let Some(color_cache) = huffman_info.color_cache.as_mut() {
                    color_cache.insert([red, green, blue, alpha]);
                }
'''
new = '''                let green = code as u8;
                let [red, blue, alpha] = if let Some(fixed) = trivial_literal {
                    fixed
                } else {
                    let red = tree[RED].read_symbol(&mut self.bit_reader)? as u8;
                    let blue = tree[BLUE].read_symbol(&mut self.bit_reader)? as u8;
                    if self.bit_reader.nbits < 15 {
                        self.bit_reader.fill()?;
                    }
                    let alpha = tree[ALPHA].read_symbol(&mut self.bit_reader)? as u8;
                    [red, blue, alpha]
                };

                data[index * 4] = red;
                data[index * 4 + 1] = green;
                data[index * 4 + 2] = blue;
                data[index * 4 + 3] = alpha;

                if let Some(color_cache) = huffman_info.color_cache.as_mut() {
                    color_cache.insert([red, green, blue, alpha]);
                }
'''
if old not in s:
    raise SystemExit("literal path marker missing")
s = s.replace(old, new, 1)

old = '''    huffman_code_groups: Vec<HuffmanCodeGroup>,
}
'''
new = '''    huffman_code_groups: Vec<HuffmanCodeGroup>,
    trivial_literals: Vec<Option<[u8; 3]>>,
}
'''
if old not in s:
    raise SystemExit("HuffmanInfo field marker missing")
s = s.replace(old, new, 1)

p.write_text(s)
