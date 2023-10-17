import logging
import numpy as np

from algorithms.basicQ import BasicQ

class TrafficManager:
    def __init__(self, env, conf, pattern, vm, pm) -> None:
        self.env = env
        self.conf = conf
        
        self.pattern = pattern
        self.vm = vm
        self.pm = pm

        self.algorithm = None

        self.nowSignal = np.random.randint(0, self.conf.intersectionType)
        logging.info("TrafficManager:init() - Operate traffic system. Start signal is {}".format(self.nowSignal))
        logging.info("TrafficManager:init() - Learning type is {}".format(self.conf.learningType))

        env.process(self.set_traffic_signal())

    def set_traffic_signal(self):
        if self.conf.learningType == "BASIC_Q":
            self.algorithm = BasicQ(self.env, self.conf, self.pattern)

        while True:
            yield self.env.timeout(self.conf.signalInterval)

            if self.conf.learningType == "RANDOM":
                self.nowSignal = np.random.randint(0, self.conf.intersectionType)
            if self.conf.learningType == "CLOCKWISE":
                if self.nowSignal >= self.conf.intersectionType - 1:
                    self.nowSignal = 0
                else:
                    self.nowSignal += 1
            if self.conf.learningType == "BASIC_Q":
                self.algorithm.update_table(self.pattern.nowTime, self.nowSignal, self.total_discomfort_value())

                # epsilon-greedy policy
                if np.random.rand() < self.conf.epsilon:
                    self.nowSignal = np.random.randint(0, self.conf.intersectionType)
                else:
                    self.nowSignal = self.algorithm.get_action(self.pattern.nowTime, self.total_discomfort_value())

            logging.info("{:6.2f} - Time: {:2}, Signal is changed. Now Signal is {}".format(self.env.now, self.pattern.nowTime, self.nowSignal))
            self.vm.update_vehicle_queue(self.nowSignal)
            self.pm.update_pedestrian_queue(self.nowSignal)

    def total_discomfort_value(self):
        return list(self.conf.weight * np.array(self.vm.get_now_discomfort_value()) + \
                    (1 - self.conf.weight) * np.array(self.pm.get_now_discomfort_value()))