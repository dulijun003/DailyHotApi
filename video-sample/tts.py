import asyncio, certifi, sys
certifi.where = lambda: "/root/.ccr/ca-bundle.crt"
import edge_tts
async def main(text, out):
    c = edge_tts.Communicate(text, "zh-CN-YunxiNeural", rate="+22%")
    await c.save(out)
asyncio.run(main(sys.argv[1], sys.argv[2]))
