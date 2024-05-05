class ENV:
    AREA_WIDTH, AREA_HEIGHT = 1000, 1000
    AREA_SIZE = (AREA_WIDTH, AREA_HEIGHT)
    AREA_CENTRE = (AREA_WIDTH / 2, AREA_HEIGHT / 2)
    ACTIONS = 9
    COLORS = ['blue', 'green', 'red', 'yellow', 'pink', 'orange']

    N_AGENTS = 6
    START_RADIUS = 400.
    SHRINK_SPEED = 6.

    FPS = 60


class SCORES:
    KILL = 0.5
    WIN = 1.
    DIED = -1.
    ALIVE = 0.05


class CAR:
    CART_SIZE = (50, 30)
    VISION_LINE_LENGTH = 400
    COLLISION_TYPE = 1
    MAX_ANGULAR_VELOCITY = 2.


class COLORS:
    RED = (255, 0, 0)
    PURPLE = (128, 0, 128)
