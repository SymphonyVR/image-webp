#!/usr/bin/env python3
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('basebench','tools/bench_vp8l_adaptive_root_final.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.TMP=Path('/tmp/vp8l-specialized-wide-root-final')
m.VARIANTS=[
 ('r9',None),
 ('n256q8w10','10|num_symbols >= 256 && long_symbols * 8 >= num_symbols'),
 ('n256q8w11','11|num_symbols >= 256 && long_symbols * 8 >= num_symbols'),
 ('n256q4w10','10|num_symbols >= 256 && long_symbols * 4 >= num_symbols'),
 ('n256q4w11','11|num_symbols >= 256 && long_symbols * 4 >= num_symbols'),
 ('n192q8w10','10|num_symbols >= 192 && long_symbols * 8 >= num_symbols'),
 ('n192q8w11','11|num_symbols >= 192 && long_symbols * 8 >= num_symbols'),
]

def patch_specialized(root,selector):
    bits_s,expr=selector.split('|',1);bits=int(bits_s)
    p=root/'src/lossless/decoder/huffman.rs';s=p.read_text()
    old='const MAX_TABLE_BITS: u8 = 9;'
    s=s.replace(old,old+f'\nconst WIDE_TABLE_BITS: u8 = {bits};',1)
    old_enum='''    Tree {
        table_mask: u16,
        primary_table: Vec<u16>,
        secondary_table: Vec<u16>,
    },'''
    new_enum=old_enum+'''\n    WideTree {
        table_mask: u16,
        primary_table: Vec<u16>,
        secondary_table: Vec<u16>,
    },'''
    if old_enum not in s:raise SystemExit('enum anchor missing')
    s=s.replace(old_enum,new_enum,1)
    old_bits='        let table_bits = (max_length as u16).min(u16::from(MAX_TABLE_BITS));'
    new_bits='        let long_symbols: usize = histogram[10..=MAX_ALLOWED_CODE_LENGTH].iter().sum();\n        let use_wide = '+expr+';\n        let max_table_bits = if use_wide { WIDE_TABLE_BITS } else { MAX_TABLE_BITS };\n        let table_bits = (max_length as u16).min(u16::from(max_table_bits));'
    if old_bits not in s:raise SystemExit('bits anchor missing')
    s=s.replace(old_bits,new_bits,1)
    old_ret='''        Ok(Self(HuffmanTreeInner::Tree {
            table_mask,
            primary_table,
            secondary_table,
        }))'''
    new_ret='''        let inner = if use_wide && table_bits > u16::from(MAX_TABLE_BITS) {
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
    if old_ret not in s:raise SystemExit('return anchor missing')
    s=s.replace(old_ret,new_ret,1)
    marker='''    /// Reads a symbol using the bit reader.
'''
    wide_fn='''    #[inline(never)]
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
    if marker not in s:raise SystemExit('slowpath insert anchor missing')
    s=s.replace(marker,wide_fn+marker,1)
    read_single='''            HuffmanTreeInner::Single(symbol) => Ok(*symbol),
'''
    wide_read='''            HuffmanTreeInner::WideTree {
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
    if read_single not in s:raise SystemExit('read match anchor missing')
    s=s.replace(read_single,wide_read+read_single,1)
    peek_single='''            HuffmanTreeInner::Single(symbol) => Some((0, *symbol)),
'''
    wide_peek='''            HuffmanTreeInner::WideTree {
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
    if peek_single not in s:raise SystemExit('peek match anchor missing')
    s=s.replace(peek_single,wide_peek+peek_single,1)
    p.write_text(s)

m.patch_dynamic=patch_specialized
m.main()
