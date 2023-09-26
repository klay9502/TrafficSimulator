import logging
import numpy as np

from algorithms.basic_q import BasicQ

class TrafficLightManager:
    def __init__(self, env, pattern, learning_type, intersection_type, time_of_green_signal, q_alpha, q_gamma, weight) -> None:
        self.env = env
        self.pattern = pattern
        self.learning_type = learning_type
        self.intersection_type = intersection_type
        self.time_of_green_signal = time_of_green_signal
        
        self.q_alpha = q_alpha
        self.q_gamma = q_gamma

        self.weight = weight

        self.now_signal = np.random.randint(0, self.intersection_type)
        logging.info("trafficlight_manager:Operate traffic system. Start signal is {}".format(self.now_signal))

        self.algorithm = BasicQ(self.env, self.intersection_type, self.pattern.get_last_time())

        self.isSignalChanged = False

        self.action = env.process(self.set_traffic_signal())

    def set_traffic_signal(self):
        while True:
            yield self.env.timeout(self.time_of_green_signal)

            if self.learning_type == "random":
                self.now_signal = np.random.randint(0, self.intersection_type)
            if self.learning_type == "clockwise":
                if self.now_signal >= self.intersection_type - 1:
                    self.now_signal = 0
                else:
                    self.now_signal += 1
            if self.learning_type == "basic_q":
                self.algorithm.update_table(self.pattern.get_now_time(), self.now_signal, self.q_alpha, self.q_gamma)
                self.algorithm.update_max_discomfort_zone(self.weight)
                self.now_signal = self.algorithm.get_min_signal(self.pattern.get_now_time())
            
            self.set_is_signal_changed(True)
            logging.info("{:6.2f} - Time: {:2}, Signal is changed. Now Signal is {}".format(self.env.now, self.pattern.get_now_time(), self.now_signal))

    def set_now_discomfort_value(self, now_vehicle_discomfort_value, now_ped_discomfort_value):
        self.algorithm.set_now_vehicle_discomfort_value(now_vehicle_discomfort_value)
        self.algorithm.set_now_ped_discomfort_value(now_ped_discomfort_value)

    def get_traffic_signal(self):
        return self.now_signal

    def get_is_signal_changed(self):
        return self.isSignalChanged
    
    def set_is_signal_changed(self, boolean):
        self.isSignalChanged = boolean