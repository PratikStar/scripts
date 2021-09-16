import os

directory = os.fsencode("/Users/pratik/research/music/samples/Helix Native copy")


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    # print(filename)
    if filename.endswith("-001.wav"): 
        print(filename)
        os.rename(
            "/Users/pratik/research/music/samples/Helix Native/" + filename,
            "/Users/pratik/research/music/samples/Helix Native/" + filename.replace("-001.wav", ".wav")
            )
        continue
    else:
        continue