"""
SpeakType Windows prototype

Workable MVP behavior:
- Hold F8 to record audio from default microphone
- Release F8 to stop and transcribe locally with faster-whisper
- Copy transcript to clipboard and attempt Ctrl+V paste into active app
"""

from __future__ import annotations

import ctypes
import queue
import tempfile
import threading
import time
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import keyboard
import numpy as np
import pyperclip
import sounddevice as sd
from faster_whisper import WhisperModel
from scipy.signal import resample_poly


SAMPLE_RATE = 44_100
TARGET_SAMPLE_RATE = 16_000
CHANNELS = 1
HOTKEY = "f8"
MODEL_SIZE = "base"
MODEL_COMPUTE_TYPE = "int8"


@dataclass
class RecordingBuffer:
    chunks: List[np.ndarray]

    def __init__(self) -> None:
        self.chunks = []

    def append(self, data: np.ndarray) -> None:
        # Data arrives as float32 in shape (frames, channels). Convert to mono.
        if data.ndim > 1:
            mono = np.mean(data, axis=1)
        else:
            mono = data
        self.chunks.append(np.copy(mono.astype(np.float32)))

    def merged(self) -> np.ndarray:
        if not self.chunks:
            return np.array([], dtype=np.float32)
        return np.concatenate(self.chunks, axis=0)


class SpeakTypeWindowsPrototype:
    def __init__(self) -> None:
        self._recording = False
        self._recording_lock = threading.Lock()
        self._stream: Optional[sd.InputStream] = None
        self._buffer = RecordingBuffer()
        self._events: "queue.Queue[str]" = queue.Queue()
        self._model = WhisperModel(MODEL_SIZE, compute_type=MODEL_COMPUTE_TYPE)
        self._last_press_time = 0.0

    def run(self) -> None:
        print("SpeakType Windows prototype is running.")
        print(f"Hold {HOTKEY.upper()} to record. Release to transcribe and paste.")
        print("Press CTRL+C to exit.")

        keyboard.on_press_key(HOTKEY, lambda _: self._events.put("press"))
        keyboard.on_release_key(HOTKEY, lambda _: self._events.put("release"))

        try:
            while True:
                event = self._events.get()
                if event == "press":
                    self._start_recording()
                elif event == "release":
                    self._stop_recording_and_transcribe()
        except KeyboardInterrupt:
            print("\nStopping prototype...")
        finally:
            with self._recording_lock:
                if self._stream is not None:
                    self._stream.stop()
                    self._stream.close()
                    self._stream = None
            keyboard.unhook_all()

    def _audio_callback(self, indata, _frames, _timestamp, status) -> None:
        if status:
            print(f"Audio status: {status}")
        with self._recording_lock:
            if self._recording:
                self._buffer.append(indata)

    def _start_recording(self) -> None:
        with self._recording_lock:
            if self._recording:
                return

            now = time.time()
            # Debounce repeat key press events.
            if now - self._last_press_time < 0.05:
                return
            self._last_press_time = now

            self._buffer = RecordingBuffer()
            self._stream = sd.InputStream(
                channels=CHANNELS,
                samplerate=SAMPLE_RATE,
                dtype="float32",
                callback=self._audio_callback,
            )
            self._stream.start()
            self._recording = True
            print("● Recording...")

    def _stop_recording_and_transcribe(self) -> None:
        with self._recording_lock:
            if not self._recording:
                return
            self._recording = False
            if self._stream is not None:
                self._stream.stop()
                self._stream.close()
                self._stream = None

        print("■ Recording stopped. Transcribing...")
        audio = self._buffer.merged()
        if audio.size == 0:
            print("No audio captured.")
            return

        # Ignore accidental micro-taps.
        duration_s = audio.shape[0] / SAMPLE_RATE
        if duration_s < 0.2:
            print("Recording too short, skipping.")
            return

        transcript = self._transcribe(audio)
        if not transcript:
            print("No speech detected.")
            return

        print(f"Transcript: {transcript}")
        self._copy_and_paste(transcript)

    def _transcribe(self, audio: np.ndarray) -> str:
        # Resample from 44.1kHz to 16kHz mono PCM float32.
        audio_16k = resample_poly(audio, TARGET_SAMPLE_RATE, SAMPLE_RATE).astype(np.float32)

        # Write a temporary WAV for clearer interoperability.
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            wav_path = Path(tmp.name)
        try:
            self._write_wav(wav_path, audio_16k, TARGET_SAMPLE_RATE)

            segments, _ = self._model.transcribe(
                str(wav_path),
                beam_size=1,
                vad_filter=True,
                language="en",
                task="transcribe",
            )
            text = " ".join(segment.text.strip() for segment in segments).strip()
            return " ".join(text.split())
        finally:
            try:
                wav_path.unlink(missing_ok=True)
            except OSError:
                pass

    @staticmethod
    def _write_wav(path: Path, audio: np.ndarray, samplerate: int) -> None:
        clipped = np.clip(audio, -1.0, 1.0)
        pcm16 = (clipped * 32767.0).astype(np.int16)
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(pcm16.tobytes())

    @staticmethod
    def _copy_and_paste(text: str) -> None:
        pyperclip.copy(text)
        # Simulate Ctrl+V in foreground application.
        keyboard.send("ctrl+v")
        # Optional confirmation tone/beep.
        try:
            ctypes.windll.user32.MessageBeep(0xFFFFFFFF)
        except Exception:
            pass


def main() -> None:
    app = SpeakTypeWindowsPrototype()
    app.run()


if __name__ == "__main__":
    main()
