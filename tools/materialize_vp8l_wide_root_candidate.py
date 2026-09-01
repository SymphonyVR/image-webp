#!/usr/bin/env python3
from pathlib import Path

p=Path('src/lossless/decoder/huffman.rs');s=p.read_text()
s=s.replace('const MAX_TABLE_BITS: u8 = 9;','const MAX_TABLE_BITS: u8 = 9;\nconst WIDE_TABLE_BITS: u8 = 11;',1)
old='''    Tree {
        table_mask: u16,
        primary_table: Vec<u16>,
        secondary_table: Vec<u16>,
    },'''
new=old+'''\n    WideTree {
        table_mask: u16,
        primary_table: Vec<u16>,
        secondary_table: Vec<u16>,
    },'''
assert old in s;s=s.replace(old,new,1)
old='        let table_bits = (max_length as u16).min(u16::from(MAX_TABLE_BITS));'
new='''        let long_symbols: usize = histogram[10..=MAX_ALLOWED_CODE_LENGTH].iter().sum();
        let use_wide = num_symbols >= 256 && long_symbols * 8 >= num_symbols;
        let max_table_bits = if use_wide {
            WIDE_TABLE_BITS
        } else {
            MAX_TABLE_BITS
        };
        let table_bits = (max_length as u16).min(u16::from(max_table_bits));'''
assert old in s;s=s.replace(old,new,1)
old='''        Ok(Self(HuffmanTreeInner::Tree {
            table_mask,
            primary_table,
            secondary_table,
        }))'''
new='''        let inner = if use_wide && table_bits > u16::from(MAX_TABLE_BITS) {
            HuffmanTreeInner::WideTree {
                table_mask,
                primary_table,
                secondary_table,
            }
        } else {
            HuffmanTreeInner::Tree {
                table_mask,
                primary_table,
                secondary_table,
            }
        };
        Ok(Self(inner))'''
assert old in s;s=s.replace(old,new,1)
marker='    /// Reads a symbol using the bit reader.\n'
wide='''    #[inline(never)]
    fn read_symbol_wide_slowpath<R: BufRead>(
        secondary_table: &[u16],
        v: u16,
        primary_table_entry: u16,
        bit_reader: &mut BitReader<R>,
    ) -> Result<u16, DecodingError> {
        let length = primary_table_entry >> 12;
        let mask = (1 << (length - WIDE_TABLE_BITS as u16)) - 1;
        let secondary_index = ((primary_table_entry & 0xfff) as usize)
            + ((v >> WIDE_TABLE_BITS) as usize & mask as usize);
        let secondary_entry = secondary_table[secondary_index];
        bit_reader.consume((secondary_entry & 0xf) as u8)?;
        Ok(secondary_entry >> 4)
    }

'''
assert marker in s;s=s.replace(marker,wide+marker,1)
anchor='            HuffmanTreeInner::Single(symbol) => Ok(*symbol),\n'
wide_arm='''            HuffmanTreeInner::WideTree {
                primary_table,
                secondary_table,
                table_mask,
            } => {
                let v = bit_reader.peek_full() as u16;
                let entry = primary_table[(v & table_mask) as usize];
                if (entry >> 12) <= WIDE_TABLE_BITS as u16 {
                    bit_reader.consume((entry >> 12) as u8)?;
                    return Ok(entry & 0xfff);
                }
                Self::read_symbol_wide_slowpath(secondary_table, v, entry, bit_reader)
            }
'''
assert anchor in s;s=s.replace(anchor,wide_arm+anchor,1)
anchor='            HuffmanTreeInner::Single(symbol) => Some((0, *symbol)),\n'
wide_arm='''            HuffmanTreeInner::WideTree {
                primary_table,
                table_mask,
                ..
            } => {
                let v = bit_reader.peek_full() as u16;
                let entry = primary_table[(v & table_mask) as usize];
                if (entry >> 12) <= WIDE_TABLE_BITS as u16 {
                    return Some(((entry >> 12) as u8, entry & 0xfff));
                }
                None
            }
'''
assert anchor in s;s=s.replace(anchor,wide_arm+anchor,1)
p.write_text(s)
