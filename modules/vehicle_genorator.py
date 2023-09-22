import logging
import random
import numpy as np
from collections import deque

from definitions.vehicle import Vehicle

class VehicleGenorator:
    def __init__(self, env, pattern, number, intersection_type, number_of_lanes, discomfort_value_update_interval, vehicle_speed, time_of_green_signal, infinity) -> None:

        self.env = env
        self.pattern = pattern
        self.number = number
        self.intersection_type = intersection_type
        self.number_of_lanes = number_of_lanes
        self.discomfort_value_update_interval = discomfort_value_update_interval
        self.vehicle_speed = vehicle_speed
        self.time_of_green_signal = time_of_green_signal
        self.infinity = infinity

        # vehicle_queue[<intersection_position>][<lane_position>][<vehicle>]
        self.vehicle_queue = [[deque() for j in range(number_of_lanes)] for i in range(intersection_type)]

        self.action = [env.process(self.vehicle_genorate(i)) for i in range(intersection_type)]

    def vehicle_genorate(self, direction) -> None:
        if (self.infinity):
            logging.info("vehicle_genorate:Vehicles will spawn indifinitely.")
            logging.info("It's not finished yet.")
            while(True):
                logging.info("{}, Spawn Vehicle!".format(self.env.now))
                yield self.env.timeout(self.spawn_interval)
        else:
            logging.info("vehicle_genorate:Vehicles will spawn only {} unit.".format(self.number))
            for i in range(self.number):
                random_list = []
                for j in range(self.intersection_type):
                    if j == direction:
                        continue
                    else:
                        random_list.append(j)
                # point_list = [<start_point>, <end_point>]
                point_list = [direction, 0]
                point_list[1] = random.choice(random_list)
                vehicle = Vehicle(self.env, i, point_list[0], point_list[1], self.discomfort_value_update_interval, self.vehicle_speed)
                self.append_vehicle_queue(vehicle)
                yield self.env.timeout(self.pattern.vehicle_spawn_time(direction))
    
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