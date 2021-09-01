import pygame

from util import ImageLoader
from screen import ScreenConfig
from character import Direction, Character


class PlayerConfig:

    width = 40
    height = 50

    x_speed = 6
    y_speed = 20 # jumping speed
    gravity = 1

    life = 3


class Player(Character):

    def __init__(self, screen):
        super(Player, self).__init__(screen)

        self.images = ImageLoader.load_player_images()
        self.status = 'standing'

        self.dir = Direction.LEFT
        self.pos = (ScreenConfig.x_offset, ScreenConfig.height - ScreenConfig.y_offset)
 
        self.life = PlayerConfig.life

    @property
    def is_dead(self):
        return self.life == 0

    


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 720))
    pygame.display.set_caption('Simple Bubble Bobble')
    clock = pygame.time.Clock()
    
    p = Player(screen)
    print("None:", None==p.pos)

    running = True
    while running:
        clock.tick(60)
        screen.fill((255, 0, 255))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
    pygame.quit()