from ..Classification_utils.Motor_Classification import which_motor
from ..Classification_utils.Motor_Detection import is_motor
# from Signal_Proccesing import wav_to_np_array

def is_motor_mult_channels(mult_channel_input):
    """

    :param mult_channel_input:
    :return:
    """
    result = []
    for i in range(mult_channel_input.shape[1]):
        result.append(is_motor(mult_channel_input[:, i][None, :]))
    return result

def which_motor_mult_channels(mult_channel_input):
    """

    :param mult_channel_input:
    :return:
    """
    result = []
    for i in range(mult_channel_input.shape[1]):
        result.append(which_motor(mult_channel_input[:, i][None, :]))
    return result

def main_classification(data_frame):
    """
    returns a tuple of two arrays:
    first array is a boolean array of whether each channel is a motor or not, and the probability of it being a motor
    second array is an array of the motor type for each channel, and the probability of it being that type

    :param data_frame:
    :return:
    """
    is_motor = is_motor_mult_channels(data_frame)
    return is_motor, which_motor_mult_channels(data_frame)

