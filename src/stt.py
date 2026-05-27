import logging
import os
import sys
import numpy as np
from faster_whisper import WhisperModel

from src import config

logger = logging.getLogger(__name__)


class Transcriber:
    def __init__(self):
        model_name = config.WHISPER_MODEL
        if hasattr(sys, '_MEIPASS'):
            import ctypes
            for root, dirs, files in os.walk(sys._MEIPASS):
                if 'cublas64_12.dll' in files:
                    full_path = os.path.join(root, 'cublas64_12.dll')
                    ctypes.CDLL(full_path)
                    os.environ['PATH'] = root + os.pathsep + os.environ.get('PATH', '')
                    logger.info("cuBLAS precargado desde %s", full_path)
                    break
        self.model = None
        try:
            self.model = WhisperModel(
                model_name,
                device="cuda",
                compute_type="float16",
            )
            logger.info("Whisper %s cargado en CUDA", model_name)
        except Exception as e:
            logger.warning("CUDA no disponible, fallback a CPU: %s", e)
            self.model = WhisperModel(
                model_name,
                device="cpu",
                compute_type="int8",
            )
            logger.info("Whisper %s cargado en CPU", model_name)

    def transcribe(self, audio: np.ndarray, sample_rate: int) -> str:
        segments, _ = self.model.transcribe(audio, language="es", beam_size=10)
        return " ".join(seg.text for seg in segments).strip()
