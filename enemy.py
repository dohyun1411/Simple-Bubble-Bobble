import pygame
import random

from global_variables import *


class Enemy(pygame.sprite.Sprite):

    def __init__(
        self,
        images,
        pos=None, # position
        screen_info=None,
        dir = enemy_dir # direction
        ):

        super(Enemy,  self).__init__()

        id_, self.image = random.choice(list(images.items()))
        self.dangerous = id_ == 'reaper2'
        self.original_image = self.image

        # assert pos or screen_info, 'Either pos or screen_info must be given to create Charater'
        if pos:
            self.pos = pos
        else:
            self.pos = (screen_info['width'] - screen_info['x_offset'], screen_info['y_offset'])
        self.rect = self.image.get_rect(center=self.pos)

        self.dir = dir
    
    def get_pos(self):
        return self.pos
    
    def get_rect(self):
        return self.rect
    
    def set_dir(self, dir):
        self.dir = dir

    def walk(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos = self.rect.center
            self.dir = -self.dir
            return True
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
            self.pos = self.rect.center
            self.dir = -self.dir
            return True
        
        self.pos = self.rect.center
        return False
        
    def draw(self, screen):
        # Flip image to corresponding direction
        flipping = True if self.dir == LEFT else False
        self.image = pygame.transform.flip(self.original_image, flipping, False)
        screen.blit(self.image, self.rect)
