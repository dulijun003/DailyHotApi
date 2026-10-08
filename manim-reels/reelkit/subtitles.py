"""Subtitle files from narration timings: .srt (for upload) and .ass (burned in).

The .ass style matches the reel: bold CJK font, ink text on a translucent
paper-coloured box, near the bottom of the 1080x1350 frame.
"""

from . import style as S


def _clean(subs, min_gap=0.35):
    """Sort, drop overlaps, and bridge short gaps so captions don't flicker."""
    subs = sorted(subs)
    out = []
    for i, (a, b, t) in enumerate(subs):
        if i + 1 < len(subs):
            nxt = subs[i + 1][0]
            b = nxt if nxt - b < min_gap else b
            b = min(b, nxt)
        out.append((a, b, t))
    return out


def _ts_srt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _ts_ass(t):
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360_000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _ass_colour(hex_rgb, alpha=0):
    r, g, b = hex_rgb[1:3], hex_rgb[3:5], hex_rgb[5:7]
    return f"&H{alpha:02X}{b}{g}{r}".upper()


def write_srt(subs, path):
    lines = []
    for i, (a, b, t) in enumerate(_clean(subs), 1):
        lines += [str(i), f"{_ts_srt(a)} --> {_ts_srt(b)}", t, ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_ass(subs, path, font_size=64, margin_v=56):
    ink = _ass_colour(S.INK)
    box = _ass_colour(S.BG, alpha=0x28)
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {S.PIXEL_WIDTH}
PlayResY: {S.PIXEL_HEIGHT}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{S.FONT},{font_size},{ink},{ink},{box},{box},-1,0,0,0,100,100,1,0,3,14,0,2,60,60,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = [f"Dialogue: 0,{_ts_ass(a)},{_ts_ass(b)},Sub,,0,0,0,,{t}"
              for a, b, t in _clean(subs)]
    path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")
