import numpy as np

class BasicQ:
    def __init__(self, env, intersection_type, last_time) -> None:
        self.env = env
        self.intersection_type = int(intersection_type)
        self.last_time = int(last_time)

        # q_table[<times>][<now signal direction>][<values>]
        self.q_table = np.zeros((self.last_time, self.intersection_type, self.intersection_type))

        self.now_vehicle_discomfort_value = []
        self.now_ped_discomfort_value = []
        self.now_total_discomfort_value = []
        self.now_max_discomfort_zone = 0

    def update_table(self, now_time, now_signal, alpha, gamma):
        sum_discomfort_value = np.sum(self.now_total_discomfort_value)
        self.q_table[now_time][self.now_max_discomfort_zone][now_signal] = \
            (1 - alpha) * self.q_table[now_time][self.now_max_discomfort_zone][now_signal] + \
            alpha * (sum_discomfort_value + (gamma * np.min(self.q_table[now_time][self.now_max_discomfort_zone])))

    def set_now_vehicle_discomfort_value(self, now_vehlcie_discomfort_value):
        self.now_vehicle_discomfort_value = now_vehlcie_discomfort_value

    def set_now_ped_discomfort_value(self, now_ped_discomfort_value):
        self.now_ped_discomfort_value = now_ped_discomfort_value

    def update_max_discomfort_zone(self, weight):
        self.now_vehicle_discomfort_value = self.now_vehicle_discomfort_value * weight
        self.now_ped_discomfort_value = self.now_ped_discomfort_value * (1 - weight)
        self.now_total_discomfort_value = np.array(self.now_vehicle_discomfort_value) + np.array(self.now_ped_discomfort_value)
        self.now_max_discomfort_zone = np.argmax(self.now_total_discomfort_value)

    def get_min_signal(self, now_time):
        return np.argmin(self.q_table[now_time][self.now_max_discomfort_zone])