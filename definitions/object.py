import logging
import math

class Object:
    def __init__(self, env, conf, objectID, startDirection, targetDirection) -> None:
        self.env = env
        self.conf = conf

        self.objectID = objectID
        self.startDirection = startDirection
        self.targetDirection = targetDirection

        self.discomfortValue = 0.0
        self.spawnedTime = env.now

        self.bIsRelease = False

        logging.debug("{:6.2f} - Spawn Object. ID: {}, Start Direction: {}, Target Direction: {}".format(self.env.now, self.objectID, self.startDirection, self.targetDirection))
        env.process(self.update_discomfort_value())

    def update_discomfort_value(self):
        while not self.bIsRelease:
            self.discomfortValue = math.pow(self.env.now - self.spawnedTime, self.conf.discomfortRange)
            logging.debug("{:6.2f} - ID: {:2}, Discomfort: {:.2f}".format(self.env.now, self.objectID, self.discomfortValue))
            yield self.env.timeout(self.conf.discomfortInterval)
    def release(self):
        logging.debug("{:6.2f} - Release Object. ID: {}, Start Direction: {}, Target Direction: {}".format(self.env.now, self.objectID, self.startDirection, self.targetDirection))
        self.bIsRelease = True