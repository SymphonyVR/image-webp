from pathlib import Path

# Expose the small amount of Huffman metadata needed to build a packed literal table.
p = Path("src/lossless/decoder/huffman.rs")
s = p.read_text()
marker = '''    pub(crate) const fn is_single_node(&self) -> bool {
        matches!(self.0, HuffmanTreeInner::Single(_))
    }

'''
insert = marker + '''    /// Returns the longest codeword represented by this tree.
    ///
    /// This is used only while constructing optional fast decode tables.
    pub(crate) fn max_code_length(&self) -> u8 {
        match &self.0 {
            HuffmanTreeInner::Single(_) => 0,
            HuffmanTreeInner::Tree {
                primary_table,
                secondary_table,
                ..
            } => {
                let primary = primary_table
                    .iter()
                    .map(|entry| (entry >> 12) as u8)
                    .max()
                    .unwrap_or(0);
                let secondary = secondary_table
                    .iter()
                    .map(|entry| (entry & 0xf) as u8)
                    .max()
                    .unwrap_or(0);
                primary.max(secondary)
            }
        }
    }

    /// Peeks a symbol from an explicitly supplied bit window when it fits in
    /// the primary table. The bit reader itself is not modified.
    pub(crate) fn peek_symbol_from_bits(&self, bits: u64) -> Option<(u8, u16)> {
        match &self.0 {
            HuffmanTreeInner::Single(symbol) => Some((0, *symbol)),
            HuffmanTreeInner::Tree {
                primary_table,
                table_mask,
                ..
            } => {
                let entry = primary_table[(bits as u16 & table_mask) as usize];
                let length = (entry >> 12) as u8;
                (length <= MAX_TABLE_BITS).then_some((length, entry & 0xfff))
            }
        }
    }

'''
if marker not in s:
    raise SystemExit("HuffmanTree metadata insertion marker missing")
p.write_text(s.replace(marker, insert, 1))

p = Path("src/lossless/decoder/mod.rs")
s = p.read_text()
old = '''use std::io::BufRead;
use std::mem;
'''
new = '''use std::io::BufRead;
use std::mem;
use std::ops::{Index, IndexMut};
'''
if old not in s:
    raise SystemExit("std import marker missing")
s = s.replace(old, new, 1)

old = '''type HuffmanCodeGroup = [HuffmanTree; HUFFMAN_CODES_PER_META_CODE];

const ALPHABET_SIZE: [u16; HUFFMAN_CODES_PER_META_CODE] = [256 + 24, 256, 256, 256, 40];
'''
new = '''const PACKED_LITERAL_BITS: u8 = 6;
const PACKED_LITERAL_TABLE_SIZE: usize = 1 << PACKED_LITERAL_BITS;

#[derive(Clone, Copy, Debug, Default)]
struct PackedLiteralEntry {
    bits: u8,
    green_code: u16,
    rgba: [u8; 4],
}

#[derive(Clone, Debug, Default)]
struct HuffmanCodeGroup {
    trees: [HuffmanTree; HUFFMAN_CODES_PER_META_CODE],
    packed_literals: Option<Box<[PackedLiteralEntry; PACKED_LITERAL_TABLE_SIZE]>>,
}

impl Index<usize> for HuffmanCodeGroup {
    type Output = HuffmanTree;

    fn index(&self, index: usize) -> &Self::Output {
        &self.trees[index]
    }
}

impl IndexMut<usize> for HuffmanCodeGroup {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        &mut self.trees[index]
    }
}

const ALPHABET_SIZE: [u16; HUFFMAN_CODES_PER_META_CODE] = [256 + 24, 256, 256, 256, 40];
'''
if old not in s:
    raise SystemExit("HuffmanCodeGroup marker missing")
s = s.replace(old, new, 1)

marker = '''    /// Reads huffman codes associated with an image
    #[inline(never)]
    fn read_huffman_codes(
'''
helper = '''    fn build_packed_literal_table(
        trees: &[HuffmanTree; HUFFMAN_CODES_PER_META_CODE],
    ) -> Option<Box<[PackedLiteralEntry; PACKED_LITERAL_TABLE_SIZE]>> {
        let max_literal_bits: u8 = trees[..=ALPHA]
            .iter()
            .map(HuffmanTree::max_code_length)
            .sum();
        if max_literal_bits >= PACKED_LITERAL_BITS {
            return None;
        }

        let mut table = Box::new([PackedLiteralEntry::default(); PACKED_LITERAL_TABLE_SIZE]);
        for (input_bits, entry) in table.iter_mut().enumerate() {
            let mut bits = input_bits as u64;
            let (green_bits, green) = trees[GREEN].peek_symbol_from_bits(bits)?;
            if green >= 256 {
                *entry = PackedLiteralEntry {
                    bits: green_bits,
                    green_code: green,
                    rgba: [0; 4],
                };
                continue;
            }
            bits >>= green_bits;

            let (red_bits, red) = trees[RED].peek_symbol_from_bits(bits)?;
            bits >>= red_bits;
            let (blue_bits, blue) = trees[BLUE].peek_symbol_from_bits(bits)?;
            bits >>= blue_bits;
            let (alpha_bits, alpha) = trees[ALPHA].peek_symbol_from_bits(bits)?;

            debug_assert!(red < 256 && blue < 256 && alpha < 256);
            *entry = PackedLiteralEntry {
                bits: green_bits + red_bits + blue_bits + alpha_bits,
                green_code: green,
                rgba: [red as u8, green as u8, blue as u8, alpha as u8],
            };
        }
        Some(table)
    }

''' + marker
if marker not in s:
    raise SystemExit("read_huffman_codes insertion marker missing")
s = s.replace(marker, helper, 1)

old = '''            for j in 0..HUFFMAN_CODES_PER_META_CODE {
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
'''
new = '''            for j in 0..HUFFMAN_CODES_PER_META_CODE {
                let mut alphabet_size = ALPHABET_SIZE[j];
                if j == 0 {
                    if let Some(color_cache) = color_cache.as_ref() {
                        alphabet_size += 1 << color_cache.color_cache_bits;
                    }
                }

                let tree = self.read_huffman_code(alphabet_size)?;
                group[j] = tree;
            }
            group.packed_literals = Self::build_packed_literal_table(&group.trees);
            hufftree_groups.push(group);
'''
if old not in s:
    raise SystemExit("Huffman group construction marker missing")
s = s.replace(old, new, 1)

old = '''                if tree[..4].iter().all(|t| t.is_single_node()) {
'''
new = '''                if tree.trees[..4].iter().all(|t| t.is_single_node()) {
'''
if old not in s:
    raise SystemExit("trivial group slice marker missing")
s = s.replace(old, new, 1)

old = '''            let code = tree[GREEN].read_symbol(&mut self.bit_reader)?;

            //check code
            if code < 256 {
                //literal, so just use huffman codes and read as argb
                let green = code as u8;
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
                index += 1;
'''
new = '''            let code = if let Some(packed_literals) = tree.packed_literals.as_ref() {
                let entry = packed_literals[self.bit_reader.peek(PACKED_LITERAL_BITS) as usize];
                self.bit_reader.consume(entry.bits)?;
                if entry.green_code < 256 {
                    data[index * 4..][..4].copy_from_slice(&entry.rgba);
                    if let Some(color_cache) = huffman_info.color_cache.as_mut() {
                        color_cache.insert(entry.rgba);
                    }
                    index += 1;
                    continue;
                }
                entry.green_code
            } else {
                tree[GREEN].read_symbol(&mut self.bit_reader)?
            };

            //check code
            if code < 256 {
                //literal, so just use huffman codes and read as argb
                let green = code as u8;
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
                index += 1;
'''
if old not in s:
    raise SystemExit("literal decode marker missing")
s = s.replace(old, new, 1)

p.write_text(s)
