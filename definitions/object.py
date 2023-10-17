class Object:
    def __init__(self, env, conf, objectID) -> None:
        self.env = env
        self.conf = conf

        self.objectID = objectID

        self.discomfortValue = 0.0
        self.spawnedTime = env.now

        self.bIsRelease = False