import logging
import os
import sys
import numpy as np
from faster_whisper import WhisperModel

from src import config

logger = logging.getLogger(__name__)


class Transcriber:
    def __init__(self, model_name=None):
        if model_name is None:
            model_name = config.WHISPER_MODEL
        if hasattr(sys, '_MEIPASS'):
            for lib_dir in [
                os.path.join(sys._MEIPASS, 'nvidia', 'cublas', 'lib'),
                os.path.join(sys._MEIPASS, 'nvidia', 'cudnn', 'lib'),
            ]:
                if os.path.isdir(lib_dir):
                    os.add_dll_directory(lib_dir)
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
        segments, _ = self.model.transcribe(audio, language="es", beam_size=5)
        return " ".join(seg.text for seg in segments).strip()
