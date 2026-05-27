import asyncio
import edge_tts
import subprocess
import tempfile
import os
import ctypes
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
            _play_windows(tmp_path)
        else:
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", tmp_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def _play_windows(path: str):
    try:
        winmm = ctypes.windll.winmm
        result = winmm.mciSendStringW(
            f'open "{path}" type mpegvideo alias jarvis_tts', None, 0, 0
        )
        if result != 0:
            raise RuntimeError(f"MCI open falló con código {result}")
        result = winmm.mciSendStringW('play jarvis_tts wait', None, 0, 0)
        if result != 0:
            raise RuntimeError(f"MCI play falló con código {result}")
        winmm.mciSendStringW('close jarvis_tts', None, 0, 0)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.exception("Error reproduciendo audio: %s", e)
