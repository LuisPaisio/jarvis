import logging
import time
import os
import sys
import winsound

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


def _ptt_loop(recorder, transcriber):
    import keyboard
    hotkey = config.PTT_HOTKEY
    logger.info("Push-to-talk activo. Presioná %s para hablar.", hotkey)
    while True:
        keyboard.wait(hotkey)
        winsound.Beep(800, 150)
        logger.info("Grabando...")
        audio = recorder.record_until_silence()
        if audio is None:
            continue
        text = transcriber.transcribe(audio, recorder.sample_rate)
        if not text:
            continue
        logger.info("Texto: %s", text)
        response = classify(text)
        logger.info("Respuesta: %s", response)
        try:
            speak(response)
        except Exception as e:
            logger.exception("Error al hablar: %s", e)
        time.sleep(0.5)


def main():
    try:
        recorder = Recorder()
        transcriber = Transcriber()
        _ptt_loop(recorder, transcriber)
    except Exception as e:
        logger.exception("Error fatal: %s", e)


if __name__ == "__main__":
    main()
