"""Convert a line of text to furigana in the format of maru.re custom lrc.

This is a quick way to generate them, however note that using the
roman lyrics fetched in LDDC could be better and more accurate.

Requirements:
- pykakasi

Usage:
Run `python maru_furigana.py` and enter the text in stdin.
Converted text will be printed to stdout.

If using Vim/NeoVim, you can select a line in visual mode
and convert the line with command `:'<,'>!python maru_furigana.py`,
then the line will be replaced with the converted text.
"""

import pykakasi

kks = pykakasi.kakasi()
result = kks.convert(input())

for item in result:
    not_hira = item["orig"] != item["hira"]
    print(f"{{{item['orig']}}}({item['hira']})" if not_hira else item["orig"], end="")

print()
