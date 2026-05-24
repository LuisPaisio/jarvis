import asyncio
import edge_tts
import subprocess
import tempfile
import os
from src import config

VOICE = config.TTS_VOICE


def speak(text: str):
    asyncio.run(_speak_async(text))


async def _speak_async(text: str):
    communicate = edge_tts.Communicate(text, VOICE)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        await communicate.save(tmp_path)
        if os.name == "nt":
            subprocess.run([
                "powershell", "-NoProfile", "-Command",
                "$wmp = New-Object -ComObject WMPlayer.OCX; "
                f"$wmp.URL = '{tmp_path}'; "
                "while ($wmp.playState -ne 1) { Start-Sleep -Milliseconds 100 }; "
                "$wmp.close(); "
                f"Remove-Item '{tmp_path}'"
            ], check=True)
        else:
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", tmp_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
