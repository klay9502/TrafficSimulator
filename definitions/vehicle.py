from definitions.object import Object


class Vehicle(Object):
    def __init__(self, env, conf, objectID, startDirection, targetDirection) -> None:
        super().__init__(env, conf, objectID, startDirection, targetDirection)