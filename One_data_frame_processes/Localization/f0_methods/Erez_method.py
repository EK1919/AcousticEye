import numpy as np
from constants import *
from scipy.signal import find_peaks
from ..basic_tools import fft_of_all_channels, normalize_array, fft_of_one_channel

def find_local_maxima(amps):
    """"
    This function finds the local maxima of the given amplitudes"""
    maximas, _ = find_peaks(amps, height=0, threshold = STR_THRESHOLD ,prominence=STR_PROMINENCE)
    maximas = [i for i in maximas if STR_LOW_FREQ < i < STR_HIGH_FREQ]
    return maximas

def a_close_to_b(x, y, threshold):
    """
    This function checks if a is close to b
    :param x:
    :param y:
    :param threshold: allowed distance between a and b
    :return: true if a is close to b, false otherwise
    """
    return np.abs(x - y) < threshold


def find_harmonics(freqs, amps, maximas):
    """
    This function finds the harmonics of the given frequencies out of the option pool which is local maximas
    :param freqs:
    :param amps:
    :param maximas:
    :return:
    """
    harmonics = []
    for val in range(len(maximas)):
        harmonic_count = 2  # multiple of frequency we are looking for
        i = val  # index of current frequency
        options = []
        while i<len(maximas) and harmonic_count <= STR_HARMONICS:
            if a_close_to_b(freqs[maximas[i]], freqs[maximas[val]]*harmonic_count, harmonic_count*STR_WIDTH):
                options.append((maximas[i], amps[maximas[i]]))
            elif len(options) > 0:
                maximal_option = max(options, key=lambda x: x[1])
                if harmonic_count == 2:
                    harmonics.append([maximas[val],maximal_option[0]])
                else:
                    harmonics[-1].append(maximal_option[0])
                harmonic_count += 1

                options = []

            if freqs[maximas[i]]>harmonic_count*freqs[maximas[val]]+harmonic_count*STR_WIDTH:
                break
            i += 1


        if len(options) > 0:
            maximal_option = max(options, key=lambda x: x[1])
            if harmonic_count == 2:
                harmonics.append([maximas[val], maximal_option[0]])
            else:
                harmonics[-1].append(maximal_option[0])

    return harmonics


def slice_audio(data, start_time, end_time):
    start_idx = int(start_time * SF)
    end_idx = int(end_time * SF)
    return data[start_idx:end_idx]



def main_process(freqs, amps):
    maximas = find_local_maxima(amps)
    harmonic_maximas = find_harmonics(freqs, amps, maximas)
    return harmonic_maximas


def calculate_strength(dic, amps, freqs):
    average = np.mean(amps)
    strength_list = []
    for key in range(len(dic)):
        values = dic[key]
        strength_per_key = 0
        for i in range(-STR_K, STR_K+1):
            strength_per_val = 0
            for val in range(len(values)):
                if values[val]+i >= len(freqs):
                    continue
                strength_per_val += (0.25**np.abs(i-1)) * (amps[values[val]+i]-average)**2  # give most strength to second harmonic
            strength_per_key += strength_per_val
        strength_list.append(strength_per_key)
    return strength_list

def perform_erez_method_on_one_channel(data, domain, freqs = None):
    """
    This function finds the frequencies which comprise the most dominant harmonic group
    it is done by finding the local maximas, and then finding the harmonics of each local maxima
    then a calculation is done to find the most dominant group
    :param data: nparray of the data
    :param domain: 'time' or 'frequency'
    :param freqs:
    :return: a list of frequencies and the strength of the group
    """
    if domain == 'time':
        freq, ampl = fft_of_one_channel(data, STR_LOW_FREQ, STR_HIGH_FREQ)
    elif domain == 'frequency':
        freq = freqs
        ampl = data


    all_harmonic_lists = main_process(freq, ampl)
    if len(all_harmonic_lists) == 0:
        return [freq[np.argmax(ampl)]], np.max(ampl) - np.mean(ampl)
    strengths_of_each_group = (calculate_strength(all_harmonic_lists, ampl, freq))
    strongest_group = np.argmax(strengths_of_each_group)
    frequencies_of_group = [freq[idx] for idx in all_harmonic_lists[strongest_group]]
    return frequencies_of_group, np.max(strengths_of_each_group)



