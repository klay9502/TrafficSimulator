import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

class PlotManager:
    def __init__(self, env, conf, vm, pm) -> None:
        self.env = env
        self.conf = conf
        self.vm = vm
        self.pm = pm

        self.listVehicleDiscomfortValue = np.empty((0, conf.intersectionType))
        self.listPedDiscomfortValue = np.empty((0, conf.intersectionType))

        self.listSumTotalDiscomfortValue = []
        self.listAverageTotalDiscomfortValue = []

        self.listSumVehicleDiscomfortValue = []
        self.listAverageVehicleDiscomfortValue = []

        self.listSumPedDiscomfortValue = []
        self.listAveragePedDiscomfortValue = []
    
        env.process(self.record())

    def record(self):
        while True:
            self.listVehicleDiscomfortValue = np.concatenate([self.listVehicleDiscomfortValue, [self.vm.get_now_discomfort_value()]])
            self.listPedDiscomfortValue = np.concatenate([self.listPedDiscomfortValue, [self.pm.get_now_discomfort_value()]])

            self.listSumTotalDiscomfortValue.append(np.sum(np.array(self.vm.get_now_discomfort_value() + \
                                                                    self.pm.get_now_discomfort_value())))
            self.listAverageTotalDiscomfortValue.append(np.average(np.array(self.vm.get_now_discomfort_value() + \
                                                                            self.pm.get_now_discomfort_value())))

            self.listSumVehicleDiscomfortValue.append(np.sum(self.vm.get_now_discomfort_value()))
            self.listAverageVehicleDiscomfortValue.append(np.sum(self.vm.get_now_discomfort_value()))

            self.listSumPedDiscomfortValue.append(np.sum(self.pm.get_now_discomfort_value()))
            self.listAveragePedDiscomfortValue.append(np.sum(self.pm.get_now_discomfort_value()))

            logging.debug("{:6.2f} - Record Values.".format(self.env.now))

            yield self.env.timeout(self.conf.pltDVRecordInterval)

    def print_plot(self):

        intersectionLabels = []
        directionLabels = []

        for i in range(self.conf.intersectionType):
            intersectionLabels.append("Load " + str(i))
            directionLabels.append("Direction" + str(i))

        plt.subplot(131)
        plt.title("Total Discomfort Value")
        plt.xlabel("Signal")
        plt.ylabel("Discomport Value")
        # plt.plot(self.listSumTotalDiscomfortValue, label="Sum")
        # plt.plot(self.listAverageTotalDiscomfortValue, label="Average")
        # plt.plot(self.read_file_compare_pattern("CLOCKWISE.csv"), label="Clockwise(Sum, Moving Average)")
        # plt.plot(self.moving_average(self.listSumTotalDiscomfortValue, int(self.conf.pltMovingAverageWindow)), label="Total(Sum, Moving Average)")
        plt.plot(self.moving_average(self.listSumVehicleDiscomfortValue, int(self.conf.pltMovingAverageWindow)), label="Vehicle(Sum, Moving Average)")
        plt.plot(self.moving_average(self.listSumPedDiscomfortValue, int(self.conf.pltMovingAverageWindow)), label="Pedestrian(Sum, Moving Average)")
        # plt.plot(self.moving_average(self.listAverageTotalDiscomfortValue, int(self.conf.simulateTime / 10)), label="Total(Average, Moving Average)")
        plt.legend()

        # temp = self.moving_average(self.listSumTotalDiscomfortValue, int(self.conf.pltMovingAverageWindow))
        # df = pd.DataFrame(temp, columns=["Clockwise"])
        # df_name = self.conf.learningType + ".csv"
        # self.save_file_csv(df_name, df)


        plt.subplot(132)
        plt.title("Discomfort Value by lanes")
        plt.xlabel("Signal")
        plt.ylabel("Discomport Value")
        plt.plot(self.listVehicleDiscomfortValue, label=intersectionLabels)
        plt.legend()

        plt.subplot(133)
        plt.title("Discomfort Value by Pedestrian Direction")
        plt.xlabel("Signal")
        plt.ylabel("Discomport Value")
        plt.plot(self.listPedDiscomfortValue, label=directionLabels)
        plt.legend()

        plt.show()

    def moving_average(self, x, w):
        return np.convolve(x, np.ones(w), 'valid') / w
    
    def save_file_csv(self, filename, df):
        path = "./outputs/" + filename
        df.to_csv(path)

    def read_file_compare_pattern(self, filename):
        path = "./outputs/" + filename
        df = pd.read_csv(path)
        return df.to_numpy()