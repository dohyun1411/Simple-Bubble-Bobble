import pygame

from config import *


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
        self.is_dead = False
    
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

        if brick := pygame.sprite.spritecollideany(self, map):
            self.collided_brick = brick
            return True

        return False # still falling
    
    def shoot(self):
        self.set_status = 'shooting'
        self.set_image('shooting')
    
    def dead(self, screen):
        self.set_status = 'dead'
        ghost_img = self.images['ghost']
        flipping = True if self.dir == LEFT else False
        ghost_img = pygame.transform.flip(ghost_img, flipping, False)
        screen.blit(ghost_img, self.rect)
        if not self.is_dead:
            self.rect.y -= 60
            screen.blit(self.images['boom'], self.rect)
            self.is_dead = True


class Bubble(pygame.sprite.Sprite):

    def __init__(
        self,
        images,
        dir,
        group,
        screen,
        pos=None,
        ):

        super(Bubble,  self).__init__()

        self.images = images
        self.image = images['bubble']
        self.original_image = self.image
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.dir = dir
        self.life = 10
        self.count = 0
        self.angle = 5
        self.rot_dir = dir
        self.original_rot_dir = 0
        self.group = group
        self.power = 3
        self.status = 0
        self.screen = screen
        self.enemy = None
        self.count = 0
    
    def set_original_rot_dir(self, angle=None, reverse=None, force=False):
        if not force and self.original_rot_dir:
            return
        if angle is not None:
            self.original_rot_dir = 1 if angle > 0 else -1
            return
        if reverse is not None:
            self.original_rot_dir *= -1

    def walk(self, map):
        self.power = 0
        brick = pygame.sprite.spritecollideany(self, map)
        self.angle = self.angle + self.rot_dir
        if brick and abs(self.rect.top - brick.rect.top) > abs(self.rect.top - brick.rect.bottom):
            self.set_original_rot_dir(angle=self.angle)
            self.rect.x += 2 * self.original_rot_dir
            if self.rect.right > screen_width or self.rect.left < 0:
                self.set_original_rot_dir(reverse=True, force=True)
        elif self.rect.y < 0:
            self.remove(re=True)
        else:
            self.rect.y -= 2
        self.pos = self.rect.center
        if self.angle > 20 or self.angle < -20:
            self.rot_dir *= -1
        self.rotate()
        self.set_correct_pos()
    
    def shoot(self, map):
        if self.count < 2:
            self.power -= 1
            self.count += 1
            self.rect.x += 40 * self.dir
            self.pos = self.rect.center
        else:
            return self.walk(map)
    
    def rotate(self):
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        if self.enemy:
            flipping = True if self.enemy.dir == LEFT else False
            self.image = pygame.transform.flip(self.image, flipping, False)
        self.rect = self.image.get_rect(center=self.pos)
    
    def remove(self, re=False):
        if self.enemy and re:
            self.group.remove(self)
            self.enemy.set_pos(self.pos)
            self.enemy.make_dangerous()
            self.enemy.group.add(self.enemy)
            self.screen.blit(self.images['boom'], self.pos)
            return
        if self.enemy:
            self.enemy.list.remove(self.enemy)
        self.group.remove(self)
        self.screen.blit(self.images['boom'], self.pos)

    def attack(self, enemy):
        self.original_image = self.images[enemy.type]
        self.status = 1
        self.enemy = enemy
    
    def set_correct_pos(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
        self.pos = self.rect.center