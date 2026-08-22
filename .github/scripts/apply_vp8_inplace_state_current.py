from pathlib import Path
p=Path('src/lossy/arithmetic_decoder.rs')
s=p.read_text()

def replace_fn(name, next_name, body):
    global s
    start=s.index(f'    fn {name}(')
    end=s.index(f'    fn {next_name}(', start)
    s=s[:start]+body+s[end:]

replace_fn('fast_read_bit','fast_read_flag',r'''    fn fast_read_bit(&mut self, probability: u8) -> bool {
        let chunks = self.chunks;
        let state = &mut self.uncommitted_state;

        if state.bit_count < 0 {
            let chunk = chunks.get(state.chunk_index).copied().unwrap_or_default();
            let v = u32::from_be_bytes(chunk);
            state.chunk_index += 1;
            state.value <<= 32;
            state.value |= u64::from(v);
            state.bit_count += 32;
        }
        debug_assert!(state.bit_count >= 0);

        debug_assert!((128..=255).contains(&state.range));
        let probability = u32::from(probability);
        let split = 1 + (((state.range - 1) * probability) >> 8);
        let bigsplit = u64::from(split) << state.bit_count;

        let retval = if let Some(new_value) = state.value.checked_sub(bigsplit) {
            state.range -= split;
            state.value = new_value;
            true
        } else {
            state.range = split;
            false
        };

        debug_assert!((1..=254).contains(&state.range));
        let shift = state.range.leading_zeros().saturating_sub(24);
        state.range <<= shift;
        state.bit_count -= shift as i32;

        debug_assert!((128..=254).contains(&state.range));
        retval
    }

''')
replace_fn('fast_read_flag','fast_read_sign',r'''    fn fast_read_flag(&mut self) -> bool {
        let chunks = self.chunks;
        let state = &mut self.uncommitted_state;

        if state.bit_count < 0 {
            let chunk = chunks.get(state.chunk_index).copied().unwrap_or_default();
            let v = u32::from_be_bytes(chunk);
            state.chunk_index += 1;
            state.value <<= 32;
            state.value |= u64::from(v);
            state.bit_count += 32;
        }
        debug_assert!(state.bit_count >= 0);

        debug_assert!((128..=255).contains(&state.range));
        let half_range = state.range / 2;
        let split = state.range - half_range;
        let bigsplit = u64::from(split) << state.bit_count;

        let retval = if let Some(new_value) = state.value.checked_sub(bigsplit) {
            state.range = half_range;
            state.value = new_value;
            true
        } else {
            state.range = split;
            false
        };

        debug_assert!((64..=128).contains(&state.range));
        let shift = if state.range == 0x80 { 0 } else { 1 };
        state.range <<= shift;
        state.bit_count -= shift;

        debug_assert!((128..=254).contains(&state.range));
        retval
    }

''')
replace_fn('fast_read_sign','fast_read_literal',r'''    fn fast_read_sign(&mut self) -> bool {
        let chunks = self.chunks;
        let state = &mut self.uncommitted_state;

        if state.bit_count < 0 {
            let chunk = chunks.get(state.chunk_index).copied().unwrap_or_default();
            let v = u32::from_be_bytes(chunk);
            state.chunk_index += 1;
            state.value <<= 32;
            state.value |= u64::from(v);
            state.bit_count += 32;
        }

        debug_assert!((128..=254).contains(&state.range));
        let half_range = state.range / 2;
        let split = state.range - half_range;
        let bigsplit = u64::from(split) << state.bit_count;

        let retval = if let Some(new_value) = state.value.checked_sub(bigsplit) {
            state.range = half_range;
            state.value = new_value;
            true
        } else {
            state.range = split;
            false
        };

        debug_assert!((64..=127).contains(&state.range));
        state.range <<= 1;
        state.bit_count -= 1;

        debug_assert!((128..=254).contains(&state.range));
        retval
    }

''')
p.write_text(s)
