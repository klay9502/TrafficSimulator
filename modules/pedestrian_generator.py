import logging
import random

from definitions.pedestrian import Pedestrian

class PedestrianGenerator:
    def __init__(self, env, pattern, intersection_type, discomfort_value_update_interval) -> None:
        self.env = env
        self.pattern = pattern
        self.ped_id = 0
        self.intersection_type = intersection_type
        self.discomfort_value_update_interval = discomfort_value_update_interval

        # ped_queue[<end_point>][<pedestrain>]
        self.ped_queue = [[] for i in range(intersection_type)]

        self.action = [env.process(self.pedestrian_generate(i)) for i in range(intersection_type)]

    def pedestrian_generate(self, direction):
        logging.info("pedestrian_generate:Pedestrians will spawn indifinitely.")
        yield self.env.timeout(0)
        while True:
            random_list = [direction - 1, direction + 1]
            for i in range(len(random_list)):
                if random_list[i] < 0:
                    random_list[i] = self.intersection_type - 1
                elif random_list[i] >= self.intersection_type:
                    random_list[i] = 0
            # point_list = [<start_point>, <end_point>]
            point_list = [0, direction]
            point_list[0] = random.choice(random_list)
            pedestrian = Pedestrian(self.env, self.ped_id, point_list[0], point_list[1], self.discomfort_value_update_interval)
            self.append_ped_queue(pedestrian)
            self.ped_id += 1
            yield self.env.timeout(self.pattern.ped_spawn_time(direction))

    def get_ped_queue(self) -> list:
        return self.ped_queue

    def append_ped_queue(self, pedestrian):
        self.ped_queue[pedestrian.end_point].append(pedestrian)

    def update_ped_queue(self):
        for inter in range(self.intersection_type):
            self.ped_queue[inter][:] = [value for value in self.ped_queue[inter] if value.isProcess != False]
        
        # print(len(self.ped_queue[0]), len(self.ped_queue[1]), len(self.ped_queue[2]), len(self.ped_queue[3]))

    def update_ped_state(self, traffic_signal):
        # 보행자 신호는 차량 신호에 종속적이기 때문에 별도의 처리가 필요
        # 대한민국 교통체계를 기준으로 우측통행 신호가 없다고 가정.
        # intersection position은 시계방향 순으로 정렬.

        # 우측 신호
        move_position = traffic_signal - 1
        if move_position < 0:
            move_position = self.intersection_type - 1
        elif move_position >= self.intersection_type:
            move_position = 0

        for ped in self.ped_queue[move_position]:
            ped.move()

        # for ped in range(len(self.ped_queue[traffic_signal])):
        #     if self.ped_queue[traffic_signal][ped].end_point == move_position:
        #         self.ped_queue[traffic_signal][ped].move()

        # for ped in range(len(self.ped_queue[move_position])):
        #     if self.ped_queue[move_position][ped].end_point == traffic_signal:
        #         self.ped_queue[move_position][ped].move()