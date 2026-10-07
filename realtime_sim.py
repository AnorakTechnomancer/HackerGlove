import time
import pygame

from glove.protocol import GloveState
from glove.gestures import interpret


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

WIDTH = 1000
HEIGHT = 700

FPS = 60

ANGLE_SPEED = 70.0       # degrees/sec
RETURN_SPEED = 100.0     # degrees/sec
MAX_TILT = 45.0

DEADZONE = 15.0

DRONE_MAX_SPEED = 250.0  # pixels/sec


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def approach(value, target, amount):
    if value < target:
        return min(value + amount, target)

    if value > target:
        return max(value - amount, target)

    return value


def axis_from_angle(angle):
    """
    Converts hand angle into analog control.

    <= DEADZONE        = 0
    MAX_TILT           = +/-1
    """

    magnitude = abs(angle)

    if magnitude <= DEADZONE:
        return 0.0

    output = (magnitude - DEADZONE) / (MAX_TILT - DEADZONE)
    output = clamp(output, 0.0, 1.0)

    return output if angle > 0 else -output


# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WRISTDECK // Gesture Control Simulator")

clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 22)
small_font = pygame.font.SysFont("consolas", 17)
big_font = pygame.font.SysFont("consolas", 32)


state = GloveState(timestamp=time.time())

drone_x = WIDTH * 0.70
drone_y = HEIGHT * 0.50

running = True


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

while running:

    dt = clock.tick(FPS) / 1000.0

    # -------------------------------
    # EVENTS
    # -------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            # Finger toggles

            elif event.key == pygame.K_1:
                state.thumb = 0.0 if state.thumb >= 0.5 else 1.0

            elif event.key == pygame.K_2:
                state.index = 0.0 if state.index >= 0.5 else 1.0

            elif event.key == pygame.K_3:
                state.middle = 0.0 if state.middle >= 0.5 else 1.0

            elif event.key == pygame.K_4:
                state.ring = 0.0 if state.ring >= 0.5 else 1.0

            elif event.key == pygame.K_5:
                state.pinky = 0.0 if state.pinky >= 0.5 else 1.0

            elif event.key == pygame.K_r:
                state.pitch = 0
                state.roll = 0
                state.yaw = 0

                state.thumb = 0
                state.index = 0
                state.middle = 0
                state.ring = 0
                state.pinky = 0

    # -------------------------------
    # KEYBOARD STATE
    # -------------------------------

    keys = pygame.key.get_pressed()

    state.trigger = keys[pygame.K_SPACE]

    # PITCH

    if keys[pygame.K_w]:
        state.pitch += ANGLE_SPEED * dt

    elif keys[pygame.K_s]:
        state.pitch -= ANGLE_SPEED * dt

    else:
        state.pitch = approach(
            state.pitch,
            0,
            RETURN_SPEED * dt
        )

    # ROLL

    if keys[pygame.K_d]:
        state.roll += ANGLE_SPEED * dt

    elif keys[pygame.K_a]:
        state.roll -= ANGLE_SPEED * dt

    else:
        state.roll = approach(
            state.roll,
            0,
            RETURN_SPEED * dt
        )

    # YAW

    if keys[pygame.K_e]:
        state.yaw += ANGLE_SPEED * dt

    elif keys[pygame.K_q]:
        state.yaw -= ANGLE_SPEED * dt

    state.pitch = clamp(state.pitch, -MAX_TILT, MAX_TILT)
    state.roll = clamp(state.roll, -MAX_TILT, MAX_TILT)

    if state.yaw > 180:
        state.yaw -= 360

    if state.yaw < -180:
        state.yaw += 360

    state.timestamp = time.time()

    # -------------------------------
    # GESTURE INTERPRETATION
    # -------------------------------

    gesture = interpret(state)

    forward = axis_from_angle(state.pitch)
    sideways = axis_from_angle(state.roll)

    # Dead-man switch

    if not state.trigger:
        forward = 0.0
        sideways = 0.0

    # -------------------------------
    # DRONE MOVEMENT
    # -------------------------------

    drone_x += sideways * DRONE_MAX_SPEED * dt

    # Positive pitch = forward = up screen
    drone_y -= forward * DRONE_MAX_SPEED * dt

    drone_x = clamp(drone_x, 20, WIDTH - 20)
    drone_y = clamp(drone_y, 20, HEIGHT - 20)

    # -------------------------------
    # DRAW
    # -------------------------------

    screen.fill((15, 18, 22))

    # Divider

    pygame.draw.line(
        screen,
        (80, 80, 80),
        (430, 0),
        (430, HEIGHT),
        2
    )

    # Title

    title = big_font.render(
        "WRISTDECK // GLOVE SIM",
        True,
        (220, 220, 220)
    )

    screen.blit(title, (25, 20))

    # -------------------------------
    # TELEMETRY
    # -------------------------------

    lines = [

        f"Pitch      {state.pitch:7.1f} deg",
        f"Roll       {state.roll:7.1f} deg",
        f"Yaw        {state.yaw:7.1f} deg",

        "",

        f"Forward    {forward:+.2f}",
        f"Sideways   {sideways:+.2f}",

        "",

        f"Pose       {gesture.pose.value}",
        f"Direction  {gesture.direction.value}",

        "",

        f"Trigger    {'HELD' if state.trigger else 'RELEASED'}",
        f"Control    {'ACTIVE' if state.trigger else 'SAFE'}",

        "",

        f"Thumb      {state.thumb:.0f}",
        f"Index      {state.index:.0f}",
        f"Middle     {state.middle:.0f}",
        f"Ring       {state.ring:.0f}",
        f"Pinky      {state.pinky:.0f}",
    ]

    y = 90

    for line in lines:

        text = font.render(
            line,
            True,
            (210, 210, 210)
        )

        screen.blit(text, (30, y))

        y += 29

    # -------------------------------
    # DRONE
    # -------------------------------

    pygame.draw.circle(
        screen,
        (100, 200, 255),
        (int(drone_x), int(drone_y)),
        15
    )

    pygame.draw.circle(
        screen,
        (220, 220, 220),
        (int(drone_x), int(drone_y)),
        30,
        2
    )

    drone_label = small_font.render(
        "DRONE-01",
        True,
        (220, 220, 220)
    )

    screen.blit(
        drone_label,
        (drone_x - 38, drone_y + 38)
    )

    # -------------------------------
    # CONTROLS
    # -------------------------------

    controls = [
        "W/S     Pitch",
        "A/D     Roll",
        "Q/E     Yaw",
        "SPACE   Dead-man",
        "1-5     Finger toggle",
        "R       Reset glove",
        "ESC     Quit",
    ]

    y = 470

    for line in controls:

        text = small_font.render(
            line,
            True,
            (150, 150, 150)
        )

        screen.blit(text, (465, y))

        y += 25

    pygame.display.flip()


pygame.quit()