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
        self.now_total_discomfort_value = np.zeros(intersection_type)
        self.now_vehicle_discomfort_value = np.zeros(intersection_type)
        self.now_ped_discomfort_value = np.zeros(intersection_type)

        self.isIntervalRecord = False
        self.list_vehicle_discomfort_value = np.empty((0, intersection_type))
        self.list_ped_discomfort_value = np.empty((0, intersection_type))

        self.list_avg_vehicle_discomfort_value = []
        self.list_avg_ped_discomfort_value = []
        self.list_avg_total_discomfort_value = []

        self.action = env.process(self.run())

    def run(self):
        self.env.process(self.record_discomfort_counter())
        yield self.env.timeout(0)

    def update_now_discomfort_value(self, vehicle_queue, ped_queue, weight):
        for inter in range(self.intersection_type):
            for lane in range(len(vehicle_queue[inter])):
                for vi in vehicle_queue[inter][lane]:
                    self.now_vehicle_discomfort_value[inter] += vi.discomfort_value * weight
                    self.now_total_discomfort_value[inter] += vi.discomfort_value * weight

        for inter in range(self.intersection_type):
            for ped in ped_queue[inter]:
                self.now_ped_discomfort_value[inter] += ped.discomfort_value * (1 - weight)
                self.now_total_discomfort_value[inter] += ped.discomfort_value * (1 - weight)
        
        if self.isIntervalRecord == True:
            self.list_vehicle_discomfort_value = np.concatenate([self.list_vehicle_discomfort_value, [self.now_vehicle_discomfort_value]])
            self.list_ped_discomfort_value = np.concatenate([self.list_ped_discomfort_value, [self.now_ped_discomfort_value]])
            
            self.list_avg_vehicle_discomfort_value.append(np.average(self.now_vehicle_discomfort_value))
            self.list_avg_ped_discomfort_value.append(np.average(self.now_ped_discomfort_value))
            self.list_avg_total_discomfort_value.append(np.average(self.now_total_discomfort_value))

            logging.debug("{:6.2f} - Pedestrian Discomfort Values: {}".format(self.env.now, self.now_ped_discomfort_value))
            logging.debug("{:6.2f} - Vehicle Discomfort Values: {}".format(self.env.now, self.now_vehicle_discomfort_value))
            
            self.isIntervalRecord = False

    def get_now_total_discomfort_value(self):
        return self.now_total_discomfort_value

    def get_now_vehicle_discomfort_value(self):
        return self.now_vehicle_discomfort_value
    
    def get_now_ped_discomfort_value(self):
        return self.now_ped_discomfort_value

    def reset_now_discomfort_value(self):
        self.now_total_discomfort_value = np.zeros(self.intersection_type)
        self.now_vehicle_discomfort_value = np.zeros(self.intersection_type)
        self.now_ped_discomfort_value = np.zeros(self.intersection_type)

    def record_discomfort_counter(self):
        while True:
            if self.isIntervalRecord == False:
                self. isIntervalRecord = True
                
            yield self.env.timeout(self.plt_discomfort_value_record_interval)

    def print_plot(self):
        self.list_avg_vehicle_discomfort_value = np.array(self.list_avg_vehicle_discomfort_value)
        self.list_avg_ped_discomfort_value = np.array(self.list_avg_ped_discomfort_value)
        self.list_avg_total_discomfort_value = np.array(self.list_avg_total_discomfort_value)

        if (self.plt_moving_average):
            self.list_avg_vehicle_discomfort_value = self.moving_average(self.list_avg_vehicle_discomfort_value, self.plt_moving_average_window)
            self.list_avg_ped_discomfort_value = self.moving_average(self.list_avg_ped_discomfort_value, self.plt_moving_average_window)
            self.list_avg_total_discomfort_value = self.moving_average(self.list_avg_total_discomfort_value, self.plt_moving_average_window)

        intersection_labels = []
        direction_labels = []

        for i in range(self.intersection_type):
            intersection_labels.append("Load " + str(i))
            direction_labels.append("Direction" + str(i))

        plt.subplot(131)
        plt.title("Average Discomfort Value")
        plt.xlabel("Sec")
        plt.ylabel("Average Discomport Value")
        plt.plot(self.list_avg_total_discomfort_value, label="Total")
        plt.plot(self.list_avg_vehicle_discomfort_value, label="Vehicle")
        plt.plot(self.list_avg_ped_discomfort_value, label="Pedestrian")
        plt.legend()

        plt.subplot(132)
        plt.plot(self.list_vehicle_discomfort_value, label=intersection_labels)
        plt.title("Discomfort Value by lanes")
        plt.xlabel("Sec")
        plt.ylabel("Discomport Value")
        plt.legend()

        plt.subplot(133)
        plt.plot(self.list_ped_discomfort_value, label=direction_labels)
        plt.title("Discomfort Value by Pedestrian Direction")
        plt.xlabel("Sec")
        plt.ylabel("Discomport Value")
        plt.legend()

        plt.show()

    def moving_average(self, x, w):
        return np.convolve(x, np.ones(w), 'valid') / w