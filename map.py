import os
import random
import pygame

from global_variables import *


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
    '__________..........__________',
    '_______.....______....._______'
]

def create_map(image):

    # 2nd and 3rd floor
    second = floor_types[1]
    third = floor_types[2]
    fourth = floor_types[1]

    # bottom and top
    bottom = floor_types[0]
    top = floor_types[0]
    
    brick_group = pygame.sprite.Group()
    brick_dict = {} # pos: Brick
    # for idx, char in enumerate(top):
    #     if char == '_':
    #         x = idx * brick_size + brick_size // 2
    #         y = brick_size // 2
    #         brick_dict[(x, y)] = Brick(image, (x, y))

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

def get_nearest_brick_x(pos, brick_dict):
    x, _ = pos
    idx = x // brick_size
    brick_x = idx * brick_size + brick_size // 2
    return brick_x