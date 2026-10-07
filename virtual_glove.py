import time

from glove.protocol import GloveState
from glove.gestures import interpret
from controller import WristController, Mode


state = GloveState(timestamp=time.time())

controller = WristController()
controller.set_mode(Mode.DRONE)
controller.drone.arm()

STEP = 5.0


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def show_state():
    print("\033[2J\033[H", end="")

    print("=== WRISTDECK // VIRTUAL GLOVE ===")
    print()
    print(f"Pitch:   {state.pitch:>7.1f}°")
    print(f"Roll:    {state.roll:>7.1f}°")
    print(f"Yaw:     {state.yaw:>7.1f}°")
    print()
    print(f"Thumb:   {state.thumb * 100:>6.0f}%")
    print(f"Index:   {state.index * 100:>6.0f}%")
    print(f"Middle:  {state.middle * 100:>6.0f}%")
    print(f"Ring:    {state.ring * 100:>6.0f}%")
    print(f"Pinky:   {state.pinky * 100:>6.0f}%")
    print()
    print(f"Trigger: {'HELD' if state.trigger else 'RELEASED'}")
    print(f"Battery: {state.battery:.0f}%")
    result = controller.process(state)
    print()
    print("INTERPRETATION")
    print("--------------")
    print(f"Pose:      {result.pose.value}")
    print(f"Direction: {result.direction.value}")
    print(f"Control:   {'ACTIVE' if result.control_active else 'SAFE'}")
    drone = controller.drone.state
    print()
    print("VIRTUAL DRONE")
    print("-------------")
    print(f"Armed:    {'YES' if drone.armed else 'NO'}")
    print(f"X:        {drone.x:.0f}")
    print(f"Y:        {drone.y:.0f}")
    print(f"Altitude: {drone.altitude:.0f}")
    print()
    print("CONTROLS")
    print("--------")
    print("W/S     Pitch")
    print("A/D     Roll")
    print("Q/E     Yaw")
    print("1-5     Toggle fingers")
    print("SPACE   Toggle trigger")
    print("R       Reset")
    print("X       Exit")
    print()
    print("JSON:")
    print(state.to_json())


def toggle_finger(name):
    current = getattr(state, name)
    setattr(state, name, 0.0 if current >= 0.5 else 1.0)


def main():
    global state

    while True:
        state.timestamp = time.time()
        show_state()

        command = input("\n> ").lower().strip()

        if command == "w":
            state.pitch += STEP

        elif command == "s":
            state.pitch -= STEP

        elif command == "a":
            state.roll -= STEP

        elif command == "d":
            state.roll += STEP

        elif command == "q":
            state.yaw -= STEP

        elif command == "e":
            state.yaw += STEP

        elif command == "1":
            toggle_finger("thumb")

        elif command == "2":
            toggle_finger("index")

        elif command == "3":
            toggle_finger("middle")

        elif command == "4":
            toggle_finger("ring")

        elif command == "5":
            toggle_finger("pinky")

        elif command == "space":
            state.trigger = not state.trigger

        elif command == "r":
            state = GloveState(timestamp=time.time())

        elif command == "x":
            break

        state.pitch = clamp(state.pitch, -90, 90)
        state.roll = clamp(state.roll, -90, 90)

        if state.yaw > 180:
            state.yaw -= 360

        if state.yaw < -180:
            state.yaw += 360


if __name__ == "__main__":
    main()