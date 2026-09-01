#!/usr/bin/env python3
from pathlib import Path
p=Path('src/lossless/decoder/mod.rs')
s=p.read_text()
hstart=s.index('impl HuffmanInfo {\n')
hend=s.index('\n}\n\n#[derive(Debug, Clone)]\nstruct ColorCache',hstart)+3
s=s[:hstart]+s[hend:]
start=s.index('    /// Decodes the image data using the huffman trees and either of the 3 methods of decoding\n    fn decode_image_data')
end=s.index('    /// Reads color cache data from the bitstream',start)
replacement=Path('tools/group_decode_body.txt').read_text()
s=s[:start]+replacement+s[end:]
p.write_text(s)
