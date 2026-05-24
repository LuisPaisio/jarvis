import logging
import numpy as np
from faster_whisper import WhisperModel

from src import config

logger = logging.getLogger(__name__)


class Transcriber:
    def __init__(self):
        model_name = config.WHISPER_MODEL
        self.model = None
        try:
            self.model = WhisperModel(
                model_name,
                device="cuda",
                compute_type="float16",
            )
            logger.info("Whisper cargado en CUDA")
        except Exception as e:
            logger.warning("CUDA no disponible, fallback a CPU: %s", e)
            self.model = WhisperModel(
                model_name,
                device="cpu",
                compute_type="int8",
            )
            logger.info("Whisper cargado en CPU")

    def transcribe(self, audio: np.ndarray, sample_rate: int) -> str:
        segments, _ = self.model.transcribe(audio, language="es", beam_size=5)
        return " ".join(seg.text for seg in segments).strip()
