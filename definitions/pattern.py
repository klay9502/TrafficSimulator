import logging
import random
import pandas as pd
import numpy as np

class Pattern:
    def __init__(self, env, time_interval, vehicle_pattern_file_path, ped_pattern_file_path, gauss_standard_deviation) -> None:
        self.env = env
        self.time_interval = time_interval
        self.vehicle_path = vehicle_pattern_file_path
        self.ped_path = ped_pattern_file_path
        self.gauss_standard_deviation = gauss_standard_deviation

        self.vehlcie_list_data = np.empty((0, 0))
        self.ped_list_data = np.empty((0, 0))

        self.now_time = 0
        self.old_env_time = 0.0

        self.read_file()
        self.action = env.process(self.time_update())

    def read_file(self):
        vehicle_data = pd.read_csv(self.vehicle_path)
        ped_data = pd.read_csv(self.ped_path)

        # Convert type dataframe to numpy array.
        self.vehlcie_list_data = vehicle_data.__array__()
        self.ped_list_data = ped_data.__array__()
    
    def time_update(self):
        while True:
            yield self.env.timeout(self.time_interval)

            if self.now_time >= ((self.vehlcie_list_data.size / len(self.vehlcie_list_data)) - 1):
                self.now_time = 0
            else:
                self.now_time += 1
            logging.info("{:6.2f} - Time: {:2}, Time is changed.".format(self.env.now, self.now_time))
            
    def vehicle_spawn_time(self, direction):
        return abs(random.gauss(self.vehlcie_list_data[direction][self.now_time], self.gauss_standard_deviation))
    
    def ped_spawn_time(self, direction):
        return abs(random.gauss(self.ped_list_data[direction][self.now_time], self.gauss_standard_deviation))
    
    def get_last_time(self):
        return self.vehlcie_list_data.size / len(self.vehlcie_list_data)
    
    def get_now_time(self):
        return self.now_time