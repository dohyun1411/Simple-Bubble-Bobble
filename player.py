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

        super(Player,  self).__init__()

        self.images = images
        self.image = images[status]
        self.original_image = self.image
        self.status = status

        assert pos or screen_info, 'Either pos or screen_info must be given to create Charater'
        if pos:
            self.pos = pos
        else:
            self.pos = (screen_info['x_offset'], screen_info['height'] - screen_info['y_offset'])
        self.rect = self.image.get_rect(center=self.pos)

        self.dir = dir

        self.standing_walking_count = 0
    
    def get_pos(self):
        return self.pos
    
    def get_rect(self):
        return self.rect

    def set_image(self, status):
        """
        Set image to corresponding status.
        """
        self.status = status
        self.image = self.images[self.status]
        self.original_image = self.image
    
    def set_dir(self, dir):
        self.dir = dir

    def stand(self):
        self.status = 'standing'
        self.set_image(self.status)

    def walk(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
        self.pos = self.rect.center

        # Change status and image
        self.standing_walking_count += 1
        if self.standing_walking_count == 6:
            self.standing_walking_count = 0
            if self.status != 'walking':
                self.status = 'walking'
            elif self.status != 'standing':
                self.status = 'standing'
        
        self.set_image(self.status)
        
    def draw(self, screen):
        # Flip image to corresponding direction
        flipping = True if self.dir == LEFT else False
        self.image = pygame.transform.flip(self.original_image, flipping, False)
        screen.blit(self.image, self.rect)

    def jump(self, dy):
        assert dy >= 0
        self.rect.y -= dy
        self.pos = self.rect.center
        self.set_image('jumping')
    
    def land(self, dy, map):
        assert dy <= 0

        self.rect.y -= dy
        self.pos = self.rect.center
        self.set_image('landing')
        # if self.rect.left < 10 * brick_size or self.rect.right 


        if self.rect.bottom >= screen_height - brick_size:
            return True
        # for brick in map:
        #     brick_rect = brick.get_rect()
        #     if not pygame.sprite.collide_mask(self, brick): continue
        #     if self.rect.bottom >= brick_rect.top:
        #         return True # landing successufully
        return False # still falling