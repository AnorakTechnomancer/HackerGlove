from dataclasses import dataclass


@dataclass
class DroneState:
    x: float = 0.0
    y: float = 0.0
    altitude: float = 0.0
    armed: bool = False


class DroneSimulator:

    def __init__(self):
        self.state = DroneState()

    def arm(self):
        self.state.armed = True

    def disarm(self):
        self.state.armed = False

    def update(self, direction, control_active):

        # No movement without the dead-man switch.
        if not control_active:
            return

        # No movement while disarmed.
        if not self.state.armed:
            return

        if direction == "FORWARD":
            self.state.y += 1

        elif direction == "BACKWARD":
            self.state.y -= 1

        elif direction == "LEFT":
            self.state.x -= 1

        elif direction == "RIGHT":
            self.state.x += 1