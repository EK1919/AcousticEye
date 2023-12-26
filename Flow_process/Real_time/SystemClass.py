from constants import *
import threading
from Flow_process.ia_mics.iaAAMic import AAMic
from datetime import datetime, timedelta
import numpy as np
from real_time_graphs import RealTimeGraphs
import time
import matplotlib.pyplot as plt
from One_data_frame_processes.main_process import main_process


class SensorDataProcessor:
    """
    This class is responsible for the real time processing the data
    received from the system.
    """
    def __init__(self, sample_time=SAMPLE_FROM_MIC, total_time=TOTAL_TIME):
        self.sample_time = sample_time  # sample time taken from system in seconds
        self.total_time = total_time  # total time to run the system in seconds
        self.frame_num = int(total_time // sample_time)
        self.sensor_data = []
        self.sensor_times = []
        self.lock = threading.Lock()
        self.mic = AAMic(sample_time_in_sec=self.sample_time)  # initialize the mic class
        self.s_time = datetime.now()
        self.graphs_properties = {}

    def main(self):
        """
        This function is the main function of the class.
        It runs the system for the total time and updates the graphs
        For each frame received from the system.
        :return:
        """
        real_time_graphs = RealTimeGraphs()  # intialize graphs class
        real_time_graphs.initialize_graph_inner("angle as a function of time", "t[s]", "selected_lobe")
        self.mic.start()  # start the system
        self.s_time = datetime.now()  # start time
        time_from_recv = datetime.now()
        time_of_first_frame = 0  # time of first frame
        first_time = True
        while datetime.now() - self.s_time < timedelta(seconds=self.total_time):  # run for total time
            fr = self.mic.get_frame(block=False)  # get frame from system
            curr_data = fr[1]
            curr_time = fr[0]
            if curr_data is not None and curr_time is not None:
                if first_time:
                    first_time = False
                    time_of_first_frame = curr_time
                sum_of_time = curr_time - time_of_first_frame
                angle = main_process(curr_data)  # process the data from one frame processes
                real_time_graphs.update_graph_inner("angle as a function of time", sum_of_time, angle, False)  # update the graphs
            sleep_time = timedelta(seconds=self.sample_time) - (datetime.now() - time_from_recv)
            time_from_recv = datetime.now()
            sleep_seconds = sleep_time.total_seconds() / 2
            plt.pause(max(sleep_seconds, 0.01))
        self.mic.stop()

    def write_file(self):
        self.mic.start()
        time.sleep(11)
        self.mic.write_to_file(sec_to_record=11)
        self.mic.stop()


if __name__ == "__main__":
    processor = SensorDataProcessor()
    processor.main()
