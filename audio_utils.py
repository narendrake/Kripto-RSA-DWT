import numpy as np
from scipy.io import wavfile

def read_wav(filename):
    rate, data = wavfile.read(filename)
    return rate, data

def write_wav(filename, rate, data):
    wavfile.write(filename, rate, data.astype(np.int16))
