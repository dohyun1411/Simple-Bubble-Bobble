import random

import pygame

from .config import *
from .map import MapConfig, Map
from .boom import Boom
from .character import Direction, Character


class Enemy(Character):

    group = pygame.sprite.Group()
    count = 0
    score = 0

    @staticmethod
    def is_all_flying():
        flying_enemy = 0
        for enemy in Enemy.group:
            if enemy.initial_flying == False:
                flying_enemy += 1
        return Enemy.count == flying_enemy

    def __init__(self, images, round):
        super(Enemy, self).__init__()

        self.images = images
        self.round = round

        # TODO: make id depends on round
        weights = EnemyConfig.weights
        self.id = random.choices(range(1, EnemyConfig.num_type + 1), weights)[0]

        if self.id == EnemyConfig.num_type:
            self.make_invincible()
        else:
            self.x_speed = random.randint(2 * self.id - 1, 2 * self.id)

        self.dir = random.choice([Direction.LEFT, Direction.RIGHT])
        self.dx = self.x_speed * self.dir
        self.dy = EnemyConfig.y_speed
        x = random.randint(ScreenConfig.x_offset, ScreenConfig.width - ScreenConfig.x_offset)
        y = ScreenConfig.x_offset
        self.pos = (x, y)
        
        self.collided_brick = None

        self.original_id = self.id
        # self.original_x_speed = self.x_speed
        self.time_being_invincible = 0
        self.invincible_before = False

        self.status = 'walking'
        self.prev_action = self.walk
        self.stand_before = False
        self.jump_before = False
        self.is_jumpping = False
        self.action_delay = 0
        self.new_round_delay = 0

        self.is_dead = False
        self.initial_flying = True

        Enemy.group.add(self)
        Enemy.count += 1

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
        self.original_image = self.images[self.name]
    
    @property
    def name(self):
        return EnemyConfig.name + str(self.id)
     
    def move_to_x(self):
        self.rect.x += self.dx
        if self.rect.left < 0:
            self.dir *= -1
            self.dx *= -1
        elif self.rect.right > ScreenConfig.width:
            self.dir *= -1
            self.dx *= -1
        self.rect = self.rect   

    def make_invincible(self):
        self.id = EnemyConfig.num_type
        self.dx = EnemyConfig.invincible_x_speed * self.dir
        self.time_being_invincible = 1
        self.invincible_before = True

    def stand(self):
        self.status = 'standing'
        self.is_jumpping = False
        if self.action_delay % EnemyConfig.max_walking_action_delay == 1:
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
        if len(pygame.sprite.spritecollide(pseudo_enemy, Map.group, False)) > 1:
            return True
        return False
    
    def set_collided_bricks(self):
        if brick := pygame.sprite.spritecollideany(self, Map.group):
            self.collided_brick = brick
        else:
            self.collided_brick = None
        
    def set_time_being_invincible(self):
        if self.time_being_invincible:
            self.time_being_invincible += 1
            if self.time_being_invincible > EnemyConfig.max_time_being_invincible:
                self.id = self.original_id
                self.dx = self.x_speed * self.dir
                self.time_being_invincible = 0

    def act_randomly(self):
        if self.is_dead:
            return self.fly()

        if self.new_round_delay < ScreenConfig.new_round_delay:
            self.new_round_delay += 1
            return
        
        self.set_collided_bricks()
        self.set_time_being_invincible()

        if self.invincible_before:
            self.invincible_before = False
            self.prev_action = self.walk
            return self.walk()
        
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
    
    def remove(self):
        self.is_dead = True
        Enemy.group.remove(self)

    def fly(self):
        if self.initial_flying:
            flying_x_speed = random.choice(EnemyConfig.flying_x_speed_range)
            self.dx = flying_x_speed * self.player_dir + self.player_dx
            self.dy = -EnemyConfig.flying_y_speed + self.player_dy / 4
            self.initial_flying = False
        else:
            self.dy += EnemyConfig.flying_gravity
        self.angle = (self.angle + EnemyConfig.flying_angular_speed) % 360
        self.move_to_x()
        self.move_to_y()
        if self.dy > 0 and pygame.sprite.spritecollideany(self, Map.group):
            Boom(self.images['boom'], self.pos)
            Enemy.group.remove(self)
            Enemy.count -= 1
            Enemy.score += EnemyConfig.scores[self.id - 1]


class PseudoEnemy(pygame.sprite.Sprite):

    def __init__(self, pos, image):
        super(PseudoEnemy,  self).__init__()
        self.pos = pos
        self.image = image
        self.rect = image.get_rect(center=pos)