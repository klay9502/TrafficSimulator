class ObjectGenerator:
    def __init__(self, env, conf, pattern) -> None:
        self.env = env
        self.conf = conf
        self.pattern = pattern

        self.idCounter = 0