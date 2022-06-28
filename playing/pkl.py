import pickle

with open('/Users/pratik/My Drive/utokyo/08. research/Music/VAE/spectrogram-2022-test/min_max_values.pkl', 'rb') as f:
    data = pickle.load(f)
    print((data))