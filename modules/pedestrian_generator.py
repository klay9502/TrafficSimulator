import logging
import numpy as np

from definitions.pedestrian import Pedestrian

class PedestrianGenerator:
    def __init__(self, env, conf, pattern) -> None:
        self.env = env
        self.conf = conf
        self.pattern = pattern

        self.idCounter = 0

        self.pedQueue = [[] for i in range(conf.intersectionType)]

        for i in range(self.conf.intersectionType):
            env.process(self.generate(i))

    def generate(self, direction):
        logging.info("PedestrianGenerator:generate() - Pedestrians will spawn indifinitely.")
        while True:
            # temp = list(range(self.conf.intersectionType))

            # directionList = [direction, 0]
            # directionList[1] = np.random.choice([temp[direction - 1], temp[direction + 1]])
            pedestrian = Pedestrian(self.env, self.conf, self.idCounter, direction)
            self.pedQueue[direction].append(pedestrian)
            yield self.env.timeout(self.pattern.pedestrian_spawn_time(direction))

    def update_pedestrian_queue(self, signal):
        for pi in self.pedQueue[signal]:
            pi.release()
        
        self.pedQueue[signal].clear()

    def get_now_discomfort_value(self):
        direction = np.zeros(self.conf.intersectionType)

        for inter in range(self.conf.intersectionType):
            for pi in self.pedQueue[inter]:
                direction[inter] += pi.discomfortValue

        return direction