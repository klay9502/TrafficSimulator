import logging
import numpy as np
import matplotlib.pyplot as plt

class PlotManager:
    def __init__(self, env, intersection_type, plt_moving_average, plt_moving_average_window, plt_discomfort_value_record_interval) -> None:
        self.env = env
        self.intersection_type = intersection_type
        self.plt_moving_average = plt_moving_average
        self.plt_moving_average_window = plt_moving_average_window
        self.plt_discomfort_value_record_interval = plt_discomfort_value_record_interval

        # discomport_value_queue[<intersection]
        self.now_discomfort_value = np.zeros(intersection_type)

        self.isIntervalRecord = False
        self.list_discomfort_value = np.empty((0, intersection_type))
        self.list_avg_discomfort_value = []

        self.action = env.process(self.run())

    def run(self):
        self.env.process(self.record_discomfort_counter())
        yield self.env.timeout(0)

    def update_now_discomfort_value(self, vehicle_queue):
        for inter in range(self.intersection_type):
            for lane in range(len(vehicle_queue[inter])):
                for vi in vehicle_queue[inter][lane]:
                    self.now_discomfort_value[inter] += vi.discomfort_value
        
        if self.isIntervalRecord == True:
            self.list_discomfort_value = np.concatenate([self.list_discomfort_value, [self.now_discomfort_value]])
            self.list_avg_discomfort_value.append(np.average(self.now_discomfort_value))
            logging.debug("{:6.2f} - {}".format(self.env.now, self.now_discomfort_value))
            self.isIntervalRecord = False

    def get_now_discomfort_value(self):
        return self.now_discomfort_value

    def reset_now_discomfort_value(self):
        self.now_discomfort_value = np.zeros(self.intersection_type)

    def record_discomfort_counter(self):
        while True:
            if self.isIntervalRecord == False:
                self. isIntervalRecord = True
                
            yield self.env.timeout(self.plt_discomfort_value_record_interval)

    def print_plot(self):
        self.list_avg_discomfort_value = np.array(self.list_avg_discomfort_value)

        if (self.plt_moving_average):
            self.list_avg_discomfort_value = self.moving_average(self.list_avg_discomfort_value, self.plt_moving_average_window)

        intersection_labels = []

        for i in range(self.intersection_type):
            intersection_labels.append("Load " + str(i))

        plt.subplot(121)
        plt.title("Average Discomfort Value")
        plt.xlabel("Time")
        plt.ylabel("Average Discomport Value")
        plt.plot(self.list_avg_discomfort_value)

        plt.subplot(122)
        plt.plot(self.list_discomfort_value, label=intersection_labels)
        plt.title("Discomfort Value by lanes")
        plt.xlabel("Time")
        plt.ylabel("Discomport Value")
        plt.legend()

        plt.show()

    def moving_average(self, x, w):
        return np.convolve(x, np.ones(w), 'valid') / w