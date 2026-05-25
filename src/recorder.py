import logging
import webrtcvad
import sounddevice as sd
import numpy as np

from src import config

logger = logging.getLogger(__name__)


class Recorder:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.vad = webrtcvad.Vad(2)
        self.silence_seconds = config.VAD_SILENCE_SECONDS
        self.device_id = None
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            if "HyperX" in dev["name"] and dev["max_input_channels"] > 0:
                self.device_id = i
                logger.info("Micrófono encontrado: %s (device %d)", dev["name"], i)
                break

    def record_until_silence(self) -> np.ndarray:
        frame_duration_ms = 30
        frame_size = int(self.sample_rate * frame_duration_ms / 1000)
        silence_frames_needed = int(self.silence_seconds * 1000 / frame_duration_ms)
        silence_count = 0
        frames = []

        audio_stream = sd.InputStream(
            samplerate=self.sample_rate,
            device=self.device_id,
            channels=1,
            dtype="int16",
            blocksize=frame_size,
        )
        audio_stream.start()

        try:
            while True:
                frame, _ = audio_stream.read(frame_size)
                pcm = frame[:, 0].tobytes()
                is_speech = self.vad.is_speech(pcm, self.sample_rate)
                if is_speech:
                    silence_count = 0
                else:
                    silence_count += 1
                frames.append(frame[:, 0])
                if silence_count >= silence_frames_needed and len(frames) > silence_frames_needed:
                    break
        finally:
            audio_stream.stop()
            audio_stream.close()

        return np.concatenate(frames)
