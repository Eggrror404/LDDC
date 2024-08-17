# SPDX-FileCopyrightText: Copyright (c) 2024 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only

from backend.lyrics import Lyrics, LyricsLine, MultiLyricsData, get_full_timestamps_lyrics_data
from utils.utils import get_divmod_time
from utils.version import __version__

from .share import get_lyrics_lines

ASS_HEADER1 = f"""[Script Info]
; Script generated by LDDC {__version__ if __version__ is not None else ""}
; https://github.com/chenmozhijin/LDDC
"""

ASS_HEADER2 = ("""ScriptType: v4.00+
Timer: 100.0000

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, """
               "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")

DIALOGUE = "Dialogue: 0,{start},{end},{lang},,0,0,0,,{text}\n"


def ms2ass_timestamp(ms: int) -> str:
    h, m, s, ms = get_divmod_time(ms)

    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}.{int(ms):03d}"


def lyrics_line2asstext(lyrics_line: LyricsLine) -> str:
    ass_text = ""
    if len(lyrics_line[2]) == 1:
        return "".join([word[2]for word in lyrics_line[2] if word[2] != ""])
    for word in lyrics_line[2]:
        word_start, word_end = word[0], word[1]
        if word_start is not None and word_end is not None:
            k = abs(word_end - word_start) // 10
        else:
            return "".join([word[2]for word in lyrics_line[2] if word[2] != ""])
        ass_text += r"{\kf" + str(k) + "}" + word[2]
    return ass_text


def ass_converter(lyrics: Lyrics,
                  lyrics_dict: MultiLyricsData,
                  langs_mapping: dict[str, dict[int, int]],
                  langs_order: list[str]) -> str:

    ass_text = ASS_HEADER1
    if lyrics.title is not None:
        ass_text += f"Title: {lyrics.title}\n"
    ass_text += ASS_HEADER2 + "\n"
    ass_text += "\n".join([
        f"Style: {lrc_type},Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1" for lrc_type in lyrics],
    ) + "\n\n"
    ass_text += "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    lyrics_orig = get_full_timestamps_lyrics_data(lyrics_dict["orig"],
                                                  duration=lyrics.duration * 1000 if lyrics.duration is not None else None,
                                                  only_line=True)

    lyrics_texts = {lang: "" for lang in langs_order[::-1]}
    for orig_i, orig_line in enumerate(lyrics_orig):
        orig_start, orig_end = orig_line[0], orig_line[1]
        if orig_start is None or orig_end is None:
            continue

        for (lyrics_line, _), lang in zip(get_lyrics_lines(lyrics_dict, langs_order, orig_i, orig_line, langs_mapping), langs_order, strict=False):
            lyrics_texts[lang] += DIALOGUE.format(start=ms2ass_timestamp(orig_start),
                                                  end=ms2ass_timestamp(orig_end),
                                                  lang=lang,
                                                  text=lyrics_line2asstext(lyrics_line))

    return ass_text + "".join(lyrics_texts.values())
