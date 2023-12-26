from Localization.Angle.magic_number import angle_coefficient
from Localization.Ratio.ratio_between_two_nodes import calculate_ratio_of_lobes
from Localization.Power.array_of_powers import select_max_pair
from Localization.Angle.angle_from_ratio import find_angle
from Localization.basic_tools import fft_of_all_channels
from One_data_frame_processes.Classification.Classification_utils.main import main_classification
from constants import *

def main_process(data_frame, horizontal_lobe_position = True):
    """
    This function is the main process of the system
    :param data_frame: the data from a certain time window
    :return: angle of the source
    """
    frequencies, amplitudes = fft_of_all_channels(data_frame)  # calculate the fft of all channels
    classification_results = main_classification(data_frame)  # classify the data
    if classification_results[0] or not FIND_ANGLE_ONLY_WHEN_MOTOR_DETECTED: # run only if the data is classified as motor
        if not horizontal_lobe_position:
            amplitudes = amplitudes[0:5]  # take only the first 5 channels if the lobes are vertical
        max_pair, power_array = select_max_pair(frequencies, amplitudes)  # find the pair of lobes with the highest power
        ratio = calculate_ratio_of_lobes(max_pair, amplitudes, frequencies, power_array)  # calculate the ratio of the lobes
        coefficient = angle_coefficient(max_pair, ratio)  # calculate the coefficient of the angle
        angle = find_angle(ratio, coefficient, max_pair,horizontal_lobe_position)  # calculate the angle of the source
        return angle
    else:
        return None


