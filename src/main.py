import re
import logging
import time
import os
import sys

from src import config
from src.recorder import Recorder
from src.stt import Transcriber
from src.brain import classify
from src.tts import speak

log_level = config.LOG_LEVEL.upper()
log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
log_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
log_path = os.path.join(log_dir, "jarvis.log")
if log_level == "OFF":
    logging.basicConfig(level=logging.CRITICAL + 1, format=log_format)
else:
    logging.basicConfig(
        level=getattr(logging, log_level, logging.WARNING),
        format=log_format,
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger(__name__)


def _vad_loop(recorder, transcriber):
    while True:
        logger.info("Escuchando...")
        audio = recorder.record_until_silence()
        text = transcriber.transcribe(audio, recorder.sample_rate)
        if not text:
            continue
        logger.info("Texto: %s", text)
        if "jarvis" not in text.lower():
            continue
        command = re.sub(r"(?i)^.*?jarvis\s*", "", text).strip()
        if not command:
            continue
        response = classify(command)
        logger.info("Respuesta: %s", response)
        speak(response)
        time.sleep(1.5)


def _ptt_loop(recorder, transcriber):
    import keyboard
    hotkey = config.PTT_HOTKEY
    logger.info("Push-to-talk activo. Presioná %s para hablar.", hotkey)
    while True:
        keyboard.wait(hotkey)
        logger.info("Grabando...")
        audio = recorder.record_until_silence()
        text = transcriber.transcribe(audio, recorder.sample_rate)
        if not text:
            continue
        logger.info("Texto: %s", text)
        response = classify(text)
        logger.info("Respuesta: %s", response)
        speak(response)
        time.sleep(0.5)


def main():
    try:
        recorder = Recorder()
        transcriber = Transcriber()
        if config.WAKE_MODE == "ptt":
            _ptt_loop(recorder, transcriber)
        else:
            _vad_loop(recorder, transcriber)
    except Exception as e:
        logger.exception("Error fatal: %s", e)


if __name__ == "__main__":
    main()
