import logging
import pvporcupine
import sounddevice as sd
import numpy as np

SAMPLE_RATE = 16000
FRAME_LENGTH = 512

logger = logging.getLogger(__name__)


class WakeWordDetector:
    def __init__(self):
        self.porcupine = pvporcupine.create(keywords=["jarvis"])
        self.device_id = None
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            if "HyperX" in dev["name"] and dev["max_input_channels"] > 0:
                self.device_id = i
                logger.info("Wake word mic: %s (device %d)", dev["name"], i)
                break
        if self.device_id is None:
            logger.info("HyperX no encontrado, usando dispositivo por defecto")

    def listen(self) -> bool:
        with sd.InputStream(
            samplerate=SAMPLE_RATE, device=self.device_id,
            channels=1, dtype="int16", blocksize=FRAME_LENGTH,
        ) as stream:
            while True:
                audio, _ = stream.read(FRAME_LENGTH)
                pcm = audio[:, 0].flatten()
                result = self.porcupine.process(pcm)
                if result >= 0:
                    return True

    def close(self):
        self.porcupine.delete()
