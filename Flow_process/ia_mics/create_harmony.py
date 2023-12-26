import numpy as np
from scipy.io.wavfile import write

T = 180
fs = 44100
f = 440
t = np.arange(0, T, 1/fs)

signal = np.sin(2*np.pi*f*t) + 0.5 * np.sin(2*np.pi*2*f*t) + 0.3 * np.sin(2*np.pi*3*f*t)
signal = signal / np.max(np.abs(signal))

write("output.wav", fs, np.int16(signal * 32767))