from dataclasses import dataclass
from enum import Enum

from glove.protocol import GloveState


class Pose(Enum):
    OPEN = "OPEN"
    FIST = "FIST"
    POINT = "POINT"
    TWO_FINGER = "TWO_FINGER"
    UNKNOWN = "UNKNOWN"


class Direction(Enum):
    NEUTRAL = "NEUTRAL"
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


@dataclass
class GestureResult:
    pose: Pose
    direction: Direction
    control_active: bool


# Eventually these become configurable/calibrated.
BENT_THRESHOLD = 0.65

# Hand must move this far from neutral before it counts.
PITCH_DEADZONE = 15.0
ROLL_DEADZONE = 15.0


def bent(value: float) -> bool:
    return value >= BENT_THRESHOLD


def straight(value: float) -> bool:
    return value < BENT_THRESHOLD


def detect_pose(state: GloveState) -> Pose:

    fingers = [
        bent(state.thumb),
        bent(state.index),
        bent(state.middle),
        bent(state.ring),
        bent(state.pinky),
    ]

    # Nothing bent
    if fingers == [False, False, False, False, False]:
        return Pose.OPEN

    # Everything bent
    if fingers == [True, True, True, True, True]:
        return Pose.FIST

    # Index straight, other fingers bent
    if (
        straight(state.index)
        and bent(state.middle)
        and bent(state.ring)
        and bent(state.pinky)
    ):
        return Pose.POINT

    # Index + middle straight, ring + pinky bent
    if (
        straight(state.index)
        and straight(state.middle)
        and bent(state.ring)
        and bent(state.pinky)
    ):
        return Pose.TWO_FINGER

    return Pose.UNKNOWN


def detect_direction(state: GloveState) -> Direction:

    pitch = state.pitch
    roll = state.roll

    # Stay neutral inside the deadzone.
    if (
        abs(pitch) < PITCH_DEADZONE
        and abs(roll) < ROLL_DEADZONE
    ):
        return Direction.NEUTRAL

    # Whichever axis is tilted further wins.
    if abs(pitch) >= abs(roll):

        if pitch >= PITCH_DEADZONE:
            return Direction.FORWARD

        if pitch <= -PITCH_DEADZONE:
            return Direction.BACKWARD

    else:

        if roll >= ROLL_DEADZONE:
            return Direction.RIGHT

        if roll <= -ROLL_DEADZONE:
            return Direction.LEFT

    return Direction.NEUTRAL


def interpret(state: GloveState) -> GestureResult:

    pose = detect_pose(state)

    # Always detect hand direction.
    direction = detect_direction(state)

    # Trigger determines whether actions are allowed,
    # not whether orientation is detected.
    control_active = state.trigger

    return GestureResult(
        pose=pose,
        direction=direction,
        control_active=control_active,
    )