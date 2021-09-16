from pydub import AudioSegment
import os

### Initialize these ###
path = "/Users/pratik/research/music/samples/Helix Native copy"
srno = 1 # Starting order
### ###

directory = os.fsencode(path)
subdirectorypath = path + "/subsamples-mp3/"
cuts = [
	0,
	9,
	17.5,
	27, # Maybe not?
	35,
	43,
	53,
	61,
	71,
	78.65,
	84.5,
	90.5,
	101
	]

if not os.path.exists(subdirectorypath):
	os.mkdir(subdirectorypath)

files = os.listdir(directory)
sorted_files = sorted(files)
for file in sorted_files:
	filename = os.fsdecode(file)

	if not filename.endswith(".wav"): 
		continue

	print(filename)
	song = AudioSegment.from_wav(path + "/" + filename)
	
	for i in range(len(cuts)-1):
		subsamplename = ('%05d' % srno) + "-" + ('%02d' % (i+1)) + " " + filename.replace('.wav', '.mp3')
		print('\t' + subsamplename)

		fullname = subdirectorypath + subsamplename

		song[cuts[i] * 1000 : cuts[i+1] * 1000].export(fullname, format="mp3")
	srno +=1


