import pygame
import random

from config import *


class Brick(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super(Brick, self).__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
    
    def get_pos(self):
        return self.pos

    def get_rect(self):
        return self.rect

floor_types = [ # _ : brick, . : empty
    '______________________________',
    '___________........___________',
    '....______________________....',
    '_______.....______....._______',
    '___...____......______________',
    '______________......____...___',
    '....____....______............',
    '............______....____....',
    '...__...__...__...__...__...__',
    '__...__...__...__...__...__...'
]

def create_map(image):

    # 2nd, 3rd and 4th floor
    second = floor_types[random.randint(1, len(floor_types) - 1)]
    third = floor_types[random.randint(1, len(floor_types) - 1)]
    fourth = floor_types[random.randint(1, len(floor_types) - 1)]

    # bottom
    bottom = floor_types[0]
    
    brick_group = pygame.sprite.Group()
    brick_dict = {} # pos: Brick

    for idx, char in enumerate(fourth):
        if char == '_':
            x = idx * brick_size + brick_size // 2
            y = fourth_y
            brick_dict[(x, y)] = Brick(image, (x, y))

    for idx, char in enumerate(third):
        if char == '_':
            x = idx * brick_size + brick_size // 2
            y = third_y
            brick_dict[(x, y)] = Brick(image, (x, y))

    for idx, char in enumerate(second):
        if char == '_':
            x = idx * brick_size + brick_size // 2
            y = second_y
            brick_dict[(x, y)] = Brick(image, (x, y))

    for idx, char in enumerate(bottom):
        if char == '_':
            x = idx * brick_size + brick_size // 2
            y = first_y
            brick_dict[(x, y)] = Brick(image, (x, y))

    for brick in brick_dict.values():
        brick_group.add(brick)

    return brick_group, brick_dict