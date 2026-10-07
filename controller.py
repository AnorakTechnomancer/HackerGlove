from enum import Enum

from glove.gestures import interpret
from drone.simulator import DroneSimulator


class Mode(Enum):
    UI = "UI"
    DRONE = "DRONE"


class WristController:

    def __init__(self):
        self.mode = Mode.UI
        self.drone = DroneSimulator()

    def set_mode(self, mode):
        self.mode = mode

    def process(self, glove_state):

        gesture = interpret(glove_state)

        if self.mode == Mode.DRONE:

            self.drone.update(
                gesture.direction.value,
                gesture.control_active
            )

        return gesture