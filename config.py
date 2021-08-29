import random

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Directions
LEFT = -1
RIGHT = 1

# Screen
screen_width = 1200
screen_height = 720
screen_info = {
    'width': screen_width,
    'height': screen_height,
    'x_offset': 36,
    'y_offset': 60
}
fps = 120

# Player configs
player_dir = RIGHT # player direction
player_speed = 10
player_dx = 0
player_dx_left = 0
player_dx_right = 0
player_width = 40
player_height = 50
is_jumpping = False
player_jumping_speed = 28
player_dy = 0
gravity = 2

# Map configs
brick_size = 40
first_y = screen_height - brick_size // 2 # 700
second_y = first_y - 180
third_y = second_y - 180
fourth_y = third_y - 180