'''
All game settings are stored in this file.
'''

from os import environ
from pygame import init, display, K_w, K_a, K_d, K_s, K_UP, K_LEFT, K_RIGHT, K_DOWN

p1_controls = {
    "thrust": K_w,
    "rotate_counter_clockwise": K_a,
    "rotate_clockwise": K_d,
    "fire": K_s
}

p2_controls = {
    "thrust": K_UP,
    "rotate_counter_clockwise": K_LEFT,
    "rotate_clockwise": K_RIGHT,
    "fire": K_DOWN
}

# Display choice. Doesn't seem to work on Windows, though.
environ["SDL_VIDEO_CENTERED"] = "1"

init()

window_w = int(display.get_desktop_sizes()[0][0] * 0.8)
window_h = int(display.get_desktop_sizes()[0][1] * 0.8)


THEME_PATH = "theme.json"
FRAMERATE = 30
BG_COLOR = (20, 20, 20)
P1_COLOR = (255, 100, 100, 128)
P2_COLOR = (100, 100, 255, 128)

PLAYER_W = window_w * 0.05
PLAYER_H = PLAYER_W * 1.618
PLAYER_WEIGHT = 5000    # In kg (Perhaps not relevant in the vacuum of space?)
#PLAYER_BOX_LEN = max(PLAYER_H, PLAYER_W) * 1.25
G_ACCELERATION = 9.8   # Should maybe vary based on altitude(?).
ROT_PER_SEC = 270
ROT_PER_FRAME = max(1, ROT_PER_SEC // FRAMERATE)