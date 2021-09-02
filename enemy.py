import random

import pygame

from screen import ScreenConfig
from character import Character, Direction


class EnemyConfig:

    name = "reaper"
    num_type = 4
    max_time_to_be_dangerous = 500

    y_speed = 2


class Enemy(Character):

    group = pygame.sprite.Group()
    count = 0

    def __init__(self, images, round):
        super(Enemy, self).__init__()

        self.images = images
        self.round = round

        # TODO: make status depends on round
        random_status = random.randint(1, EnemyConfig.num_type)
        self.status = EnemyConfig.name + str(random_status)

        if random_status == EnemyConfig.num_type:
            self.make_dangerous()
        else:
            self.x_speed = random.randint(2 * random_status - 1, 2 * random_status)

        self.dir = random.choice([Direction.LEFT, Direction.RIGHT])
        self.dx = 0
        self.dy = 0
        x = random.randint(ScreenConfig.x_offset, ScreenConfig.width - ScreenConfig.x_offset)
        y = ScreenConfig.x_offset
        self.pos = (x, y)

        self.time_to_be_dangerous = 0

        Enemy.group.add(self)
        Enemy.count += 1
    
    def make_dangerous(self):
        self.status = EnemyConfig.name + str(EnemyConfig.num_type)
        self.x_speed = 1
        self.time_to_be_dangerous = 1