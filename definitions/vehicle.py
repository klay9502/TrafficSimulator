import logging
import math

from definitions.object import Object


class Vehicle(Object):
    def __init__(self, env, conf, objectID, startDirection, targetDirection) -> None:
        super().__init__(env, conf, objectID)

        self.startDirection = startDirection
        self.targetDirection = targetDirection

        logging.debug("{:6.2f} - Spawn Vehicle. ID: {}, Start Direction: {}, Target Direction: {}".format(self.env.now, self.objectID, self.startDirection, self.targetDirection))
        env.process(self.update_discomfort_value())

    def update_discomfort_value(self):
        while not self.bIsRelease:
            self.discomfortValue = math.pow(self.env.now - self.spawnedTime, self.conf.discomfortRange)
            logging.debug("{:6.2f} - Update Vehicle ID: {:2}, Discomfort: {:.2f}".format(self.env.now, self.objectID, self.discomfortValue))
            yield self.env.timeout(self.conf.discomfortInterval)
    def release(self):
        logging.debug("{:6.2f} - Release Vehicle. ID: {}, Start Direction: {}, Target Direction: {}".format(self.env.now, self.objectID, self.startDirection, self.targetDirection))
        self.bIsRelease = True