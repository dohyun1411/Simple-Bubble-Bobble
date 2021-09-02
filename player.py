import pygame

from util import Loader
from screen import ScreenConfig
from character import Direction, Character


class PlayerConfig:

    width = 40
    height = 50

    x_speed = 6
    y_speed = 20 # jumping speed
    gravity = 1

    life = 3

    # delay for walking image
    max_walking_image_delay = 4


class Player(Character):

    def __init__(self, screen, map_):
        super(Player, self).__init__(screen, map_)

        self.images = Loader.load_player_images()
        self.status = 'standing'

        self.dx_left = 0
        self.dx_right = 0
        # self.dy = 0
        self.pos = (ScreenConfig.x_offset, ScreenConfig.height - ScreenConfig.y_offset)

        self.life = PlayerConfig.life

        self.walking_image_delay = 0

    @property
    def is_dead(self):
        return self.life == 0

    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self._rect = self.image.get_rect(center=pos)
        # self.set_correct_pos()

    # TODO
    def set_correct_pos(self):
        if self.status != 'landing':
            if self.rect.bottom != self.collided_brick.rect.top + 5:
                self.rect.bottom = self.collided_brick.rect.top + 5
            self.rect = self.rect
    
    def stand(self):
        self.status = 'standing'
    
    def walk(self):
        if self.walking_image_delay == 0:
            if self.status == 'standing':
                self.status = 'walking'
            elif self.status == 'walking':
                self.status = 'standing'
            else:
                print("WHILE WALKING status:", self.status)
        self.walking_image_delay += 1
        self.walking_image_delay %= PlayerConfig.max_walking_image_delay

        self.move_to_x()

    def jump(self):
        self.move_to_y()
        if self.dy < 0:
            self.status = 'jumping'
            return True # player is jumping
        else:
            return self.land()
    
    def land(self):
        self.status = 'landing'
        if brick := pygame.sprite.spritecollideany(self, self.map_):
            self.collided_brick = brick
            return False # landing finished
        return True # player is landing
    
    def shoot(self):
        self.status = 'shooting'
    

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Simple Bubble Bobble')
    screen = pygame.display.set_mode((1200, 720))
    clock = pygame.time.Clock()
    
    p = Player(screen, '')

    running = True
    i = 0
    while running:
        clock.tick(60)
        screen.fill((255, 0, 255))
        if i % 100 == 0:
            print('POS', p.pos)
            print('RECT', p.rect)
        p.draw()
        i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    p.dx = PlayerConfig.x_speed
            elif event.type == pygame.KEYUP:
                p.dx = 0
        # print("DX:", p.dx)
        p.walk()
        
        pygame.display.update()
    pygame.quit()