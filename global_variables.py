import os

# Colors
WHITE = (255, 255, 255)

# Directions
LEFT = -1
RIGHT = 1

# Player configs
player_dir = RIGHT # player direction
player_speed = 15 # player x speed
player_dx = 0 # player dx
player_width = 64

# Map configs
brick_size = 56
floor_interval = 220

# Screen
screen_width = 1200
screen_height = 720
screen_info = {
    'width': screen_width,
    'height': screen_height,
    'x_offset': 36,
    'y_offset': 36 + brick_size
}