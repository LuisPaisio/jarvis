import asyncio
import edge_tts
import tempfile
import subprocess
import os

from src import config

VOICE = config.TTS_VOICE


def speak(text: str):
    asyncio.run(_speak_async(text))


async def _speak_async(text: str):
    communicate = edge_tts.Communicate(text, VOICE)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name
    await communicate.save(tmp_path)

    if os.name == "nt":
        subprocess.Popen(
            ["powershell", "-Command",
             f"(New-Object Media.SoundPlayer '{tmp_path}').PlaySync(); Remove-Item '{tmp_path}'"],
            shell=True,
        ).wait()
    else:
        subprocess.Popen(["ffplay", "-nodisp", "-autoexit", tmp_path],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
        os.unlink(tmp_path)
