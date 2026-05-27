import os
from dotenv import load_dotenv

load_dotenv()


def get(key: str, default: str = "") -> str:
    return os.getenv(key, default)


OPENCODE_PATH = get("OPENCODE_PATH")
DEFAULT_MICROPHONE = get("DEFAULT_MICROPHONE", "default")
WHISPER_MODEL = get("WHISPER_MODEL", "small")
TTS_VOICE = get("TTS_VOICE", "es-MX-DaliaNeural")
VAD_SILENCE_SECONDS = float(get("VAD_SILENCE_SECONDS", "1.5"))
DEFAULT_BROWSER = get("DEFAULT_BROWSER", "edge")
OPENCODE_MODEL = get("OPENCODE_MODEL", "DeepSeek V4 Flash Free")
LOG_FILE = get("LOG_FILE", "jarvis.log")
LOG_LEVEL = get("LOG_LEVEL", "WARNING")
WAKE_MODE = get("WAKE_MODE", "vad")
PTT_HOTKEY = get("PTT_HOTKEY", "ctrl+alt+z")
PTT_SILENCE_SECONDS = float(get("PTT_SILENCE_SECONDS", "0.8"))
WHISPER_VAD_MODEL = get("WHISPER_VAD_MODEL", "tiny")
