import pygame
import random

from config import *


class Enemy(pygame.sprite.Sprite):

    def __init__(
        self,
        images,
        map,
        group,
        list_
        ):

        super(Enemy,  self).__init__()
        
        self.images = images
        weights = [0.5, 0.0, 0.3, 0.2]
        id_, self.image = random.choices(list(images.items()), weights=weights)[0]
        self.type = id_
        self.original_image = self.image
        self.is_collided_with_wall = 1
        self.group = group
        self.list = list_

        self.pos = (random.randint(36, screen_width - 36), 36)
        self.rect = self.image.get_rect(center=self.pos)

        if self.type == 'reaper':
            self.x_speed = random.randint(1, 2)
        elif self.type == 'reaper3':
            self.x_speed = random.randint(3, 4)
        elif self.type == 'reaper4':
            self.x_speed = random.randint(5, 6)
        self.y_speed = 2
        self.flipping = False
        self.dir = random.choice([LEFT, RIGHT])
        self.map = map
        self.collided_brick = None
        self.status = 'walking'
        self.turn = 0
        self.prev_action = self.walk
        self.jump_before = False
        self.original_type = id_
        self.original_original_image = self.original_image
        self.original_x_speed = self.x_speed
        self.dangerous_count = 0

    def set_pos(self, pos):
        self.pos = pos
        self.rect.center =pos

    def stand(self):
        if self.turn % 10 == 1:
            self.dir *= -1
            self.flip()
        self.turn += 1

    def walk(self):
        if brick := pygame.sprite.spritecollideany(self, self.map):
            self.collided_brick = brick
        else:
            self.collided_brick = None
            self.land()
            return

        self.status = 'walking'
        dx = self.x_speed * self.dir
        self.rect.x += dx
        if self.rect.left < -10:
            self.dir *= -1
        elif self.rect.right > screen_width + 10:
            self.dir *= -1
        self.pos = self.rect.center
        self.flip()
        self.turn += 1
        
    def jump(self):
        self.status = 'jumping'
        self.rect.y -= self.y_speed
        self.pos = self.rect.center
        brick = pygame.sprite.spritecollideany(self, self.map)
        self.collided_brick = brick
        if (brick and self.turn > 4 and brick.rect.top + 4 > self.rect.bottom) \
            or self.rect.top < 0:
            if self.turn > 8:
                self.turn = 100
                self.set_correct_pos(force=True)
                self.status = 'walking'
        self.turn += 1

    def land(self):
        self.status = 'landing'
        self.rect.y += self.y_speed
        self.pos = self.rect.center
        if brick := pygame.sprite.spritecollideany(self, self.map):
            self.collided_brick = brick
            return True
        return False
    
    def set_correct_pos(self, force=False):
        if self.collided_brick and (self.status not in  {'landing', 'jumping'} or force):
            if self.rect.bottom != self.collided_brick.rect.top + 20:
                self.rect.bottom = self.collided_brick.rect.top + 20
                self.pos = self.rect.center

    def act_randomly(self):
        self.flip()
        if self.dangerous_count:
            self.dangerous_count += 1
            if self.dangerous_count > 500:
                self.type = self.original_type
                self.image = self.images[self.type]
                self.original_image = self.original_original_image
                self.x_speed = self.original_x_speed
                self.dangerous_count = 0

        self.max_turn = random.choice([40, 50, 60, 70, 80])
        if self.turn < self.max_turn or self.status in {'landing', 'jumping'}:
            return self.prev_action()
        random_actions = [self.stand, self.walk, self.jump]
        if self.get_jump_cond():
            if self.jump_before:
                weights = [0.2, 0.8, 0.0]
                self.jump_before = False
            else:
                weights = [0.2, 0.2, 0.6]
                self.jump_before = True
        else:
            weights = [0.2, 0.8, 0.0]
        self.prev_action = random.choices(random_actions, weights=weights)[0]
        self.turn = 0
        return self.prev_action()

    def flip(self):
        flipping = True if self.dir == LEFT else False
        self.image = pygame.transform.flip(self.original_image, flipping, False)
        self.rect = self.image.get_rect(center=self.pos)
    
    def get_jump_cond(self):
        for h in [50, 100, 150, 200]:
            moved_pos = (self.pos[0], self.pos[1] - h)
            pseudo = PseudoEnemy(moved_pos, self.image)
            if pygame.sprite.spritecollideany(pseudo, self.map):
                return True
        return False
        
    def remove(self):
        self.group.remove(self)
    
    def make_dangerous(self):
        self.type = 'reaper2'
        self.image = self.images[self.type]
        self.original_image = self.image
        self.x_speed = 1
        self.dangerous_count = 1


class PseudoEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super(PseudoEnemy,  self).__init__()
        self.pos = pos
        self.rect = image.get_rect(center=self.pos)