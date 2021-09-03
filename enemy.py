import random

import pygame

from screen import ScreenConfig
from map import MapConfig, Map
from character import Character, Direction


class EnemyConfig:
    
    name = 'reaper'
    num_type = 4

    max_time_being_dangerous = 500
    max_action_delay_list = [100, 150, 200]
    max_walking_action_delay = 16
    max_jumping_action_delay = 20

    brick_intersection = 20

    y_speed = 2
    x_speed_danger = 1 # x speed for dangerous enemy

    walking_weights = [0., 1., 0.]
    walking_jumping_weights = [0., 0.2, 0.8]
    standing_walking_weights = [0.2, 0.8, 0.]
    standing_walking_jumping_weights = [0.2, 0.2, 0.6]


class Enemy(Character):

    group = pygame.sprite.Group()
    count = 0

    def __init__(self, images, round):
        super(Enemy, self).__init__()

        self.images = images
        self.round = round

        # TODO: make id depends on round
        # self.id = random.randint(1, EnemyConfig.num_type)
        self.id = 1

        if self.id == EnemyConfig.num_type:
            self.make_dangerous()
        else:
            self.x_speed = random.randint(2 * self.id - 1, 2 * self.id)

        self.dir = random.choice([Direction.LEFT, Direction.RIGHT])
        self.dx = self.x_speed
        self.dy = EnemyConfig.y_speed
        x = random.randint(ScreenConfig.x_offset, ScreenConfig.width - ScreenConfig.x_offset)
        y = ScreenConfig.x_offset
        self.pos = (x, y)
        
        self.collided_brick = None

        self.original_id = self.id
        self.original_original_image = self.original_image
        self.original_x_speed = self.x_speed
        self.time_being_dangerous = 0

        self.status = 'walking'
        self.prev_action = self.walk
        self.stand_before = False
        self.jump_before = False
        self.action_delay = 0

        Enemy.group.add(self)
        Enemy.count += 1

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
        image_name = EnemyConfig.name + str(id)
        self.original_image = self.images[image_name]
     
    def move_to_x(self):
        self.rect.x += self.dx
        if self.rect.left < 0:
            self.dir *= -1
            self.dx *= -1
        elif self.rect.right > ScreenConfig.width:
            self.dir *= -1
            self.dx *= -1
        self.rect = self.rect   

    def make_dangerous(self):
        self.id = EnemyConfig.num_type
        self.x_speed = EnemyConfig.x_speed_danger
        self.time_being_dangerous = 1
    
    def remove(self):
        pass

    def stand(self):
        self.status = 'standing'
        self.is_jumpping = False
        if self.action_delay % EnemyConfig.max_walking_action_delay == 0:
            self.dir *= -1
            self.dx *= -1
        self.action_delay += 1
    
    def walk(self):
        if not self.collided_brick:
            return self.fall()
        elif self.correct_falling_pos():
            pass
        else:
            self.status = 'walking'
            self.is_jumpping = False
            self.move_to_x()
        self.action_delay += 1

    def jump(self):
        initial_jump = self.action_delay < EnemyConfig.max_jumping_action_delay
        if not self.collided_brick or initial_jump:
            self.status = 'jumping'
            self.is_jumpping = True
            self.dy = -EnemyConfig.y_speed
            self.move_to_y()
        elif self.correct_jumping_pos():
            pass
        else:
            self.action_delay = max(EnemyConfig.max_action_delay_list)
            # self.status = 'walking'
            self.is_jumpping = False
        self.action_delay += 1
    
    def correct_jumping_pos(self):
        collided_brick_top =  self.collided_brick.rect.top
        if self.rect.bottom >= collided_brick_top + 20:
            self.dy = -EnemyConfig.y_speed
            self.move_to_y()
            return True
        return False

    def fall(self):
        self.status = 'falling'
        self.is_jumpping = True
        self.dy = EnemyConfig.y_speed
        self.move_to_y()
        # self.action_delay += 1

    def correct_falling_pos(self):
        collided_brick_top =  self.collided_brick.rect.top
        if self.rect.bottom < collided_brick_top + EnemyConfig.brick_intersection:
            self.dy = EnemyConfig.y_speed
            self.move_to_y()
            return True
        return False

    def get_jump_condition(self):
        moved_pos = (self.pos[0], self.pos[1] - MapConfig.interval)
        pseudo_enemy = PseudoEnemy(moved_pos, self.image)
        if pygame.sprite.spritecollideany(pseudo_enemy, Map.group):
            return True
        return False

    def act_randomly(self):
        if brick := pygame.sprite.spritecollideany(self, Map.group):
            self.collided_brick = brick
        else:
            self.collided_brick = None
            
        self.max_action_delay = random.choice(EnemyConfig.max_action_delay_list)
        if self.action_delay < self.max_action_delay or self.is_jumpping:
            return self.prev_action()

        random_actions = [self.stand, self.walk, self.jump]
        if self.get_jump_condition():
            if self.stand_before and self.jump_before:
                weights = EnemyConfig.walking_weights
            elif self.stand_before:
                weights = EnemyConfig.walking_jumping_weights
            elif self.jump_before:
                weights = EnemyConfig.standing_walking_weights
            else:
                weights = EnemyConfig.standing_walking_jumping_weights
        else:
            if self.stand_before:
                weights = EnemyConfig.walking_weights
            else:
                weights = EnemyConfig.standing_walking_weights
        self.prev_action = random.choices(random_actions, weights=weights)[0]
        self.action_delay = 0
        self.stand_before = self.prev_action == self.stand
        self.jump_before = self.prev_action == self.jump
        return self.prev_action()


class PseudoEnemy(pygame.sprite.Sprite):

    def __init__(self, pos, image):
        super(PseudoEnemy,  self).__init__()
        self.pos = pos
        self.rect = image.get_rect(center=pos)