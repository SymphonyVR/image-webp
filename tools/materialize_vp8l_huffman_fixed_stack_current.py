#!/usr/bin/env python3
from pathlib import Path

hp = Path('src/lossless/decoder/huffman.rs')
mp = Path('src/lossless/decoder/mod.rs')
h = hp.read_text()
m = mp.read_text()

old = 'pub(crate) fn build_implicit(code_lengths: Vec<u16>) -> Result<Self, DecodingError> {'
new = 'pub(crate) fn build_implicit(code_lengths: impl AsRef<[u16]>) -> Result<Self, DecodingError> {\n        let code_lengths = code_lengths.as_ref();'
assert old in h
h = h.replace(old, new, 1)

old = '''        let mut hufftree_groups = Vec::new();

        for _i in 0..num_huff_groups {
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
                let group: HuffmanCodeGroup11 =
                    trees.try_into().map_err(|_| DecodingError::HuffmanError)?;
                hufftree_groups.push(HuffmanCodeGroup::Wide(group));
            } else {
                let trees: Vec<HuffmanTree9> = specs
                    .into_iter()
                    .map(HuffmanCodeSpec::build::<9>)
                    .collect::<Result<_, _>>()?;
                let group: HuffmanCodeGroup9 =
                    trees.try_into().map_err(|_| DecodingError::HuffmanError)?;
                hufftree_groups.push(HuffmanCodeGroup::Normal(group));
            }
        }
'''
new = '''        let mut hufftree_groups = Vec::with_capacity(num_huff_groups as usize);

        for _i in 0..num_huff_groups {
            let mut specs: [Option<HuffmanCodeSpec>; HUFFMAN_CODES_PER_META_CODE] =
                [None, None, None, None, None];
            for (j, &base_alphabet_size) in ALPHABET_SIZE.iter().enumerate() {
                let mut alphabet_size = base_alphabet_size;
                if j == 0 {
                    if let Some(color_cache) = color_cache.as_ref() {
                        alphabet_size += 1 << color_cache.color_cache_bits;
                    }
                }
                specs[j] = Some(self.read_huffman_code_spec(alphabet_size)?);
            }

            let use_wide_root = specs
                .iter()
                .filter_map(Option::as_ref)
                .any(HuffmanCodeSpec::prefers_wide_root);
            if use_wide_root {
                let group: HuffmanCodeGroup11 = [
                    specs[0].take().unwrap().build::<11>()?,
                    specs[1].take().unwrap().build::<11>()?,
                    specs[2].take().unwrap().build::<11>()?,
                    specs[3].take().unwrap().build::<11>()?,
                    specs[4].take().unwrap().build::<11>()?,
                ];
                hufftree_groups.push(HuffmanCodeGroup::Wide(group));
            } else {
                let group: HuffmanCodeGroup9 = [
                    specs[0].take().unwrap().build::<9>()?,
                    specs[1].take().unwrap().build::<9>()?,
                    specs[2].take().unwrap().build::<9>()?,
                    specs[3].take().unwrap().build::<9>()?,
                    specs[4].take().unwrap().build::<9>()?,
                ];
                hufftree_groups.push(HuffmanCodeGroup::Normal(group));
            }
        }
'''
assert old in m
m = m.replace(old, new, 1)

old = '''            let mut code_length_code_lengths = vec![0; CODE_LENGTH_CODES];
            let num_code_lengths = 4 + self.bit_reader.read_bits::<usize>(4)?;
'''
new = '''            let mut code_length_code_lengths = [0u16; CODE_LENGTH_CODES];
            let num_code_lengths = 4 + self.bit_reader.read_bits::<usize>(4)?;
'''
assert old in m
m = m.replace(old, new, 1)

old = '''            let code_lengths =
                self.read_huffman_code_lengths(code_length_code_lengths, alphabet_size)?;
'''
new = '''            let code_lengths =
                self.read_huffman_code_lengths(&code_length_code_lengths, alphabet_size)?;
'''
assert old in m
m = m.replace(old, new, 1)

old = '''        code_length_code_lengths: Vec<u16>,
        num_symbols: u16,
    ) -> Result<Vec<u16>, DecodingError> {
'''
new = '''        code_length_code_lengths: &[u16],
        num_symbols: u16,
    ) -> Result<Vec<u16>, DecodingError> {
'''
assert old in m
m = m.replace(old, new, 1)

hp.write_text(h)
mp.write_text(m)
