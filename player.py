import pygame

from screen import ScreenConfig
from map import BrickConfig, Map
from character import Character, Direction


class PlayerConfig:

    width = 40
    height = 50

    x_speed = 6
    y_speed = 20 # jumping speed
    gravity = 1

    life = 3

    max_walking_image_delay = 4 # delay for walking image
    
    brick_gap = 5 # gap between player and collided brick


class Player(Character):

    group = pygame.sprite.Group()

    def __init__(self, images):
        super(Player, self).__init__()

        self.images = images
        self.status = 'standing'

        self.dx_left = 0
        self.dx_right = 0
        self.dy = 0
        # self.pos = (ScreenConfig.x_offset, ScreenConfig.height - ScreenConfig.y_offset)
        self.pos = (500, ScreenConfig.height - ScreenConfig.y_offset)

        self.life = PlayerConfig.life

        self.walking_image_delay = 0
        
        self.is_jumpping = False

        Player.group.add(self)

    @property
    def is_dead(self):
        return self.life == 0
    
    def stand(self):
        if not self.is_jumpping:
            self.status = 'standing'
    
    def walk(self):
        if not self.is_jumpping:
            if self.walking_image_delay == 0:
                if self.status != 'walking':
                    self.status = 'walking'
                elif self.status != 'standing':
                    self.status = 'standing'
        self.walking_image_delay += 1
        self.walking_image_delay %= PlayerConfig.max_walking_image_delay

        self.move_to_x()

    def jump(self):
        if self.dy < 0:
            self.move_to_y()
            self.dy += PlayerConfig.gravity

            self.status = 'jumping'
            self.is_jumpping = True
        else:
            return self.land()
    
    def land(self):
        if self.collided_bricks:
            self.set_correct_pos()
        else:
            self.move_to_y()
            self.dy += PlayerConfig.gravity

            self.status = 'landing'
            self.is_jumpping = True
    
    def set_correct_pos(self):
        correcting = False
        if self.dir == Direction.RIGHT:
            min_left = min(brick.rect.left for brick in self.collided_bricks)
            if 0 < self.rect.right - min_left < BrickConfig.size / 2:
                self.rect.right = min_left
                self.rect = self.rect
                correcting = True
        else:
            max_right = max(brick.rect.right for brick in self.collided_bricks)
            if 0 < max_right - self.rect.left < BrickConfig.size / 2:
                self.rect.left = max_right
                self.rect = self.rect
                correcting = True

        if not correcting:
            self.dy = 0
            self.is_jumpping = False
            collided_brick_top =  self.collided_bricks[0].rect.top
            if self.rect.bottom > collided_brick_top + PlayerConfig.brick_gap:
                self.rect.bottom = collided_brick_top + PlayerConfig.brick_gap
                self.rect = self.rect

    def move(self):
        player_brick = pygame.sprite.groupcollide(Player.group, Map.group, False, False)
        if player_brick:
            self.collided_bricks = player_brick[self]
        else:
            self.collided_bricks = None

        if self.dx:
            self.walk()
        else:
            self.stand()

        if self.is_jumpping:
            self.jump()
        else:
            self.land()

    def shoot(self):
        self.status = 'shooting'