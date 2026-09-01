#!/usr/bin/env python3
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('basebench','tools/bench_vp8l_adaptive_root_final.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.TMP=Path('/tmp/vp8l-wide-mask-root-final')
m.VARIANTS=[
 ('r9',None),
 ('n256q16w10','10|num_symbols >= 256 && long_symbols * 16 >= num_symbols'),
 ('n256q16w11','11|num_symbols >= 256 && long_symbols * 16 >= num_symbols'),
 ('n256q8w10','10|num_symbols >= 256 && long_symbols * 8 >= num_symbols'),
 ('n256q8w11','11|num_symbols >= 256 && long_symbols * 8 >= num_symbols'),
 ('n192q8w11','11|num_symbols >= 192 && long_symbols * 8 >= num_symbols'),
]

def patch_wide_mask(root,selector):
    bits_s,expr=selector.split('|',1);wide=int(bits_s)
    p=root/'src/lossless/decoder/huffman.rs';s=p.read_text()
    old='        let table_bits = (max_length as u16).min(u16::from(MAX_TABLE_BITS));'
    new='''        let long_symbols: usize = histogram[10..=MAX_ALLOWED_CODE_LENGTH].iter().sum();
        let use_wide = '''+expr+''';
        let max_table_bits = if use_wide { '''+str(wide)+''' } else { MAX_TABLE_BITS };
        let table_bits = (max_length as u16).min(u16::from(max_table_bits));'''
    if old not in s: raise SystemExit('table anchor missing')
    s=s.replace(old,new,1)
    old='''    fn read_symbol_slowpath<R: BufRead>(
        secondary_table: &[u16],
        v: u16,
        primary_table_entry: u16,
        bit_reader: &mut BitReader<R>,
    ) -> Result<u16, DecodingError> {'''
    new='''    fn read_symbol_slowpath<R: BufRead>(
        secondary_table: &[u16],
        v: u16,
        primary_table_entry: u16,
        bit_reader: &mut BitReader<R>,
    ) -> Result<u16, DecodingError> {'''
    # keep the existing 9-bit slowpath byte-for-byte; add a separate rare wide slowpath.
    if old not in s: raise SystemExit('slowpath signature missing')
    marker='''    /// Reads a symbol using the bit reader.
'''
    wide_fn='''    #[inline(never)]
    fn read_symbol_wide_slowpath<R: BufRead>(
        secondary_table: &[u16],
        v: u16,
        primary_table_entry: u16,
        table_bits: u8,
        bit_reader: &mut BitReader<R>,
    ) -> Result<u16, DecodingError> {
        let length = primary_table_entry >> 12;
        let mask = (1 << (length - u16::from(table_bits))) - 1;
        let secondary_index = ((primary_table_entry & 0xfff) as usize)
            + ((v >> table_bits) as usize & mask as usize);
        let secondary_entry = secondary_table[secondary_index];
        bit_reader.consume((secondary_entry & 0xf) as u8)?;
        Ok(secondary_entry >> 4)
    }

'''
    if marker not in s: raise SystemExit('insert marker missing')
    s=s.replace(marker,wide_fn+marker,1)
    old='''                if (entry >> 12) <= MAX_TABLE_BITS as u16 {
                    bit_reader.consume((entry >> 12) as u8)?;
                    return Ok(entry & 0xfff);
                }

                Self::read_symbol_slowpath(secondary_table, v, entry, bit_reader)'''
    new='''                let length = entry >> 12;
                if length <= MAX_TABLE_BITS as u16 {
                    bit_reader.consume(length as u8)?;
                    return Ok(entry & 0xfff);
                }

                if *table_mask <= 0x1ff {
                    return Self::read_symbol_slowpath(secondary_table, v, entry, bit_reader);
                }
                let table_bits = if *table_mask <= 0x3ff { 10 } else { 11 };
                if length <= u16::from(table_bits) {
                    bit_reader.consume(length as u8)?;
                    return Ok(entry & 0xfff);
                }
                Self::read_symbol_wide_slowpath(
                    secondary_table,
                    v,
                    entry,
                    table_bits,
                    bit_reader,
                )'''
    if old not in s: raise SystemExit('read anchor missing')
    s=s.replace(old,new,1)
    old='''                if (entry >> 12) <= MAX_TABLE_BITS as u16 {
                    return Some(((entry >> 12) as u8, entry & 0xfff));
                }
                None'''
    new='''                let length = entry >> 12;
                if length <= MAX_TABLE_BITS as u16 {
                    return Some((length as u8, entry & 0xfff));
                }
                if *table_mask > 0x1ff {
                    let table_bits = if *table_mask <= 0x3ff { 10 } else { 11 };
                    if length <= u16::from(table_bits) {
                        return Some((length as u8, entry & 0xfff));
                    }
                }
                None'''
    if old not in s: raise SystemExit('peek anchor missing')
    s=s.replace(old,new,1)
    p.write_text(s)

m.patch_dynamic=patch_wide_mask
m.main()
