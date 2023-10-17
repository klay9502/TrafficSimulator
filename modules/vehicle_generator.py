import logging
import random
import math
import numpy as np
from collections import deque

from definitions.vehicle import Vehicle
from modules.object_generator import ObjectGenerator

class VehicleGenerator(ObjectGenerator):
    def __init__(self, env, conf, pattern) -> None:
        super().__init__(env, conf, pattern)

        self.vehicleQueue = [[deque() for j in range(conf.numberOfLanes)] for i in range(conf.intersectionType)]
        
        for i in range(self.conf.intersectionType):
            env.process(self.generate(i))
        
    def generate(self, direction) -> None:
        logging.info("VehicleGenerator:generate() - Vehicles will spawn indifinitely.")
        while True:
            # randomList = []
            # for i in range(self.conf.intersectionType):
            #     if i == direction:
            #         continue
            #     else:
            #         randomList.append(i)
            directionList = [direction, 0]
            directionList[1] = (direction + random.choice(range(1, self.conf.intersectionType))) % self.conf.intersectionType


            vehicle = Vehicle(self.env,
                              self.conf,
                              self.idCounter,
                              directionList[0],
                              directionList[1])
            self.vehicleQueue[vehicle.startDirection][vehicle.targetDirection].append(vehicle)
            self.idCounter += 1
            yield self.env.timeout(self.pattern.vehicle_spawn_time(direction))

    def update_vehicle_queue(self, signal):
        for lane in range(self.conf.numberOfLanes):
            for vi in range(math.floor(self.conf.signalInterval / self.conf.vehicleSpeed)):
                if len(self.vehicleQueue[signal][lane]) == 0:
                    break
                self.vehicleQueue[signal][lane][0].release()
                self.vehicleQueue[signal][lane].popleft()

    def get_now_discomfort_value(self):
        direction = np.zeros(self.conf.intersectionType)

        for inter in range(self.conf.intersectionType):
            for lane in range(self.conf.numberOfLanes):
                for vi in self.vehicleQueue[inter][lane]:
                    direction[inter] += vi.discomfortValue
        
        return direction
    
