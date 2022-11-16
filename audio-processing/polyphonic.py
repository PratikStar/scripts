from pydub import AudioSegment
import os
from pathlib import Path

### Initialize these ###
path = Path("/Users/pratik/data/timbre/clips")
### ###

cuts = [  # 13 passages
    [0.3, 8],  # mono
    [9.6, 16.5],  # poly
    [18.4, 26.5],  # poly
    [27.4, 34],  # poly
    [35.7, 41.6],  # poly
    [44, 51.7],  # mono. but last strum
    [53.5, 60.5],  # mono. but three strum in the middle
    [61.4, 70],  # mono.
    [71.55, 78.65],  # mono
    [78.65, 84.5],  # poly
    [84.5, 90.2],  # mono
    [90.5, 95.3],  # mono # 12th clip
    [96, 100.7]  # mono
]

monophonic = [0,
              5,  # a chord is strummed at the end, but rest of the clip is monophonic
              6,
              7,  # seems two strings are plucked in the mid
              8,
              10,
              11,
              12]
polyphonic = [1, 2, 3, 4, 9]

mono_path = path / '..' / 'monophonic'
poly_path = path / '..' / 'polyphonic'

if not os.path.exists(mono_path):
    os.mkdir(mono_path)
if not os.path.exists(poly_path):
    os.mkdir(poly_path)


for source_file in os.listdir(path):
    if not source_file.endswith('.wav'):
        continue
    print(f"Loading {source_file}")
    song = AudioSegment.from_wav(path / source_file).set_channels(1)

    # print(f"\tProcessing monophonic passages...")
    # suffix = 1
    # for i in range(len(cuts)):
    #     if i not in monophonic:
    #         continue
    #     cut = song[cuts[i][0] * 1000: cuts[i][1] * 1000]
    #
    #     cut.export(mono_path / source_file.replace('.wav', f" - {suffix} .wav"), format="wav")
    #     suffix += 1

    # break
    print(f"\tProcessing polyphonic passages...")
    suffix = 1
    for i in range(len(cuts)):
        if i not in polyphonic:
            continue
        cut = song[cuts[i][0] * 1000: cuts[i][1] * 1000]
        cut.export(poly_path / source_file.replace('.wav', f" - {suffix} .wav"), format="wav")
        suffix += 1
