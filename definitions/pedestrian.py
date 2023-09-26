import logging
import math

class Pedestrian:
    def __init__(self, env, ped_id, start_point, end_point, update_interval) -> None:
        self.env = env

        self.ped_id = ped_id
        self.start_point = start_point
        self.end_point = end_point
        self.update_interval = update_interval

        self.isUpdateDiscomport = True
        self.isProcess = True
        self.spawned_time = env.now
        self.discomfort_value = 0

        self.action = env.process(self.run())
        
    def run(self):
        logging.debug("{:6.2f} - Spawn Pedestrian. Pedestrian ID: {}, Start Direction: {}, Target Direction: {}".format(self.env.now, self.ped_id, self.start_point, self.end_point))
        self.env.process(self.update_discomfort_value())
        yield self.env.timeout(0)

    def update_discomfort_value(self):
        while self.isUpdateDiscomport:
            self.discomfort_value = math.pow(self.env.now - self.spawned_time, 2)
            # logging.debug("{:6.2f} - Pedestrian {}'s discomfort value has updated. Discomport Value is {}".format(self.env.now, self.ped_id, self.discomfort_value))
            yield self.env.timeout(self.update_interval)

    def move(self):
        logging.debug("{:6.2f} - Pedestrian is Moving. Ped ID: {}, Start Direction: {}, Target Direction: {}".format(self.env.now, self.ped_id, self.start_point, self.end_point))
        self.isProcess = False
        self.isUpdateDiscomport = False