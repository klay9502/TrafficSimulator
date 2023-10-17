import os
import logging

class Configuration:
    def __init__(self, filePath) -> None:
        self.filePath = filePath

        self.simulateTime : float = 0.0
        self.simulateInterval : float = 0.0

        self.timeInterval : int = 0

        self.vehiclePatternFilePath : str = ""
        self.pedPatternFilePath : str = ""
        self.gauseStandardDeviation : float = 0.0
        self.learningType : str = ""

        self.epsilon : float = 0.0
        
        self.qAlpha : float = 0.0
        self.qGamma : float = 0.0

        self.weight : float = 0.0

        self.intersectionType : int = 0
        self.numberOfLanes : int = 0

        self.signalInterval : float = 0.0

        self.discomfortRange : float = 0.0
        self.discomfortInterval : float = 0.0

        self.vehicleSpeed : float = 0.0

        self.pltMovingAverageWindow : float = 0.0
        self.pltDVRecordInterval : float = 0.0

        self.parse_config()
        
    def parse_config(self) -> None:
        with open(self.filePath, "r") as file:
            for line in file:
                try:
                    line = line.strip()
                    if line.startswith("#"):
                        # Exception the Comment Line.
                        continue
                    if line == "":
                        continue

                    key, val = line.split("=")
                    key = key.strip()
                    val = val.strip()

                    if key == "SIMULATE_TIME":
                        self.simulateTime = float(val)
                    if key == "SIMULATE_INTERVAL":
                        self.simulateInterval = float(val)
                    if key == "TIME_INTERVAL":
                        self.timeInterval = int(val)
                    if key == "VEHICLE_PATTERN_FILENAME":
                        path = os.getcwd()
                        path = path + "\patterns"
                        fileName = os.path.join(path, val)
                        if os.path.exists(fileName):
                            self.vehiclePatternFilePath = fileName
                        else:
                            logging.error("Configuration:parse_config() - There are no file in {}".format(fileName))
                    if key == "PEDESTRIAN_PATTERN_FILENAME":
                        path = os.getcwd()
                        path = path + "\patterns"
                        fileName = os.path.join(path, val)
                        if os.path.exists(fileName):
                            self.pedPatternFilePath = fileName
                        else:
                            logging.error("Configuration:parse_config() - There are no file in {}".format(fileName))
                    if key == "GAUSS_STANDARD_DEVIATION":
                        self.gauseStandardDeviation = float(val)
                    if key == "LEARNING_TYPE":
                        self.learningType = str(val)
                    if key == "EPSILON":
                        self.epsilon = float(val)
                    if key == "Q_ALPHA":
                        self.qAlpha = float(val)
                    if key == "Q_GAMMA":
                        self.qGamma = float(val)
                    if key == "WEIGHT":
                        self.weight = float(val)
                    if key == "INTERSECTION_TYPE":
                        self.intersectionType = int(val)
                    if key == "NUMBER_OF_LANES":
                        self.numberOfLanes = int(val)
                    if key == "SIGNAL_INTERVAL":
                        self.signalInterval = float(val)
                    if key == "DISCOMFORT_RANGE":
                        self.discomfortRange = float(val)
                    if key == "DISCOMFORT_INTERVAL":
                        self.discomfortInterval = float(val)
                    if key == "VEHICLE_SPEED":
                        self.vehicleSpeed = float(val)
                    if key == "PLT_MOVING_AVERAGE_WINDOW":
                        self.pltMovingAverageWindow = float(val)
                    if key == "PLT_DISCOMFORT_VALUE_RECORD_INTERVAL":
                        self.pltDVRecordInterval = float(val)

                except:
                    logging.error("Configuration:parse_config() - Error in parsing the line: {}".format(line))
                    raise