import os
import pygame

from global_variables import *


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        images,
        status='standing',
        pos=None, # position
        screen_info=None,
        dir = player_dir # direction
        ):

        super(Player, self).__init__()

        self.images = images
        self.image = images[status]
        self.original_image = self.image
        self.status = status

        assert pos or screen_info, 'Either pos or screen_info must be given to create Player'
        if pos:
            self.pos = pos
        else:
            self.pos = (screen_info['offset'], screen_info['height'] - screen_info['offset'])
        self.rect = self.image.get_rect(center=self.pos)

        self.dir = dir

    def set_image(self, status):
        """
        Set image to corresponding status.
        """
        self.image = self.images[self.status]
        self.original_image = self.image
    
    def set_dir(self, dir):
        self.dir = dir

    def stand(self):
        self.status = 'standing'
        self.set_image(self.status)

    def walk(self, dx):
        self.rect.x += dx

        # Change status and image
        if self.status == 'standing':
            self.status = 'walking'
        elif self.status == 'walking':
            self.status = 'standing'
        
        self.set_image(self.status)
        
    def draw(self, screen):
        # Flip image to corresponding direction
        flipping = True if self.dir == LEFT else False
        self.image = pygame.transform.flip(self.original_image, flipping, False)
        screen.blit(self.image, self.rect)