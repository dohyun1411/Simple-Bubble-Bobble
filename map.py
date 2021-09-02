import random

import pygame

from screen import ScreenConfig
  

class BrickConfig:
    
    size = 40


class Brick(pygame.sprite.Sprite):

    def __init__(self, image, x_index, y_index):
        super(Brick, self).__init__()

        self.image = image
        self.x_index = x_index
        self.y_index = y_index

        x = x_index * BrickConfig.size + BrickConfig.size / 2
        y = MapConfig.top_y - y_index * MapConfig.interval
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=self.pos)


class MapConfig:

    num_floor = 4
    floor_types = [ # _ : brick, . : empty
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
    bottom_floor_type = '______________________________'
    interval = 180 # TODO: make interval depend on num_floor
    top_y = ScreenConfig.height - BrickConfig.size / 2


class Map:

    group = pygame.sprite.Group()
    
    def __init__(self, brick_image):
        for floor in range(MapConfig.num_floor):
            if floor == 0: # bottom
                floor_type = MapConfig.bottom_floor_type
            else:
                random_index = random.randint(0, len(MapConfig.floor_types) - 1)
                floor_type = MapConfig.floor_types[random_index]
                
            for i, char in enumerate(floor_type):
                if char == '_':
                    Map.group.add(Brick(brick_image, i, floor))