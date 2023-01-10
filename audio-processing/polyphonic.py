from pydub import AudioSegment
import os, re
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
    [44, 50.5],  # mono. removed the last strum (50 - 51.x)
    [53.5, 60.5],  # poly! (OLD interpretation: mono. but three strum in the middle)
    [61.4, 70],  # poly! (OLD interpretation: mono)
    [72.85, 78.65],  # mono (removed the first second of power chord)
    [78.65, 84.5],  # poly
    [84.5, 90.2],  # mono (extend start?)
    [90.5, 95.3],  # mono # 12th clip
    [96, 100.7]  # mono
]

monophonic = [0,
              5,  # a chord is strummed at the end, but rest of the clip is monophonic
              # 6,
              # 7,  # seems two strings are plucked in the mid
              8,
              10,
              11,
              12]
polyphonic = [1, 2, 3, 4, 9]

mono_path = path / '..' / 'monophonic-tmp'
poly_path = path / '..' / 'polyphonic'

if not os.path.exists(mono_path):
    os.mkdir(mono_path)
    os.mkdir(mono_path / 'test')
if not os.path.exists(poly_path):
    os.mkdir(poly_path)
    os.mkdir(poly_path / 'test')

regex = ".*"


for source_file in sorted(os.listdir(path)):
    if not source_file.endswith('.wav'):
        continue
    if not re.search(regex, source_file):
        continue
    print(f"Loading {source_file}")
    song = AudioSegment.from_wav(path / source_file).set_channels(1)

    allsound = None
    print(f"\tProcessing monophonic passages...")
    # suffix = 1
    for i in range(len(cuts)):
        if i not in monophonic:
            continue
        cut = song[cuts[i][0] * 1000: cuts[i][1] * 1000]

        # cut.export(mono_path / source_file.replace('.wav', f" - {suffix} .wav"), format="wav")
        # suffix += 1
        if allsound is None:
            allsound = cut
        else:
            # print("appending")
            allsound = allsound.append(cut,  crossfade=0)

    slices = allsound[::4000]

    i = 1
    for sl in slices:
        if i == 6:
            dest_file_name = f"{mono_path}/test/{source_file.split('.wav')[0]} - {i}.wav"
        else:
            dest_file_name = f"{mono_path}/{source_file.split('.wav')[0]} - {i}.wav"
        sl.export(dest_file_name, format="wav")
        i += 1

    # break
    # print(f"\tProcessing polyphonic passages...")
    # suffix = 1
    # for i in range(len(cuts)):
    #     if i not in polyphonic:
    #         continue
    #     cut = song[cuts[i][0] * 1000: cuts[i][1] * 1000]
    #     cut.export(poly_path / source_file.replace('.wav', f" - {suffix} .wav"), format="wav")
    #     suffix += 1
