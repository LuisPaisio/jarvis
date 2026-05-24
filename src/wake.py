import logging
import os
import openwakeword
from openwakeword.model import Model
import sounddevice as sd
import numpy as np

SAMPLE_RATE = 16000

logger = logging.getLogger(__name__)


class WakeWordDetector:
    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(openwakeword.__file__),
            "resources", "models", "hey_jarvis_v0.1.onnx",
        )
        self.model = Model(wakeword_models=[model_path])
        self.umbral = 0.5

    def escuchar(self, duracion_bloques=3):
        audio = sd.rec(int(duracion_bloques * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32")
        sd.wait()
        return audio.flatten()

    def detectar(self, audio):
        self.model.predict(audio)
        scores = self.model.prediction_data
        for mdl in scores:
            for word in scores[mdl]:
                if scores[mdl][word] > self.umbral:
                    return True
        return False

    def listen(self) -> bool:
        while True:
            audio = self.escuchar()
            if self.detectar(audio):
                return True

    def close(self):
        pass
