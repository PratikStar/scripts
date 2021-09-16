import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from sklearn.preprocessing import MinMaxScaler


data = load_iris()
X = data.data




scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)


