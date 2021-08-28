import random
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

        # assert pos or screen_info, 'Either pos or screen_info must be given to create Charater'
        if pos:
            self.pos = pos
        else:
            self.pos = (screen_info['x_offset'], screen_info['height'] - screen_info['y_offset'])
        self.rect = self.image.get_rect(center=self.pos)

        self.dir = dir
        self.standing_walking_count = 0
        self.collided_brick = None
        self.shooting_image_count = 0
    
    def get_pos(self):
        return self.pos
    
    def get_rect(self):
        return self.rect

    def set_image(self, status):
        """
        Set image to corresponding status.
        """
        
        if status == 'shooting':
            self.shooting_image_count = 4
        self.shooting_image_count -= 1
        if self.shooting_image_count > 0:
            self.status = 'shooting'
        else:
            self.status = status

        self.image = self.images[self.status]
        self.original_image = self.image
    
    def set_dir(self, dir):
        self.dir = dir

    def stand(self):
        self.status = 'standing'
        self.set_image(self.status)
    
    def set_correct_pos(self):
        if self.status != 'landing':
            if self.rect.bottom != self.collided_brick.rect.top + 5:
                self.rect.bottom = self.collided_brick.rect.top + 5
                self.pos = self.rect.center

    def walk(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
        self.pos = self.rect.center

        # Change status and image
        # self.standing_walking_count += 1
        # if self.standing_walking_count == 6:
        #     self.standing_walking_count = 0
        #     if self.status != 'walking':
        #         self.status = 'walking'
        #     elif self.status != 'standing':
        #         self.status = 'standing'
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

        for brick in map:
            if pygame.sprite.collide_mask(self, brick):
                self.collided_brick = brick
                return True

        return False # still falling
    
    def shoot(self):
        self.set_image('shooting')


class Bubble(pygame.sprite.Sprite):

    def __init__(
        self,
        image,
        dir,
        pos=None,
        ):

        super(Bubble,  self).__init__()

        self.image = image
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.dir = dir
        self.life = 10
        self.count = 0
    
    def walk(self):
        self.rect.y -= 4
    
    def shoot(self):
        if self.count < 16:
            self.count += 1
            self.rect.x += 4 * self.dir
            self.pos = self.rect.center
            return self.shoot()
        return self.walk()
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
