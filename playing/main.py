import numpy as np

db_spectrogram = np.array([[1,28.553274154663086,3], [-51.44672393798828,5,6]])
print("db_spectrogram")
print(db_spectrogram)
min_value,max_value = 0, 1
og_db_min, og_db_max = db_spectrogram.min(), db_spectrogram.max()
print("Min: {}".format(og_db_min))
print("Max: {}".format(og_db_max))

normalized_db_spectrogram = (db_spectrogram - db_spectrogram.min()) / (db_spectrogram.max() - db_spectrogram.min())

normalized_db_spectrogram = normalized_db_spectrogram * (max_value - min_value) + min_value
print("normalized_db_spectrogram")
print(normalized_db_spectrogram)

###########################################################################



############### SPECTROGRAM --> denormalize --> db_to_amplitude --> griffinlim --> AUDIO
denormalized_db_spectrogram = (normalized_db_spectrogram - min_value) / (max_value - min_value)
denormalized_db_spectrogram = denormalized_db_spectrogram * (og_db_max - og_db_min) + og_db_min
print("denormalized_db_spectrogram")
print(denormalized_db_spectrogram)


d = (db_spectrogram - denormalized_db_spectrogram)
if np.allclose(db_spectrogram, denormalized_db_spectrogram):
    print("NOrmalization reversed")

print(d)