import re
import logging
import time
import os
import sys
import threading

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

_stop_event = threading.Event()
_mode_switch_event = threading.Event()
_current_mode = [config.WAKE_MODE]


def get_current_mode() -> str:
    return _current_mode[0]


def set_mode(mode: str):
    if mode == _current_mode[0]:
        return
    _current_mode[0] = mode
    _stop_event.set()
    _mode_switch_event.set()
    logger.info("Modo cambiado a %s", mode)


def _vad_loop(recorder, transcriber):
    while not _stop_event.is_set():
        logger.info("Escuchando...")
        audio = recorder.record_until_silence(stop_event=_stop_event)
        if audio is None or _stop_event.is_set():
            break
        text = transcriber.transcribe(audio, recorder.sample_rate)
        if not text:
            continue
        logger.info("Texto: %s", text)
        if not re.search(r"(?i)\bjarvi[sz']*", text):
            continue
        command = re.sub(r"(?i)^.*?\bjarvi[sz']*\b\s*", "", text).strip()
        if not command:
            continue
        response = classify(command)
        logger.info("Respuesta: %s", response)
        speak(response)
        time.sleep(1.5)
    logger.info("VAD loop finalizado")


def _ptt_loop(recorder, transcriber):
    import keyboard
    hotkey = config.PTT_HOTKEY
    logger.info("Push-to-talk activo. Presioná %s para hablar.", hotkey)
    while not _stop_event.is_set():
        result = keyboard.wait(hotkey, timeout=0.5)
        if _stop_event.is_set():
            break
        if result is None:
            continue
        logger.info("Grabando...")
        audio = recorder.record_until_silence(
            stop_event=_stop_event,
            silence_seconds=config.PTT_SILENCE_SECONDS
        )
        if audio is None or _stop_event.is_set():
            break
        text = transcriber.transcribe(audio, recorder.sample_rate)
        if not text:
            continue
        logger.info("Texto: %s", text)
        response = classify(text)
        logger.info("Respuesta: %s", response)
        speak(response)
        time.sleep(0.5)
    logger.info("PTT loop finalizado")


def main():
    try:
        recorder = Recorder()
        vad_transcriber = Transcriber(config.WHISPER_VAD_MODEL)
        ptt_transcriber = Transcriber()

        while True:
            _stop_event.clear()
            _mode_switch_event.clear()

            if _current_mode[0] == "ptt":
                _ptt_loop(recorder, ptt_transcriber)
            else:
                _vad_loop(recorder, vad_transcriber)

            if _mode_switch_event.is_set():
                logger.info("Reiniciando loop en modo %s", _current_mode[0])
                continue
            break
    except Exception as e:
        logger.exception("Error fatal: %s", e)


if __name__ == "__main__":
    main()
