from dataclasses import dataclass, asdict
import json
import time


@dataclass
class GloveState:
    timestamp: float

    # Hand orientation, degrees
    pitch: float = 0.0
    roll: float = 0.0
    yaw: float = 0.0

    # Finger bend: 0.0 = straight, 1.0 = fully bent
    thumb: float = 0.0
    index: float = 0.0
    middle: float = 0.0
    ring: float = 0.0
    pinky: float = 0.0

    # Physical controls
    trigger: bool = False

    # Device information
    battery: float = 100.0

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, data: str):
        return cls(**json.loads(data))


def neutral_state() -> GloveState:
    return GloveState(timestamp=time.time())