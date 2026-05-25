import logging
import os
import sys

from src import config
from src.wake import WakeWordDetector
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


def main():
    try:
        logger.info("Iniciando Jarvis...")
        wake = WakeWordDetector()
        recorder = Recorder()
        transcriber = Transcriber()

        try:
            while True:
                logger.info("Esperando wake word...")
                if wake.listen():
                    audio = recorder.record_until_silence()
                    text = transcriber.transcribe(audio, recorder.sample_rate)
                    logger.info("Texto: %s", text)

                    if not text:
                        continue

                    response = classify(text)
                    logger.info("Respuesta: %s", response)
                    speak(response)
        except KeyboardInterrupt:
            logger.info("Jarvis detenido por el usuario")
        finally:
            wake.close()
    except Exception as e:
        logger.exception("Error fatal: %s", e)


if __name__ == "__main__":
    main()
