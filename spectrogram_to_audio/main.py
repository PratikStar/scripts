import librosa
import numpy as np

# read file
file    = "test.wav"
sig, fs = librosa.core.load(file, sr=8000)

exit()
# process
abs_spectrogram = np.abs(librosa.core.spectrum.stft(sig))
audio_signal = librosa.core.spectrum.griffinlim(abs_spectrogram)

print(audio_signal, audio_signal.shape)

# write output
librosa.output.write_wav('test2.wav', audio_signal, fs)