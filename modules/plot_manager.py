import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

class PlotManager:
    def __init__(self, env, conf, vm) -> None:
        self.env = env
        self.conf = conf
        self.vm = vm

        self.listVehicleDiscomfortValue = np.empty((0, conf.intersectionType))

        self.listSumTotalDiscomfortValue = []
        self.listAverageTotalDiscomfortValue = []
    
        env.process(self.record())

    def record(self):
        while True:
            self.listVehicleDiscomfortValue = np.concatenate([self.listVehicleDiscomfortValue, [self.vm.get_now_discomfort_value()]])

            self.listSumTotalDiscomfortValue.append(np.sum(self.vm.get_now_discomfort_value()))
            self.listAverageTotalDiscomfortValue.append(np.average(self.vm.get_now_discomfort_value()))

            yield self.env.timeout(self.conf.signalInterval)

    def print_plot(self):

        intersectionLabels = []

        for i in range(self.conf.intersectionType):
            intersectionLabels.append("Load " + str(i))

        plt.subplot(131)
        plt.title("Total Discomfort Value")
        plt.xlabel("Signal")
        plt.ylabel("Discomport Value")
        plt.plot(self.listSumTotalDiscomfortValue, label="Sum")
        plt.plot(self.listAverageTotalDiscomfortValue, label="Average")
        plt.legend()

        plt.subplot(132)
        plt.title("Total Discomfort Value (Moving Average)")
        plt.xlabel("Signal")
        plt.ylabel("Discomport Value")
        plt.plot(self.moving_average(self.listSumTotalDiscomfortValue, int(self.conf.simulateTime / 10)), label="Sum")
        plt.plot(self.moving_average(self.listAverageTotalDiscomfortValue, int(self.conf.simulateTime / 10)), label="Average")
        plt.legend()

        plt.subplot(133)
        plt.plot(self.listVehicleDiscomfortValue, label=intersectionLabels)
        plt.title("Discomfort Value by lanes")
        plt.xlabel("Signal")
        plt.ylabel("Discomport Value")
        plt.legend()

        plt.show()

    def moving_average(self, x, w):
        return np.convolve(x, np.ones(w), 'valid') / w