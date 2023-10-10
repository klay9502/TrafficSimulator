import numpy as np

class BasicQ:
    def __init__(self, env, conf, pattern):
        self.env = env
        self.conf = conf
        self.pattern = pattern
        
        # qTable[<times>][<argmax discomfort value>][<now signal direction>]
        self.qTable = np.zeros((int(pattern.vehicleDataList.size / len(pattern.vehicleDataList)),
                                conf.intersectionType,
                                conf.intersectionType))
        
    def get_action(self, nowTime, DiscomfortValueList):
        argmax = np.random.choice(np.argwhere(DiscomfortValueList == np.amax(DiscomfortValueList)).flatten().tolist())
        # print("action is {} {}".format(nowTime, argmax))
        # print(np.argwhere(self.qTable[nowTime][argmax] == np.amin(self.qTable[nowTime][argmax])).flatten().tolist())
        return np.random.choice(np.argwhere(self.qTable[nowTime][argmax] == np.amin(self.qTable[nowTime][argmax])).flatten().tolist())
    
    def update_table(self, nowTime, chooseSignal, DiscomfortValueList):
        argmax = np.random.choice(np.argwhere(DiscomfortValueList == np.amax(DiscomfortValueList)).flatten().tolist())
        reward = np.sum(DiscomfortValueList)
        nextSignal = np.min(self.qTable[nowTime][chooseSignal])
        self.qTable[nowTime][chooseSignal][argmax] = \
            (1 - self.conf.qAlpha) * self.qTable[nowTime][chooseSignal][argmax] + \
            self.conf.qAlpha * (reward + (self.conf.qGamma * nextSignal))
        # print("Update is {} {}".format(chooseSignal, argmax))
        # print(self.qTable[nowTime])
