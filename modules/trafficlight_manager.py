import logging
import numpy as np

class TrafficLightManager:
    def __init__(self, env, learning_type, intersection_type, time_of_green_signal) -> None:
        self.env = env
        self.learning_type = learning_type
        self.intersection_type = intersection_type
        self.time_of_green_signal = time_of_green_signal

        self.now_signal = np.random.randint(0, self.intersection_type)
        logging.info("trafficlight_manager:Operate traffic system. Start signal is {}".format(self.now_signal))
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

            self.set_is_signal_changed(True)
            logging.info("Time: {} - Now Signal: {}".format(self.env.now, self.now_signal))

    def get_traffic_signal(self):
        return self.now_signal

    def get_is_signal_changed(self):
        return self.isSignalChanged
    
    def set_is_signal_changed(self, boolean):
        self.isSignalChanged = boolean