from One_data_frame_processes.Localization.Angle.magic_number import angle_coefficient
from One_data_frame_processes.Localization.Ratio.ratio_between_two_nodes import calculate_ratio_of_lobes
from One_data_frame_processes.Localization.Power.array_of_powers import select_max_pair
from One_data_frame_processes.Localization.Angle.angle_from_ratio import find_angle
from One_data_frame_processes.Localization.basic_tools import fft_of_all_channels
from One_data_frame_processes.Classification.Classification_utils.main import main_classification
from constants import *
from scipy.io import wavfile
import numpy as np


def main_process(data_frame, horizontal_lobe_position = True):
    """
    The real time flow takes one data frame at a time, and runs this function on it, to get the angle of the source.
    flow: data -> fft -> classification -> max_pair -> ratio -> angle
    fft is performed on raw data
    classification is performed on raw data
    if classification is true, the angle is calculated
    max pair is calculated on whole integral or around harmonic frequencies, according to the constants
    ratio is calculated on whole integral or around harmonic frequencies, according to the constants
    angle is calculated using constant coefficient, or dynamic coefficient, according to the constants
    :param horizontal_lobe_position: true if lobes are horizontal, false if vertical
    :param data_frame: the data from a certain time window
    :return: angle of the source
    """
    if FIND_ANGLE_ONLY_WHEN_MOTOR_DETECTED_BY_CLASSIFIER:
        classification_results = main_classification(data_frame.T)
    frequencies, amplitudes = fft_of_all_channels(data_frame,start = 0, end = None)  # calculate the fft of all channels

    if FIND_ANGLE_ONLY_WHEN_MOTOR_DETECTED_BY_CLASSIFIER and classification_results[0][0] or not FIND_ANGLE_ONLY_WHEN_MOTOR_DETECTED_BY_CLASSIFIER: # run only if the data is classified as motor
        if not horizontal_lobe_position:
            amplitudes = amplitudes[0:5]  # take only the first 5 channels if the lobes are vertical
        max_pair, power_array = select_max_pair(frequencies, amplitudes)  # find the pair of lobes with the highest power
        ratio = calculate_ratio_of_lobes(max_pair, amplitudes, frequencies, power_array)  # calculate the ratio of the lobes
        coefficient = angle_coefficient(max_pair, ratio)  # calculate the coefficient of the angle
        angle = find_angle(ratio, coefficient, max_pair,horizontal_lobe_position)  # calculate the angle of the source
        return angle
    else:
        return None






