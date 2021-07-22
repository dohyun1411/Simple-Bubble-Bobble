import os
import random
import pygame

from global_variables import *


class Brick(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super(Brick, self).__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

floor_types = [ # _ : brick, . : empty
    '.._________...._______',
    '..____..____..____..__',
    '.._____....____..___..',
    '..____.._____...______',
    '______....________....',
    '_______...___...______',
    '___..___________...___',
    '__..___..____.._______',
    '______..___..___..____',
    '______________________' # only use for top and bottom
]

def create_map(image):

    # 2nd and 3rd floor
    second = random.choice(floor_types[:-1])
    third = random.choice(floor_types[:-1])

    # bottom and top
    bottom = random.choice(floor_types[4:])
    if bottom == floor_types[-1]: # map is closed
        top = random.choice(floor_types)
    else: # map is open
        top = bottom
    
    brick_group = pygame.sprite.Group()
    # image = random.choice(list(images.values()))
    for idx, char in enumerate(top):
        if char == '_':
            x = idx * brick_size + brick_size // 2
            y = brick_size // 2
            brick_group.add(Brick(image, (x, y)))

    for idx, char in enumerate(third):
        if char == '_':
            x = idx * brick_size + brick_size // 2
            y = floor_interval + brick_size // 2
            brick_group.add(Brick(image, (x, y)))

    for idx, char in enumerate(second):
        if char == '_':
            x = idx * brick_size + brick_size // 2
            y = 2 * floor_interval + brick_size // 2
            brick_group.add(Brick(image, (x, y)))

    for idx, char in enumerate(bottom):
        if char == '_':
            x = idx * brick_size + brick_size // 2
            y = 3 * floor_interval + brick_size // 2 + 4
            brick_group.add(Brick(image, (x, y)))
    
    return brick_group            