import os
import argparse
import logging
import simpy
from definitions.pattern import Pattern

from modules.configuration import Configuration
from modules.pedestrian_generator import PedestrianGenerator
from modules.plot_manager import PlotManager
from modules.traffic_manager import TrafficManager
from modules.vehicle_generator import VehicleGenerator

class Simulator:
    def __init__(self, conf) -> None:
        self.conf = conf

        self.module_init()

    def module_init(self) -> None:
        env = simpy.Environment()

        pattern = Pattern(env, self.conf)

        vehicleGenerator = VehicleGenerator(env, self.conf, pattern)
        pedestrianGenerator = PedestrianGenerator(env, self.conf, pattern)

        trafficManager = TrafficManager(env, self.conf, pattern, vehicleGenerator, pedestrianGenerator)

        plotManager = PlotManager(env, self.conf, vehicleGenerator, pedestrianGenerator)

        env.process(self.env_update(env))
        env.run(until=self.conf.simulateTime)

        plotManager.print_plot()

    def env_update(self, env) -> None:
        while True:
            yield env.timeout(self.conf.simulateInterval)

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", required=True, metavar="<configuration file>", help="Configuration File", type=str)
    parser.add_argument("-l", "--log", metavar="<log level (DEBUG/INFO/WARNING/ERROR)>", help="Log Level (DEBUG/INFO/WARNING/ERROR)", type=str, default="INFO")
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)
    Simulator(Configuration(args.conf))

if __name__ == "__main__":
    main()