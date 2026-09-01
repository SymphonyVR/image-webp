#!/usr/bin/env python3
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('basebench','tools/bench_vp8l_adaptive_root_final.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.TMP=Path('/tmp/vp8l-narrow-root-final')
m.VARIANTS=[
 ('r9',None),
 ('n256q16r8','num_symbols >= 256 && long_symbols * 16 >= num_symbols'),
 ('n256q8r8','num_symbols >= 256 && long_symbols * 8 >= num_symbols'),
 ('n256q4r8','num_symbols >= 256 && long_symbols * 4 >= num_symbols'),
 ('n192q8r8','num_symbols >= 192 && long_symbols * 8 >= num_symbols'),
 ('n128q8r8','num_symbols >= 128 && long_symbols * 8 >= num_symbols'),
]

def patch_narrow(root,selector):
    p=root/'src/lossless/decoder/huffman.rs';s=p.read_text()
    old='        let table_bits = (max_length as u16).min(u16::from(MAX_TABLE_BITS));'
    new='''        let long_symbols: usize = histogram[10..=MAX_ALLOWED_CODE_LENGTH].iter().sum();
        let use_narrow = '''+selector+''';
        let max_table_bits = if use_narrow { 8 } else { MAX_TABLE_BITS };
        let table_bits = (max_length as u16).min(u16::from(max_table_bits));'''
    if old not in s: raise SystemExit('table-bits anchor missing')
    s=s.replace(old,new,1)
    old='''    fn read_symbol_slowpath<R: BufRead>(
        secondary_table: &[u16],
        v: u16,
        primary_table_entry: u16,
        bit_reader: &mut BitReader<R>,
    ) -> Result<u16, DecodingError> {
        let length = primary_table_entry >> 12;
        let mask = (1 << (length - MAX_TABLE_BITS as u16)) - 1;
        let secondary_index = ((primary_table_entry & 0xfff) as usize)
            + ((v >> MAX_TABLE_BITS) as usize & mask as usize);'''
    new='''    fn read_symbol_slowpath<R: BufRead>(
        secondary_table: &[u16],
        v: u16,
        primary_table_entry: u16,
        table_mask: u16,
        bit_reader: &mut BitReader<R>,
    ) -> Result<u16, DecodingError> {
        let length = primary_table_entry >> 12;
        let table_bits = if table_mask & 0x100 == 0 { 8 } else { MAX_TABLE_BITS };
        let mask = (1 << (length - u16::from(table_bits))) - 1;
        let secondary_index = ((primary_table_entry & 0xfff) as usize)
            + ((v >> table_bits) as usize & mask as usize);'''
    if old not in s: raise SystemExit('slowpath anchor missing')
    s=s.replace(old,new,1)
    old='''                if (entry >> 12) <= MAX_TABLE_BITS as u16 {
                    bit_reader.consume((entry >> 12) as u8)?;
                    return Ok(entry & 0xfff);
                }

                Self::read_symbol_slowpath(secondary_table, v, entry, bit_reader)'''
    new='''                let length = entry >> 12;
                if length <= 8 || (length == 9 && table_mask & 0x100 != 0) {
                    bit_reader.consume(length as u8)?;
                    return Ok(entry & 0xfff);
                }

                Self::read_symbol_slowpath(secondary_table, v, entry, *table_mask, bit_reader)'''
    if old not in s: raise SystemExit('read anchor missing')
    s=s.replace(old,new,1)
    old='''                if (entry >> 12) <= MAX_TABLE_BITS as u16 {
                    return Some(((entry >> 12) as u8, entry & 0xfff));
                }'''
    new='''                let length = entry >> 12;
                if length <= 8 || (length == 9 && table_mask & 0x100 != 0) {
                    return Some((length as u8, entry & 0xfff));
                }'''
    if old not in s: raise SystemExit('peek anchor missing')
    s=s.replace(old,new,1)
    p.write_text(s)

m.patch_dynamic=patch_narrow
m.main()
