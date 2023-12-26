import wave

import librosa
import numpy as np
from scipy import signal
import soundfile as sf


def resample_audio(audio_array, original_sr=48000, target_sr=32000):
    """Resample audio to the target sampling rate.

    Args:
      audio_array: NumPy array containing audio samples
      original_sr: Original sampling rate of the audio data (default is 48000)
      target_sr: Target sampling rate for resampling (default is 32000)
    """
    # Resample the audio to the target sampling rate
    return signal.resample(audio_array, int(len(audio_array) * target_sr / original_sr))


def wav_to_np_array(file_path):
    try:
        # Read the WAV file using the soundfile library
        signal, sample_rate = sf.read(file_path)

        # Ensure the signal is in float32 format
        signal = signal.astype(np.float32)

        return signal
    except Exception as e:
        print(f"Error: {e}")
        return None



def load_wav_with_librosa(input_array, sample_rate=None):
    try:
        # Use librosa to load the NumPy array
        y, sr = librosa.load(input_array, sr=sample_rate)

        return y, sr
    except Exception as e:
        print(f"Error: {e}")
        return None, None


def unite_channels(channels):
    return np.mean(channels, axis=1)  # Using NumPy to combine channels
