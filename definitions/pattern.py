import logging
import random
import pandas as pd
import numpy as np

class Pattern:
    def __init__(self, env, conf):
        self.env = env
        self.conf= conf

        self.nowTime = 0
        self.oldTime = 0

        self.vehicleDataList = np.empty((0, 0))
        self.pedDataList = np.empty((0, 0))

        self.read_file()
        env.process(self.update_time())

    def read_file(self):
        vehicleData = pd.read_csv(self.conf.vehiclePatternFilePath)
        pedData = pd.read_csv(self.conf.pedPatternFilePath)
        
        self.vehicleDataList = vehicleData.__array__()
        self.pedDataList = pedData.__array__()

        # if (self.vehicleDataList.size / len(self.vehicleDataList)) != self.conf.numberOfLanes:
        #     logging.error("Pattern:read_file() - The number of columns in the csv file differs from the intersection parameter.")
        #     raise
    
    def update_time(self):
        while True:
            yield self.env.timeout(self.conf.timeInterval)

            if self.nowTime >= int((self.vehicleDataList.size / len(self.vehicleDataList)) - 1):
                self.nowTime = 0
            else:
                self.nowTime += 1
            
            logging.info("{:6.2f} - Time: {:2}, Time is changed.".format(self.env.now, self.nowTime))

    def vehicle_spawn_time(self, direction):
        return abs(random.gauss(self.vehicleDataList[direction][self.nowTime], self.conf.gauseStandardDeviation))
    
    def pedestrian_spawn_time(self, direction):
        return abs(random.gauss(self.pedDataList[direction][self.nowTime], self.conf.gauseStandardDeviation))