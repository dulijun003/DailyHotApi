"""Text-to-speech narration via edge-tts (Microsoft neural voices).

A whole narration block (one or more sentences) is synthesised in ONE call so
the intonation flows naturally, and edge-tts's word boundaries give the time
at which every character is spoken. That lets the scene:
  - land animations on specific words   (Narration.until("山羊"))
  - time subtitles per clause exactly    (Narration.clauses())

Results are cached by content hash under reelkit/assets/tts/.

Network: honours HTTPS_PROXY and the system CA store / SSL_CERT_FILE.

Good Chinese voices:  zh-CN-YunxiNeural (male, lively; default)
                      zh-CN-XiaoxiaoNeural (female, warm)
                      zh-CN-YunyangNeural (male, news anchor)
"""

import asyncio
import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "assets" / "tts"
PUNCT = "，。、；：！？,.;:!?“”‘’《》（）()… "
CLAUSE_END = "，。、；：！？,;:!?"
LEAD, TAIL = 0.04, 0.12        # seconds of air kept before / after the speech


@dataclass
class Narration:
    text: str
    path: str
    duration: float
    char_times: list           # (start, end) per character of `text`

    def time_of(self, phrase, after=0):
        """Seconds (from clip start) at which `phrase` starts being spoken."""
        i = self.text.find(phrase, after)
        if i < 0:
            raise ValueError(f"cue {phrase!r} not in narration {self.text!r}")
        return self.char_times[i][0], i + len(phrase)

    def clauses(self):
        """[(start, end, text)] split at punctuation, punctuation stripped (？！ kept)."""
        out, buf, idx = [], "", []
        for i, ch in enumerate(self.text):
            if ch in CLAUSE_END:
                if buf.strip():
                    keep = ch if ch in "？！?!" else ""
                    out.append((self.char_times[idx[0]][0], self.char_times[idx[-1]][1],
                                buf.strip() + keep))
                buf, idx = "", []
            else:
                buf += ch
                if ch not in PUNCT:
                    idx.append(i)
        if buf.strip() and idx:
            out.append((self.char_times[idx[0]][0], self.char_times[idx[-1]][1], buf.strip()))
        return out


async def _synth(text, voice, rate, pitch, out_mp3):
    import edge_tts
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    com = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, proxy=proxy,
                               boundary="WordBoundary")
    words = []
    with open(out_mp3, "wb") as f:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append((chunk["offset"] / 1e7, (chunk["offset"] + chunk["duration"]) / 1e7,
                              chunk["text"]))
    return words


def _char_times(text, words):
    """Assign every character a (start, end) from the word boundaries."""
    times = [None] * len(text)
    pos = 0
    for a, b, w in words:
        j = text.find(w, pos)
        if j < 0:
            continue
        n = len(w)
        for k in range(n):                      # spread the word over its characters
            times[j + k] = (a + (b - a) * k / n, a + (b - a) * (k + 1) / n)
        pos = j + n
    # Punctuation / unmatched chars inherit the previous char's end.
    last = (0.0, 0.0)
    for i, t in enumerate(times):
        if t is None:
            times[i] = (last[1], last[1])
        else:
            last = t
    return times


def tts(text, voice="zh-CN-YunxiNeural", rate="+20%", pitch="+0Hz"):
    """Synthesise (or load from cache) one narration block."""
    key = hashlib.sha1(f"v2|{voice}|{rate}|{pitch}|{text}".encode()).hexdigest()[:16]
    wav, meta = CACHE / f"{key}.wav", CACHE / f"{key}.json"
    if not (wav.exists() and meta.exists()):
        CACHE.mkdir(parents=True, exist_ok=True)
        raw = CACHE / f"{key}.raw.mp3"
        for attempt in range(4):
            try:
                words = asyncio.run(_synth(text, voice, rate, pitch, raw))
                break
            except Exception:
                if attempt == 3:
                    raise
        # Cut the voice's built-in leading/trailing silence using the real
        # speech boundaries (more precise than a level detector).
        start = max(0.0, words[0][0] - LEAD)
        end = words[-1][1] + TAIL
        tmp = CACHE / f"{key}.part.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw),
                        "-af", f"atrim=start={start}:end={end},asetpts=PTS-STARTPTS,"
                               "afade=t=in:d=0.02",
                        "-ar", "44100", "-ac", "2", str(tmp)], check=True)
        raw.unlink()
        tmp.rename(wav)
        words = [(a - start, b - start, w) for a, b, w in words]
        meta.write_text(json.dumps({"words": words, "duration": end - start},
                                   ensure_ascii=False))
    data = json.loads(meta.read_text())
    return Narration(text, str(wav), data["duration"], _char_times(text, data["words"]))


def split_sentences(text):
    return [s for s in re.split(r"(?<=[。！？!?])", text) if s.strip()]
