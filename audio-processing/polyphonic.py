from pydub import AudioSegment
import os
from pathlib import Path

### Initialize these ###
path = Path("/Users/pratik/data/timbre/clips")
### ###

cuts = [  # 12 passages
    0,
    9,
    17.5,
    27,  # Maybe not?
    35,
    43,
    53,
    61,  # 7
    71,
    78.65,
    84.5,
    90.5,  # 12th clip
    101  # nothing after this clip
]

monophonic = [0,
              5,  # a chord is strummed at the end, but rest of the clip is monophonic
              6,  # seems two strings are plucked in the mid
              8,
              10,
              11]
polyphonic = [1, 2, 3, 4, 7, 9]


mono_path = path / 'monophonic'
poly_path = path / 'polyphonic'

if not os.path.exists(mono_path):
    os.mkdir(mono_path)
if not os.path.exists(poly_path):
    os.mkdir(poly_path)


for source_file in os.listdir(path):
	if not source_file.endswith('.wav'):
		continue
	print(f"Cutting {source_file}")
	song = AudioSegment.from_wav(path / source_file)

	print(f"\tProcessing monophonic passages...")
	mono_clip = None
	for i in range(len(cuts) - 1):
		if i not in monophonic:
			continue
		cut = song[cuts[i] * 1000: cuts[i + 1] * 1000]
		if mono_clip is None:
			mono_clip = cut
		else:
			mono_clip += cut
	mono_clip.export(mono_path/source_file, format="wav")

	print(f"\tProcessing polyphonic passages...")
	poly_clip = None
	for i in range(len(cuts) - 1):
		if i not in polyphonic:
			continue
		cut = song[cuts[i] * 1000: cuts[i + 1] * 1000]
		if poly_clip is None:
			poly_clip = cut
		else:
			poly_clip += cut
	poly_clip.export(poly_path/source_file, format="wav")
