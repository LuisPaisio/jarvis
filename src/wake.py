import logging
import os
import sys
import openwakeword
from openwakeword.model import Model
import sounddevice as sd
import numpy as np

SAMPLE_RATE = 16000

logger = logging.getLogger(__name__)


def _find_model() -> str:
    rutas = []
    if getattr(sys, 'frozen', False):
        rutas.append(os.path.join(sys._MEIPASS, "models", "hey_jarvis_v0.1.onnx"))
    rutas.append(os.path.join(os.path.dirname(__file__), "..", "models", "hey_jarvis_v0.1.onnx"))
    rutas.append(os.path.join(
        os.path.dirname(openwakeword.__file__),
        "resources", "models", "hey_jarvis_v0.1.onnx",
    ))
    for r in rutas:
        if os.path.exists(r):
            return r
    raise FileNotFoundError(f"No se encontró el modelo en ninguna ruta")


class WakeWordDetector:
    def __init__(self):
        model_path = _find_model()
        self.model = Model(wakeword_model_paths=[model_path])
        self.umbral = 0.3
        self.device_id = None
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            if "HyperX" in dev["name"] and dev["max_input_channels"] > 0:
                self.device_id = i
                logger.info("Wake word mic: %s (device %d)", dev["name"], i)
                break
        if self.device_id is None:
            logger.info("HyperX no encontrado, usando dispositivo por defecto")

    def escuchar(self, duracion_bloques=3):
        audio = sd.rec(int(duracion_bloques * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32", device=self.device_id)
        sd.wait()
        return audio.flatten()

    def detectar(self, audio):
        scores = self.model.predict(audio)
        logger.debug("Scores wake word: %s", scores)
        for _, score in scores.items():
            if score > self.umbral:
                return True
        return False

    def listen(self) -> bool:
        while True:
            audio = self.escuchar()
            if self.detectar(audio):
                return True

    def close(self):
        pass
