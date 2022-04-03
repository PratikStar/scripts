from pydub import AudioSegment
import os

### Initialize these ###
path = "/Users/pratik/research/music/samples/Helix Native copy"
srno = 1 # Starting order
### ###

directory = os.fsencode(path)
subdirectorypath = path + "/subsamples-mp3/"
# cuts = [
# 	0,
# 	9,
# 	17.5,
# 	27, # Maybe not?
# 	35,
# 	43,
# 	53,
# 	61,
# 	71,
# 	78.65,
# 	84.5,
# 	90.5,
# 	101
# 	]

# rock = [
# "00:00:00", 
# "00:04:19", 
# "00:09:24", 
# "00:15:20", 
# "00:20:23", 
# "00:26:25", 
# "00:35:00", 
# "00:39:06", 
# "00:41:55", 
# "00:45:48", 
# "00:50:06", 
# "00:55:15", 
# "01:00:08", 
# "01:05:57", 
# "01:07:19", 
# "01:10:49", 
# "01:14:45", 
# "01:19:00", 
# "01:23:38", 
# "01:28:08",
# "01:29:27"
# ]

# rock_acous = [
# "00:00:00",
# "00:01:44", 
# "00:02:25", 
# "00:03:29", 
# "00:04:57", 
# "00:08:48", 
# "00:10:53", 
# "00:12:50",
# "00:13:57"
# ]
# cuts = []

# for ts in rock_acous:
# 	t = ts.split(":")
# 	cut=0
# 	cut += int(t[len(t)-1])
# 	cut += int(t[len(t)-2]) *60
# 	cut += int(t[len(t)-3]) *3600

# 	cuts.append(cut)
# print(cuts)


song = AudioSegment.from_wav("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/other.wav")

song[ 38 * 1000 : 39 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/livin-on-a-prayer.wav")
song[ 262 * 1000 : 263 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/smells-like-teen-spirit.wav")
song[ 570 * 1000 : 571 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/sweet-child-o-mine.wav")
song[ 979 * 1000 : 980 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/black-hole-sun.wav")
song[ 781 * 1000 : 782 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/sultans-of-swing.wav")
song[ 1462 * 1000 : 1463 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/november-rain.wav")
song[ 2111 * 1000 : 2112 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/here-i-go-again.wav")



song[ 2356 * 1000 : 2357 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/basket-case.wav")


song[ 2520 * 1000 : 2521 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/eye-of-the-tiger.wav")


# song[ 781 * 1000 : 782 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/losing-my-religion.wav")
# song[ 781 * 1000 : 782 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/with-or-without-you.wav")
song[ 3504 * 1000 : 3505 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/heart-shaped-box.wav")

# song[ 781 * 1000 : 782 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/money-of-nothing.wav")
# song[ 781 * 1000 : 782 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/nothing-else-matters.wav")
# song[ 781 * 1000 : 782 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/you-shook-me-all-night-long.wav")
# song[ 781 * 1000 : 782 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/tears-in-heaven.wav")
# song[ 781 * 1000 : 782 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/strat-me-up.wav")
# song[ 781 * 1000 : 782 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/thunderstruck.wav")
# song[ 781 * 1000 : 782 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/welcome-to-the-jungle.wav")
# song[ 781 * 1000 : 782 * 1000].export("/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-samples/come-as-you-are.wav")

exit()
for i in range(len(cuts)-1):
	subsamplename = "rock-acoustic-" + ('%02d' % (i+1)) + " .wav"
	print('\t' + subsamplename)
	print('\t\t' + 'From: ' + str(cuts[i]) + " to: " + str(cuts[i+1]))

	fullname = "/Users/pratik/My Drive/08. research/Music/VAE/audio-test/rock-acoustic-songs/" + subsamplename

	song[cuts[i] * 1000 : cuts[i+1] * 1000].export(fullname)
exit()

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


