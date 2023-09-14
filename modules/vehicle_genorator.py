import logging
import numpy as np
from collections import deque

from definitions.vehicle import Vehicle

class VehicleGenorator:
    def __init__(self, env, spawn_interval, number, intersection_type, number_of_lanes, discomfort_value_update_interval, vehicle_speed, time_of_green_signal, infinity) -> None:

        self.env = env
        self.spawn_interval = spawn_interval
        self.number = number
        self.intersection_type = intersection_type
        self.number_of_lanes = number_of_lanes
        self.discomfort_value_update_interval = discomfort_value_update_interval
        self.vehicle_speed = vehicle_speed
        self.time_of_green_signal = time_of_green_signal
        self.infinity = infinity

        # vehicle_queue[<intersection_position>][<lane_position>][<vehicle>]
        self.vehicle_queue = [[deque() for j in range(number_of_lanes)] for i in range(intersection_type)]

        self.action = env.process(self.vehicle_genorate())

    def vehicle_genorate(self) -> None:
        if (self.infinity):
            logging.info("vehicle_genorate:Vehicles will spawn indifinitely.")
            while(True):
                logging.info("{}, Spawn Vehicle!".format(self.env.now))
                yield self.env.timeout(self.spawn_interval)
        else:
            logging.info("vehicle_genorate:Vehicles will spawn only {} unit.".format(self.number))
            for i in range(self.number):
                # point_list = [<start_point>, <end_point>]
                point_list = np.random.choice(range(0, self.intersection_type), 2, replace=False)
                vehicle = Vehicle(self.env, i, point_list[0], point_list[1], self.discomfort_value_update_interval, self.vehicle_speed)
                self.append_vehicle_queue(vehicle)
                yield self.env.timeout(self.spawn_interval)
    
    def get_vehicle_queue(self) -> list:
        return self.vehicle_queue

    def append_vehicle_queue(self, vehicle):
        self.vehicle_queue[vehicle.start_point][vehicle.end_point].append(vehicle)

    def update_vehicle_queue(self):
        for inter in range(self.intersection_type):
            for lane in range(self.number_of_lanes):
                for vi in range(len(self.vehicle_queue[inter][lane])):
                    if self.vehicle_queue[inter][lane][vi].isProcess == False:
                        self.vehicle_queue[inter][lane].popleft()
                        break

    def update_vehlcies_state(self, traffic_signal):
        for lane in range(self.number_of_lanes):
            for vi in range(len(self.vehicle_queue[traffic_signal][lane])):
                if vi * self.vehicle_speed < self.time_of_green_signal:
                    self.env.process(self.vehicle_queue[traffic_signal][lane][vi].drive())
                else:
                    break