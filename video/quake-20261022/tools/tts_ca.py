# Run core/tts/tts_zh.py with certifi pointed at the session's proxy CA bundle (edge-tts pins certifi).
import sys, runpy, certifi
certifi.where = lambda: "/root/.ccr/ca-bundle.crt"
script = sys.argv[1]; sys.argv = sys.argv[1:]
runpy.run_path(script, run_name="__main__")
