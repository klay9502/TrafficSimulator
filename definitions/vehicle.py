import logging
import math


class Vehicle:
    def __init__(self, env, vehicle_id, start_point, end_point, update_interval, vehicle_speed) -> None:
        self.env = env

        self.vehicle_id = vehicle_id
        self.start_point = start_point
        self.end_point = end_point
        self.update_interval = update_interval
        self.vehicle_speed = vehicle_speed
        
        self.isUpdateDiscomport = True
        self.isProcess = True
        self.spawned_time = env.now
        self.discomfort_value = 0

        self.action = env.process(self.run())

    def run(self):
        logging.debug("{:6.2f} - Spawn Vehicle. Vehicle ID: {}, Start Direction-Lane: {}-{}, Target Direction: {}".format(self.env.now, self.vehicle_id, self.start_point, self.end_point, self.end_point))
        self.env.process(self.update_discomfort_value())
        yield self.env.timeout(0)

    def update_discomfort_value(self):
        while self.isUpdateDiscomport:
            self.discomfort_value = math.pow(self.env.now - self.spawned_time, 2)
            # logging.debug("Time: {} - ID: {}, Spawned Time: {}, Discomport Value: {}".format(self.env.now, self.vehicle_id, self.spawned_time, self.discomfort_value))
            yield self.env.timeout(self.update_interval)

    def drive(self):
        logging.debug("{:6.2f} - Vehicle is Moving. Vehicle ID: {}, Start Direction-Lane: {}-{}, Target Direction: {}".format(self.env.now, self.vehicle_id, self.start_point, self.end_point, self.end_point))
        self.isProcess = False
        yield self.env.timeout(self.vehicle_speed)
        self.isUpdateDiscomport = False