import logging
import os
import threading
import time
import warnings
from collections import deque
from collections import namedtuple
import datetime as d2
from datetime import datetime
from queue import Queue
from colorama import Fore, Back, Style
import numpy as np
from scipy.io import wavfile
import json
import enum
from Flow_process.sentinel_client_elta.log_print import *
from multiprocessing import Process

# class e_MIC_UNIT_STATUS(int, enum.Enum):
#     e_MIC_UNIT_STATUS_NOT_CONNECTED = 0
#     e_MIC_UNIT_STATUS_CONNECTED = 1


class ExtendedAcousticData():
    def __init__(self, acoustic_arr):
        self.msg_time = datetime.now()
        self.acoustic_arr = acoustic_arr        


class MetaData():
    def __init__(self, temp, humid, ses_lat, ses_long, ses_alt, platform, mic_xyz_location, recording_place="somewhere"):
        self.temp = temp
        self.humid = humid
        self.ses_lat = ses_lat
        self.ses_long = ses_long
        self.ses_alt = ses_alt        
        self.platform = platform #octave, rotem, othelo
        self.mic_xyz_location = mic_xyz_location # mic XYZ
        self.recording_place = recording_place


class MicStatus():
    def __init__(self,name,id,is_connected=0,is_transmited=0):
        self.name = name
        self.id = id
        self.is_connected = is_connected
        self.is_transmited = is_transmited
        self.dead_channels = []
        self.noisy_channels = []

class MicApiBase(threading.Thread):
    MAX_MEMORY_CAPACITY_MB = 500
    MAX_MEMORY_CAPACITY_BYTES = MAX_MEMORY_CAPACITY_MB * 1024 * 1024 * 8  # 500MB

    frame = namedtuple("frame", 'time data sns')

    def __init__(self,system_name, device_id=1, sample_rate=32000, sample_time_in_sec=1):
        threading.Thread.__init__(self)

        self.system_name = system_name
        self.device_id = device_id
        self.sample_rate = sample_rate
        self.sample_time_in_sec = sample_time_in_sec
        self.sample_size = int(sample_rate * sample_time_in_sec)
        self.save_stream = False

        self._is_connected = False
        self._is_transmited = False
        self._play_mode = True

        self._num_of_channels = 1

        self.max_queue_len = int(
            self.MAX_MEMORY_CAPACITY_MB / ((self.sample_rate * self._num_of_channels * 32) / 8 / 1024 ** 2))
        self.f_lock = threading.Lock()

        self.raw_data = None
        
        self.frames = deque()
        self.all_frames = Queue(maxsize=self.max_queue_len)

        self.format_file = 'int16'
        self.start_time = None
        self.last_write_time = None

        # logger
        self.logger = logging.getLogger()

        self.write_mic_loc = False
        self._mic_loc = []

        self.distances = {"mic_1_2": 0.7,
                          "mic_1_4": 0.7,
                          "mic_2_3": 0.7,
                          "mic_2_4": 0.7,
                          "mic_3_1": 0.7,
                          "mic_3_4": 0.7}

        self.calc_mic_locations()
        
        self._mic_status = MicStatus(self.name,self.device_id)
        self.mic_status_need_update = False
        self.meta_data = MetaData(0, 0, "lat", "long", "alt", "raptor-F22", "mic_xyz_location", "caribien_sea" )

    @property
    def is_connected(self):
        return self._is_connected

    @is_connected.setter
    def is_connected(self, connection_state):
        self._is_connected = connection_state

    @property
    def is_transmited(self):
        return self._is_transmited

    @is_transmited.setter
    def is_transmited(self, transmit_state):
        self._is_transmited = transmit_state

    @property
    def rate(self):
        return self.sample_rate

    @property
    def num_of_channels(self):
        return self._num_of_channels

    @num_of_channels.setter
    def num_of_channels(self, num):
        self._num_of_channels = num

    @property
    def name(self):
        return f'{self.__class__.__name__}_{self.device_id}'

    @property
    def play_mode(self):
        return self._play_mode

    @property
    def mic_loc_str(self):
        return self._mic_loc


    @play_mode.setter
    def play_mode(self, mode):
        self._play_mode = mode
    

    def update_metadata(self, temp, humid, ses_lat, ses_long, ses_alt, platform, mic_xyz_location, recording_place):
        self.meta_data.temp = temp
        self.meta_data.humid = humid
        self.meta_data.ses_lat = ses_lat
        self.meta_data.ses_long = ses_long
        self.meta_data.ses_alt = ses_alt
        self.meta_data.platform = platform
        self.meta_data.mic_xyz_location = mic_xyz_location
        self.meta_data.recording_place = recording_place


    def calc_mic_locations(self):
        # ## Rahash Kal
        # mic1 = [0, - self.distances['mic_1_2'], 0]
        # mic2 = [- self.distances['mic_2_3'], 0, 0]
        # mic3 = [0, 0, 0]
        # mic4 = [0, 0, - self.distances['mic_3_4']]
        # self.mic_loc = np.array([mic1, mic2, mic3, mic4])

        mic = [0, 0, 0]
        self._mic_loc = np.array([mic, mic, mic, mic])

    @property
    def mic_loc(self):
        return self._mic_loc

    @property
    def mic_status(self):
        return self._mic_status.__dict__

    def set_mic_status(self,frame):
        if self.is_connected:
            self._mic_status.is_connected = 1
        if self.is_transmited:
            self._mic_status.is_transmited = 1
            self.calc_channels(frame)

    def calc_channels(self,frame):
        std_vec_1 = np.std(frame,axis=1)
        dead_ch_vec = np.where(std_vec_1 == 0)
        noisy_ch_vec = np.where(std_vec_1 > np.min(std_vec_1)*10)
        self._mic_status.dead_channels = dead_ch_vec[0].tolist()
        self._mic_status.noisy_channels = noisy_ch_vec[0].tolist()

    def get_mic_api_list(self):
        return [self]

    def run(self) -> None:
        # self.start_time = datetime.now() if not self.start_time else self.start_time
        self._run()

    def _run(self):
        pass

    def pause(self):
        self.play_mode = False

    def play(self):
        self.play_mode = True
        
    def set_save_stream(self, save_stream):
        self.save_stream = save_stream

    """
    :return: The Last Frame Recorded from Mic, a tuple (time, data, sensor)
    if there is no data, it will return the data as null
    """
    def get_frame(self, block=True):
        num_of_frames = len(self.frames)
        # print("num_of_frames",Fore.RED + str(num_of_frames))
        # print(Style.RESET_ALL)
        if num_of_frames - 1 > 5:
            warnings.warn(f"There are {num_of_frames} in Queue, your'e working in semi-real time")
            logPrint("WARN", E_LogPrint.LOG, f"There are {num_of_frames} in Queue, your'e working in semi-real time")


        # returning last frame
        frame = None
        if self.frames:
            self.f_lock.acquire()
            frame = self.frames.pop()
            self.f_lock.release()
        else:
            frame = self.frame(datetime.now(), None, self.device_id)
        
        return frame
        # return self.frames.pop() if self.frames else self.frame(datetime.now(), None, self.device_id)

    def write_mic_location(self,location=os.path.abspath('./results/')):
        if not os.path.exists(location):
            os.makedirs(location)
        file_name = f"mic_locations.npy"
        mic_loc_file_path = os.path.join(location, file_name)
        if not file_name in os.listdir(location):
            try:            
                with open(mic_loc_file_path, 'wb') as f:
                    np.save(f, self._mic_loc)
                    logPrint("INFO", E_LogPrint.BOTH, f"save {file_name} for {self.name} to {mic_loc_file_path}", bcolors.OKBLUE)                
                    self.write_mic_loc = True
            except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
                logPrint("ERROR", E_LogPrint.BOTH, f"failed to save mic_locations for {self.name}", bcolors.FAIL)                
        else:
            self.write_mic_loc = True
    
    def clear_all_frames(self, old_delete_time, is_clear_all=False):
        self.f_lock.acquire()
        keep_msgs = []
        if is_clear_all:
          self.all_frames.queue.clear()          
        else:    
            while not self.all_frames.empty():
                one_msg = self.all_frames.get()
                if one_msg.msg_time >= old_delete_time:
                    keep_msgs.append(one_msg)
            for msg in keep_msgs:
                self.all_frames.put(msg)
        self.f_lock.release()   
    
    def write_to_file(self, location=os.path.abspath('./results/'), sec_to_record=30):
        if not self.write_mic_loc:
            self.write_mic_location(location)

        # check if date doesn't change (in case the computer doesn't have date at reboot)
        d_now = datetime.now()
        if d_now.date() > self.start_time.date():
            self.start_time = d_now

        file_time = self.start_time.strftime("%Y%m%d-%H%M%S.%f")
        file_name=f'i_love_{self.system_name}_{self.name}_{file_time}_{sec_to_record}.wav'
        file_path = os.path.join(location, file_name)
        # self.start_time += d2.timedelta(0, sec_to_record)

        frames_to_write = []
        self.f_lock.acquire()
        while not self.all_frames.empty():
            ex_acoustic_data = self.all_frames.get()
            frames_to_write.append(ex_acoustic_data.acoustic_arr)
        self.f_lock.release()

        if len(frames_to_write) == 0:
            logPrint( "WARN", E_LogPrint.LOG, f"no frames - skip writing sound file", bcolors.WARNING)
            return

        #TBD - need to calculate according to request frame time length in sec 
        self.start_time += d2.timedelta(0, len(frames_to_write))

        logPrint( "INFO", E_LogPrint.LOG, f"writing {len(frames_to_write)} frames to sound file")

        #write_files_process = Process(target=self._write_sound_files, args=[frames_to_write,self.format_file,file_path, self.sample_rate])
        # write_files_process.start()
        try:
            data, b_count = np.concatenate(frames_to_write), len(frames_to_write)
            data = data.astype(self.format_file)

            # updating last write time
            if self.last_write_time:
                self.last_write_time += d2.timedelta(0, self.sample_time_in_sec * b_count)

            wavfile.write(file_path, self.sample_rate, data)
            self.add_metadata(file_path)
            
        except Exception as ex:
            logPrint("ERROR", E_LogPrint.BOTH, f'Failed to write {file_path} - {ex}', bcolors.FAIL)

        return frames_to_write

    def add_metadata(self, file_path):
        pass


    @staticmethod
    def _write_sound_files(frames_to_write,format_file,file_path,sample_rate): 
        logPrint("INFO", E_LogPrint.BOTH, "Process _write_sound_files started")
        try:
            data = np.concatenate(frames_to_write)
            data = data.astype(format_file)

            wavfile.write(file_path, sample_rate, data)
            return;
        except Exception as ex:
            logPrint("ERROR", E_LogPrint.BOTH, f'Failed to write {file_path} - {ex}', bcolors.FAIL)


# changed 18.1.23 version 3.0.0 - by rami
    # writing events file moved from classifier external defined process to current location
    # save stream default value changed to False (gonen)
    # file signature time was changed to represents actual time
# changed in version 3.1.0 - by gonen
    # add MetaData class to enable adding metadata when saving wav file (currently used by syncope api alone) to enable in all mic APIs should update image with taglib
# changed by gonen in version 3.2.0:    
    # update metadata stored fields