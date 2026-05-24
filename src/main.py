import logging

from src import config
from src.wake import WakeWordDetector
from src.recorder import Recorder
from src.stt import Transcriber
from src.brain import classify
from src.tts import speak

log_level = config.LOG_LEVEL.upper()
log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
if log_level == "OFF":
    logging.basicConfig(level=logging.CRITICAL + 1, format=log_format)
else:
    logging.basicConfig(
        level=getattr(logging, log_level, logging.WARNING),
        format=log_format,
        handlers=[
            logging.FileHandler("jarvis.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger(__name__)


def main():
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


if __name__ == "__main__":
    main()
