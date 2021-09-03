import pygame

from screen import ScreenConfig
from map import BrickConfig, Map
from character import Direction, Character
from enemy import Enemy
from bubble import Bubble


class PlayerConfig:

    x_speed = 6
    y_speed = 20 # jumping speed
    gravity = 1

    life = 3

    max_walking_image_delay = 4 # delay for walking image
    max_shooting_image_delay = 8 # delay for shooting image
    
    brick_intersection = 4 # intersection between player and collided brick


class Player(Character):

    group = pygame.sprite.Group()

    def __init__(self, images, sounds):
        super(Player, self).__init__()

        self.images = images
        self.sounds = sounds
        self.status = 'standing'

        self.dir = Direction.RIGHT
        self.dx_left = 0
        self.dx_right = 0
        self.dy = 0
        self.pos = (ScreenConfig.x_offset, ScreenConfig.height - ScreenConfig.y_offset)

        self.life = PlayerConfig.life
        
        self.collided_bricks = None

        self.is_standing = True
        self.is_jumpping = False
        self.walking_image_delay = 0
        self.shooting_image_delay = 0

        self.new_round_delay = 0

        Player.group.add(self)
        
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status):
        self._status = status
        self.original_image = self.images[status]

    def move_to_x(self):
        self.rect.x += self.dx
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > ScreenConfig.width:
            self.rect.right = ScreenConfig.width
        self.rect = self.rect

    def stand(self):
        if not self.is_jumpping and self.shooting_image_delay == 0:
            self.status = 'standing'
    
    def walk(self):
        if not self.is_jumpping and self.shooting_image_delay == 0:
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
            
            if self.shooting_image_delay == 0:
                self.status = 'jumping'
            self.is_jumpping = True
        else:
            return self.fall()
    
    def fall(self):
        self.move_to_y()
        self.dy += PlayerConfig.gravity
        if self.collided_bricks:
            self.correct_pos()
        else:
            if self.shooting_image_delay == 0:
                self.status = 'falling'
            self.is_jumpping = True
    
    def correct_pos(self):
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
            if self.rect.bottom > collided_brick_top + PlayerConfig.brick_intersection:
                self.rect.bottom = collided_brick_top + PlayerConfig.brick_intersection
                self.rect = self.rect

    def move(self):
        player_brick = pygame.sprite.groupcollide(Player.group, Map.group, False, False)
        if player_brick:
            self.collided_bricks = player_brick[self]
        else:
            self.collided_bricks = None

        if self.shooting_image_delay:
            self.shooting_image_delay += 1
            if self.shooting_image_delay == PlayerConfig.max_shooting_image_delay:
                self.shooting_image_delay = 0

        if self.dx:
            self.is_standing = False
            self.walk()
        else:
            self.is_standing = True
            self.stand()

        if self.is_jumpping:
            self.jump()
        else:
            self.fall()
        
        self.check_bubble_collision()
        if self.new_round_delay < ScreenConfig.new_round_delay:
            self.new_round_delay += 1
        else:
            self.check_enemy_collision()
        
    def shoot(self, bubble_images):
        if self.dir == Direction.LEFT:
            x = self.rect.left
        else:
            x = self.rect.right
        y = self.pos[1]
        speed = 0 if self.is_standing else PlayerConfig.x_speed
        Bubble(bubble_images, self.sounds, self.dir, (x, y), speed)
        self.status = 'shooting'
        self.shooting_image_delay = 1
    
    def check_bubble_collision(self):
        player_bubble = pygame.sprite.groupcollide(Player.group, Bubble.group, False, False)
        if player_bubble:
            for bubble in player_bubble[self]:
                if isinstance(bubble, Bubble) and not bubble.is_shooting:
                    bubble.player_dir = self.dir
                    bubble.player_dx = self.dx
                    bubble.remove()
    
    def check_enemy_collision(self):
        if pygame.sprite.spritecollideany(self, Enemy.group):
            self.life -= 1
            if self.life > 0:
                self.new_round_delay = 0


class Heart(pygame.sprite.Sprite):

    group = pygame.sprite.Group()

    def __init__(self, pos, image):
        super(Heart, self).__init__()
        self.pos = pos
        self.image = image
        self.rect = image.get_rect(center=pos)
        Heart.group.add(self)