from pydub import AudioSegment
import os

### Initialize these ###
path = "/Users/pratik/research/music/samples/DI by Jason/"
filename = "dis_for_pratik-004.wav"
srno = 1 # Starting order
### ###

subdirectorypath =  path + "di-subsamples/"
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


print(path + filename)
song = AudioSegment.from_wav(path + filename)

for i in range(len(cuts)-1):
	subsamplename = "00000-" + ('%02d' % (i+1)) + " DI.wav"
	print('\t' + subsamplename)

	fullname = subdirectorypath + subsamplename

	song[cuts[i] * 1000 : cuts[i+1] * 1000].export(fullname, format="wav")


