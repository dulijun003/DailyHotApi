"""Text-to-speech narration via edge-tts (Microsoft neural voices).

Each sentence is synthesised separately and cached by content hash, so
re-rendering only calls the service for lines that changed.

Network notes: edge-tts honours HTTPS_PROXY (passed explicitly below) and the
system CA store / SSL_CERT_FILE.

Good Chinese voices:  zh-CN-YunxiNeural (male, lively; default)
                      zh-CN-XiaoxiaoNeural (female, warm)
                      zh-CN-YunyangNeural (male, news anchor)
"""

import asyncio
import hashlib
import os
import re
import subprocess
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "assets" / "tts"

SENTENCE_END = re.compile(r"(?<=[。！？!?])")
CLAUSE_SPLIT = re.compile(r"(?<=[，、；：,;:])")
TRAILING_PUNCT = "，。、；：！？,.;:!?"


def split_sentences(text):
    return [s.strip() for s in SENTENCE_END.split(text) if s.strip()]


def split_clauses(sentence):
    """Subtitle chunks: clauses, with trailing punctuation dropped (except ？！)."""
    out = []
    for c in CLAUSE_SPLIT.split(sentence):
        c = c.strip()
        if not c:
            continue
        keep = c[-1] if c[-1] in "？！?!" else ""
        out.append(c.rstrip(TRAILING_PUNCT) + keep)
    return out


def _duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


async def _synth(text, voice, rate, pitch, out):
    import edge_tts
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    com = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, proxy=proxy)
    await com.save(str(out))


# Edge voices pad each clip with ~0.2 s of leading and ~0.8 s of trailing
# silence; trim both so sentence timing (and subtitle sync) is tight.
TRIM = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,"
        "areverse,"
        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,"
        "areverse")


def tts(text, voice="zh-CN-YunxiNeural", rate="+15%", pitch="+0Hz"):
    """Return (path, duration_seconds) for `text`, synthesising if not cached."""
    key = hashlib.sha1(f"{voice}|{rate}|{pitch}|{text}|trim1".encode()).hexdigest()[:16]
    out = CACHE / f"{key}.wav"
    if not out.exists() or out.stat().st_size == 0:
        CACHE.mkdir(parents=True, exist_ok=True)
        raw = out.with_suffix(".raw.mp3")
        for attempt in range(4):
            try:
                asyncio.run(_synth(text, voice, rate, pitch, raw))
                break
            except Exception:
                if attempt == 3:
                    raise
        tmp = out.with_suffix(".part.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", TRIM,
                        "-ar", "44100", "-ac", "2", str(tmp)], check=True)
        raw.unlink()
        tmp.rename(out)
    return str(out), _duration(out)
