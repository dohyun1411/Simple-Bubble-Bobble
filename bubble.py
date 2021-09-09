import random

import pygame

from config import *
from map import Map
from boom import Boom
from character import Direction, Character
from enemy import Enemy


class Bubble(Character):

    group = pygame.sprite.Group()
    
    def __init__(self, images, sounds, dir, pos, speed):
        super(Bubble, self).__init__()

        self.images = images
        self.sounds = sounds
        self.status = 'normal'

        self.dir = dir
        self.dx = (BubbleConfig.max_x_speed + speed) * dir
        self.dy = -BubbleConfig.y_speed
        self.pos = pos

        self.is_shooting = True
        self.angular_dir = random.choice([Direction.LEFT, Direction.RIGHT])
        self.initial_dir = 0
    
        self.enemy = None
        self.player_dir = None

        sounds['shooting'].play()

        Bubble.group.add(self)

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status):
        self._status = status
        self.original_image = self.images[status]

    @property
    def dx(self):
        return self._dx
    
    @dx.setter
    def dx(self, dx):
        self._dx = dx

    @property
    def enemy(self):
        return self._enemy
    
    @enemy.setter
    def enemy(self, enemy):
        if enemy:
            self._enemy = enemy
            self.status = enemy.name
            self.dir = enemy.dir
            self.pos = enemy.pos
            self.dx = 0
            enemy.remove()
        else:
            self._enemy = None

    def move_to_x(self):
        self.rect.x += self.dx
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx = 0
        elif self.rect.right > ScreenConfig.width:
            self.rect.right = ScreenConfig.width
            self.dx = 0
        self.rect = self.rect
    
    def move_to_x_while_jumping(self):
        self.rect.x += self.dx
        if self.rect.left < 0:
            self.dx *= -1
        elif self.rect.right > ScreenConfig.width:
            self.dx *= -1
        self.rect = self.rect

    def jump(self):
        brick = pygame.sprite.spritecollideany(self, Map.group)
        if brick and abs(self.rect.top - brick.rect.top) > abs(self.rect.top - brick.rect.bottom):
            if not self.initial_dir:
                self.initial_dir = (self.angle < 0) * 2 - 1
                self.dx = self.initial_dir * BubbleConfig.x_speed
            self.move_to_x_while_jumping()
        else:
            self.move_to_y()

        if self.rect.top < 0:
            self.remove(revival=True)
    
    def remove(self, revival=False):
        Boom(self.images['boom'], self.pos)
        if self.enemy:
            self.enemy.pos = self.pos
            if self.player_dir:
                self.enemy.player_dir = self.player_dir
                self.enemy.player_dx = self.player_dx
                self.enemy.player_dy = self.player_dy
            if revival:
                self.enemy.is_dead = False
                self.enemy.make_invincible()
            else:
                self.sounds['bubble_kill'].play()
            Enemy.group.add(self.enemy)
        Bubble.group.remove(self)

    def collide_with_enemy(self):
        if self.status != 'normal' or not self.is_shooting:
            return None
        if enemy := pygame.sprite.spritecollideany(self, Enemy.group):
            if enemy.id != EnemyConfig.num_type and not enemy.is_dead:
                return enemy
        return None

    def shoot(self):
        if enemy := self.collide_with_enemy():
            self.enemy = enemy
            self.is_shooting = False
        if self.is_shooting:
            self.dx -= BubbleConfig.x_acc * self.dir
            self.move_to_x()
            if self.dx == 0:
                self.is_shooting = False
        else:
            self.angle += BubbleConfig.angular_speed * self.angular_dir
            if abs(self.angle) > 20:
                self.angular_dir *= -1
            self.jump()