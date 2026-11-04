"""Generate original WAV assets for the block-breaker exercise."""

import math
import random
import struct
import wave
from pathlib import Path


SAMPLE_RATE = 22050
OUTPUT = Path(__file__).resolve().parents[1] / "SourceAudio"
OUTPUT.mkdir(exist_ok=True)


def write_wave(name, samples):
    path = OUTPUT / name
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, x)) * 32767)) for x in samples))
    print(path)


melody = [523.25, 659.25, 783.99, 659.25, 587.33, 698.46, 880.0, 698.46,
          659.25, 783.99, 987.77, 783.99, 587.33, 698.46, 783.99, 523.25]
bass = [130.81, 146.83, 164.81, 130.81]
music = []
for i in range(SAMPLE_RATE * 8):
    t = i / SAMPLE_RATE
    step = int(t / 0.5)
    local = t % 0.5
    envelope = (1 - math.exp(-local * 45)) * math.exp(-local * 4.5)
    lead = math.sin(2 * math.pi * melody[step] * local) + 0.22 * math.sin(2 * math.pi * melody[step] * 2 * local)
    bass_note = bass[int(t / 2)]
    bass_t = t % 2
    low = math.sin(2 * math.pi * bass_note * bass_t) * (0.65 + 0.35 * math.exp(-bass_t * 2))
    music.append(0.13 * envelope * lead + 0.08 * low)
write_wave("Breakout_BGM.wav", music)

rng = random.Random(2026)
knock = []
for i in range(int(SAMPLE_RATE * 0.18)):
    t = i / SAMPLE_RATE
    envelope = math.exp(-t * 34)
    tone = math.sin(2 * math.pi * (640 - 1500 * t) * t)
    knock.append(0.42 * envelope * (0.8 * tone + 0.2 * rng.uniform(-1, 1)))
write_wave("Breakout_SE_Knock.wav", knock)
