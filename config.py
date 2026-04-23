'''
All game settings are stored in this file.
'''

from os import environ
#from pygame import init
from pygame.locals import *

# Display choice. Doesn't seem to work on Windows, though.
environ["SDL_VIDEO_CENTERED"] = "1"

#init()

#window_w = int(display.get_desktop_sizes()[0][0] * 0.8)
#window_h = int(display.get_desktop_sizes()[0][1] * 0.8)

WINDOW_W = 800
WINDOW_H = 600
CAPTION = "MAYHEM"
BORDER_THICKNESS = 10

THEME_PATH = "theme.json"
FRAMERATE = 60
COLORS = {
    "BACKGROUND": (20, 20, 20),
    "P1": (255, 100, 100, 128),
    "P2": (100, 100, 255, 128)
}

G_ACCELERATION = 9.81    # Could maybe vary based on altitude(?).
BUMPING_BUFFER = 1     # Number of pixels

# Player specs
PLAYER = {
    "WIDTH": WINDOW_W * 0.04,
    "HEIGHT": WINDOW_W * 0.04 * 1.618,
    "WEIGHT": 5000,    # In kg (Perhaps not relevant in the vacuum of space?)
    "LIVES": 5,
    "ROTATION_SPEED": 180,  # Degrees per second.
    "ACCELERATION": 15, # Acceleration when thrusting.
    "MAX_THRUST": 12,
    "MAX_FALL_VELOCITY": 8,
    "COLLISION_BUMP": 5,
    "CONTROLS": {
        "P1": {
            "thrust": K_w,
            "rotate_counter_clockwise": K_a,
            "rotate_clockwise": K_d,
            "fire": K_s
        },
        "P2": {
            "thrust": K_UP,
            "rotate_counter_clockwise": K_LEFT,
            "rotate_clockwise": K_RIGHT,
            "fire": K_DOWN
        }
    },
    "COLOR": {
        "P1": COLORS["P1"],
        "P2": COLORS["P2"]
    }
}
#P1_CONTROLS = {
#    "thrust": K_w,
#    "rotate_counter_clockwise": K_a,
#    "rotate_clockwise": K_d,
#    "fire": K_s
#}
#P2_CONTROLS = {
#    "thrust": K_UP,
#    "rotate_counter_clockwise": K_LEFT,
#    "rotate_clockwise": K_RIGHT,
#    "fire": K_DOWN
#}
BULLET = {
    "RADIUS": WINDOW_W * 0.005,
    "SPEED": 500
}