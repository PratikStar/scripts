from pydub import AudioSegment, silence
import os
from pathlib import Path

### Initialize these ###
path = Path("/Users/pratik/data/timbre/clips")
filename = "09A DI.wav"
### ###

sound = AudioSegment.from_wav(path / filename)
cut = sound[96 * 1000: 100.7 * 1000]

def get_details(sound):
    # sound = AudioSegment.from_wav(path / filename)
    print(f"Number of channels: {sound.channels}")
    print(f"Duration in seconds: {sound.duration_seconds}")
    print(f"frame_rate: {sound.frame_rate}")
    print(f"frame_count: {sound.frame_count()}")

    print(f"Loudness in dbFS: {sound.dBFS}")
    print(f"Number of bytes in each sample (sample_width): {sound.sample_width}")
    print(f"Number of bytes for each \"frame\": {sound.frame_width}")

    samples = list(sound.set_channels(1).get_array_of_samples())
    print(f"zeroes in samples: {samples.count(0)}")
    # print(f"First 100 samples: {samples[:100]}")
    # print(f"Last 100 samples: {samples[-100:]}")


get_details(cut)


cut.export(path/"000 temp.wav", format="wav")

# pathnsynth = Path("/Users/pratik/data/nsynth-test/audio")
# filenamensynth = "bass_electronic_018-037-100.wav"
# nsynth = AudioSegment.from_wav(pathnsynth / filenamensynth)
