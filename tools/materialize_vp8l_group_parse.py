#!/usr/bin/env python3
from pathlib import Path

p = Path('src/lossless/decoder/mod.rs')
s = p.read_text()
s = s.replace('use huffman::HuffmanTree;', 'use huffman::{HuffmanTree, HuffmanTree11, HuffmanTree9};', 1)
old = 'type HuffmanCodeGroup = [HuffmanTree; HUFFMAN_CODES_PER_META_CODE];'
new = '''type HuffmanCodeGroup9 = [HuffmanTree9; HUFFMAN_CODES_PER_META_CODE];
type HuffmanCodeGroup11 = [HuffmanTree11; HUFFMAN_CODES_PER_META_CODE];

#[derive(Debug, Clone)]
enum HuffmanCodeGroup {
    Normal(HuffmanCodeGroup9),
    Wide(HuffmanCodeGroup11),
}

#[derive(Debug)]
enum HuffmanCodeSpec {
    Single(u16),
    Two(u16, u16),
    Implicit(Vec<u16>),
}

impl HuffmanCodeSpec {
    fn prefers_wide_root(&self) -> bool {
        let Self::Implicit(code_lengths) = self else {
            return false;
        };
        let mut symbols = 0usize;
        let mut long_symbols = 0usize;
        for &length in code_lengths {
            if length != 0 {
                symbols += 1;
                if length > 9 {
                    long_symbols += 1;
                }
            }
        }
        symbols >= 256 && long_symbols * 8 >= symbols
    }

    fn build<const TABLE_BITS: u8>(self) -> Result<HuffmanTree<TABLE_BITS>, DecodingError> {
        match self {
            Self::Single(symbol) => Ok(HuffmanTree::build_single_node(symbol)),
            Self::Two(zero, one) => Ok(HuffmanTree::build_two_node(zero, one)),
            Self::Implicit(code_lengths) => HuffmanTree::build_implicit(code_lengths),
        }
    }
}'''
assert old in s
s = s.replace(old, new, 1)
old = '''        for _i in 0..num_huff_groups {
            let mut group: HuffmanCodeGroup = Default::default();
            for j in 0..HUFFMAN_CODES_PER_META_CODE {
                let mut alphabet_size = ALPHABET_SIZE[j];
                if j == 0 {
                    if let Some(color_cache) = color_cache.as_ref() {
                        alphabet_size += 1 << color_cache.color_cache_bits;
                    }
                }

                let tree = self.read_huffman_code(alphabet_size)?;
                group[j] = tree;
            }
            hufftree_groups.push(group);
        }
'''
new = '''        for _i in 0..num_huff_groups {
            let mut specs = Vec::with_capacity(HUFFMAN_CODES_PER_META_CODE);
            for (j, &base_alphabet_size) in ALPHABET_SIZE.iter().enumerate() {
                let mut alphabet_size = base_alphabet_size;
                if j == 0 {
                    if let Some(color_cache) = color_cache.as_ref() {
                        alphabet_size += 1 << color_cache.color_cache_bits;
                    }
                }
                specs.push(self.read_huffman_code_spec(alphabet_size)?);
            }

            let use_wide_root = specs.iter().any(HuffmanCodeSpec::prefers_wide_root);
            if use_wide_root {
                let trees: Vec<HuffmanTree11> = specs
                    .into_iter()
                    .map(HuffmanCodeSpec::build::<11>)
                    .collect::<Result<_, _>>()?;
                let group: HuffmanCodeGroup11 = trees
                    .try_into()
                    .map_err(|_| DecodingError::HuffmanError)?;
                hufftree_groups.push(HuffmanCodeGroup::Wide(group));
            } else {
                let trees: Vec<HuffmanTree9> = specs
                    .into_iter()
                    .map(HuffmanCodeSpec::build::<9>)
                    .collect::<Result<_, _>>()?;
                let group: HuffmanCodeGroup9 = trees
                    .try_into()
                    .map_err(|_| DecodingError::HuffmanError)?;
                hufftree_groups.push(HuffmanCodeGroup::Normal(group));
            }
        }
'''
assert old in s
s = s.replace(old, new, 1)
start = s.index('    /// Decodes and returns a single huffman tree\n    fn read_huffman_code')
end = s.index('    /// Reads huffman code lengths', start)
reader = '''    /// Parses a final-image Huffman tree before choosing a group root width.
    fn read_huffman_code_spec(
        &mut self,
        alphabet_size: u16,
    ) -> Result<HuffmanCodeSpec, DecodingError> {
        let simple = self.bit_reader.read_bits::<u8>(1)? == 1;
        if simple {
            let num_symbols = self.bit_reader.read_bits::<u8>(1)? + 1;
            let is_first_8bits = self.bit_reader.read_bits::<u8>(1)?;
            let zero_symbol = self.bit_reader.read_bits::<u16>(1 + 7 * is_first_8bits)?;
            if zero_symbol >= alphabet_size {
                return Err(DecodingError::BitStreamError);
            }
            if num_symbols == 1 {
                Ok(HuffmanCodeSpec::Single(zero_symbol))
            } else {
                let one_symbol = self.bit_reader.read_bits::<u16>(8)?;
                if one_symbol >= alphabet_size {
                    return Err(DecodingError::BitStreamError);
                }
                Ok(HuffmanCodeSpec::Two(zero_symbol, one_symbol))
            }
        } else {
            let mut code_length_code_lengths = vec![0; CODE_LENGTH_CODES];
            let num_code_lengths = 4 + self.bit_reader.read_bits::<usize>(4)?;
            for i in 0..num_code_lengths {
                code_length_code_lengths[CODE_LENGTH_CODE_ORDER[i]] =
                    self.bit_reader.read_bits(3)?;
            }
            let code_lengths =
                self.read_huffman_code_lengths(code_length_code_lengths, alphabet_size)?;
            Ok(HuffmanCodeSpec::Implicit(code_lengths))
        }
    }

'''
s = s[:start] + reader + s[end:]
s = s.replace(
    '        let table = HuffmanTree::build_implicit(code_length_code_lengths)?;',
    '        let table = HuffmanTree9::build_implicit(code_length_code_lengths)?;',
    1,
)
p.write_text(s)
