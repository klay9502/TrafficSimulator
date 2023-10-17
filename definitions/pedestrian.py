import logging
import math

from definitions.object import Object

class Pedestrian(Object):
    def __init__(self, env, conf, objectID, direction) -> None:
        super().__init__(env, conf, objectID)

        self.direction = direction

        logging.debug("{:6.2f} - Spawn Pedestrian. ID: {}, Direction: {}, ".format(self.env.now, self.objectID, self.direction))
        env.process(self.update_discomfort_value())

    def update_discomfort_value(self):
        while not self.bIsRelease:
            self.discomfortValue = math.pow(self.env.now - self.spawnedTime, self.conf.discomfortRange)
            logging.debug("{:6.2f} - Update Pedestrian ID: {:2}, Discomfort: {:.2f}".format(self.env.now, self.objectID, self.discomfortValue))
            yield self.env.timeout(self.conf.discomfortInterval)
    def release(self):
        logging.debug("{:6.2f} - Release Pedestrian. ID: {}, Direction: {}".format(self.env.now, self.objectID, self.direction))
        self.bIsRelease = True