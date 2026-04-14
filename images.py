from config import *
from pygame import image, transform

DARK_BG = "images/dark_bg.jpg"

dark_bg = image.load(DARK_BG)
dark_bg = transform.scale(dark_bg, (window_w, window_h))