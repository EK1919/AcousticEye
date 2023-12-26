import numpy as np
from constants import *
def fft_of_one_channel(time_domain_data, start = 0, end = None):
    """
    This function returns the fft of the time domain data
    :param time_domain_data:
    :param start:
    :param end:
    :return:
    """


    frequencies = np.fft.fftfreq(len(time_domain_data), 1/SF)
    low_bound = np.where(frequencies == start)[0][0]
    if end == None:
        high_bound = len(time_domain_data)
    else:
        high_bound = np.where(frequencies == end)[0][0]

    frequency_domain_data = np.fft.fft(time_domain_data)
    return frequencies[low_bound,high_bound], frequency_domain_data[low_bound,high_bound]

def fft_of_all_channels(time_domain_data, start = 0, end = None):
    """
    This function returns the fft of the time domain data for all channels
    received in a two-dimensional array
    :param time_domain_data:
    :param start:
    :param end:
    :return:
    """
    frequencies = np.fft.fftfreq(len(time_domain_data[0]), 1/SF)
    low_bound = np.where(frequencies == start)[0][0]
    if end is None:
        high_bound = len(time_domain_data[0])
    else:
        high_bound = np.where(frequencies == end)[0][0]

    frequency_domain_data = np.abs(np.fft.fft(time_domain_data, axis=1))
    return frequencies[low_bound:high_bound], frequency_domain_data[low_bound:high_bound]

def normalize_array(array):
    """
    This function normalizes an array
    :param array:
    :return:
    """
    return array / np.max(array)

def apply_hann_window(data):
    """
    This function applies a Hann window on the data
    :param data:
    :return:
    """
    return np.hanning(len(data)) * data

def apply_function_on_all_channels(data, function, *args, **kwargs):
    """
    This function applies a function on all channels
    :param data:
    :param function:
    :return:
    """
    result = []
    for i in range(len(data)):
        result.append(function(data[i], args, kwargs))
    return result

def convert_amp_to_db(amps):
    return 20 * np.log10(amps)

def normalize_all_channels(data):
    maximumm = 0
    for ch in data:
        maximumm = max(max(ch), maximumm)
    return data / maximumm



