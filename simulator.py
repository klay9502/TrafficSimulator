import os
import argparse
import logging
import simpy
from definitions.pattern import Pattern
from modules.trafficlight_manager import TrafficLightManager
from modules.vehicle_genorator import VehicleGenorator
from modules.plot_manager import PlotManager

class Simulator:
    def __init__(self, conf) -> None:
        self.conf = conf
        self.simulate_time = 0.0
        self.simulate_interval = 0.0
        self.pattern_file_path = ""
        self.learning_type = ""

        self.intersection_type = 0
        self.number_of_lanes = 0

        self.time_of_green_signal = 0

        self.vehicle_spawn_infinity = True
        self.vehicnumber_of_vehicle = 0
        self.discomfort_value_update_interval = 0
        self.vehicle_spawn_interval = 0.0
        self.vehicle_speed = 0.0

        self.plt_discomfort_value_record_interval = 0.0

        self.parse_config()
        self.run()

    def parse_config(self) -> None:
        with open(self.conf, "r") as file:
            for line in file:
                try:
                    line = line.strip()
                    if line.startswith("#"):
                        # Exception the Comment Line.
                        continue
                    if line == "":
                        continue

                    key, val = line.split("=")
                    key = key.strip()
                    val = val.strip()
                    if key == "simulate_time":
                        self.simulate_time = float(val)
                    if key == "simulate_interval":
                        self.simulate_interval = float(val)
                    if key == "pattern_file_name":
                        path = os.getcwd()
                        file_name = os.path.join(path, val)
                        if os.path.exists(file_name):
                            self.pattern_file_path = file_name
                        else:
                            logging.error("There are no file in {}".format(file_name))
                            break
                    if key == "learning_type":
                        self.learning_type = str(val)
                    if key == "intersection_type":
                        self.intersection_type = int(val)
                    if key == "number_of_lanes":
                        self.number_of_lanes = int(val)
                    if key == "time_of_green_signal":
                        self.time_of_green_signal = int(val)
                    if key == "vehicle_spawn_infinity":
                        if val == "True":
                            self.vehicle_spawn_infinity = True
                        else:
                            self.vehicle_spawn_infinity = False
                    if key == "number_of_vehicle":
                        self.number_of_vehicle = int(val)
                    if key == "discomfort_value_update_interval":
                        self.discomfort_value_update_interval = int(val)
                    if key == "vehicle_spawn_interval":
                        self.vehicle_spawn_interval = float(val)
                    if key == "vehicle_speed":
                        self.vehicle_speed = float(val)
                    if key == "plt_discomfort_value_record_interval":
                        self.plt_discomfort_value_record_interval = float(val)

                except:
                    logging.error("Error in parsing the line: {}".format(line))
                    continue

    def run(self) -> None:
        env = simpy.Environment()
        pattern = Pattern(self.pattern_file_path)
        trafficlight_manager = TrafficLightManager(env, self.learning_type, self.intersection_type, self.time_of_green_signal)
        vehicle_generator = VehicleGenorator(env,
                                            self.vehicle_spawn_interval,
                                            self.number_of_vehicle,
                                            self.intersection_type,
                                            self.number_of_lanes,
                                            self.discomfort_value_update_interval,
                                            self.vehicle_speed,
                                            self.time_of_green_signal,
                                            self.vehicle_spawn_infinity)
        plot_manager = PlotManager(env,
                                   self.intersection_type,
                                   self.plt_discomfort_value_record_interval)
        
        env.process(self.update(env, trafficlight_manager, vehicle_generator, plot_manager))
        env.run(until=self.simulate_time)

        # plot_manager.print_plot()

    def update(self, env, trafficlight_manager, vehicle_generator, plot_manager) -> None:
        while True:
            if trafficlight_manager.get_is_signal_changed():
                vehicle_generator.update_vehlcies_state(trafficlight_manager.get_traffic_signal())
                trafficlight_manager.set_is_signal_changed(False)

            vehicle_generator.update_vehicle_queue()

            plot_manager.update_now_discomfort_value(vehicle_generator.get_vehicle_queue())
            plot_manager.reset_now_discomfort_value()

            yield env.timeout(self.simulate_interval)

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", required=True, metavar="<configuration file>", help="Configuration File", type=str)
    parser.add_argument("-l", "--log", metavar="<log level (DEBUG/INFO/WARNING/ERROR)>", help="Log Level (DEBUG/INFO/WARNING/ERROR)", type=str, default="DEBUG")
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)
    simulator = Simulator(args.conf)

if __name__ == "__main__":
    main()