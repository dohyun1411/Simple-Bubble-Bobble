import os

import pygame

from util import Loader
from screen import ScreenConfig
from map import Map
from player import Player, PlayerConfig


class Main:

    def __init__(self):

        # initialize
        pygame.init()
        pygame.display.set_caption('Simple Bubble Bobble')

        self.screen = pygame.display.set_mode(ScreenConfig.width_height)
        self.clock = pygame.time.Clock()
        self.volume = ScreenConfig.volume

        # create a map
        map_ = Map()
        self.map = map_.brick_group

        # create a Player
        self.player = Player(self.screen, self.map)

        self.round = 0
        self.running = True
    
    def run(self):

        # play BGM
        bgm = pygame.mixer.music
        bgm.load(os.path.join(Loader.sound_path, 'main_theme.mp3'))
        bgm.set_volume(self.volume)
        bgm.play(-1)

        # event handler
        while self.running:
            self.clock.tick(ScreenConfig.fps)

            self.handle_event()

            # player
            if self.player.dx:
                self.player.walk()
            else:
                self.player.stand()
            
            self.draw()

        # quit
        self.quit()
            
    def handle_event(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False # quit
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False # quit

                elif event.key == pygame.K_LEFT:
                    self.player.dx_left = -PlayerConfig.x_speed # move left

                elif event.key == pygame.K_RIGHT:
                    self.player.dx_right = PlayerConfig.x_speed # move right
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.dx_left = 0 # stop moving
                elif event.key == pygame.K_RIGHT:
                    self.player.dx_right = 0 # stop moving

    def draw(self):

        # draw background
        background_image = Loader.load_background_images()[ScreenConfig.background_image]
        background_pos = ScreenConfig.background_pos
        self.screen.blit(background_image, background_pos)

        # draw map
        self.map.draw(self.screen)

        # text round
        round_font = pygame.font.SysFont(ScreenConfig.round_font, ScreenConfig.round_size)
        round_text = round_font.render(f"ROUND {self.round}", True, ScreenConfig.round_color)
        round_rect = round_text.get_rect(center=ScreenConfig.round_pos)
        self.screen.blit(round_text, round_rect)

        self.player.draw()

        pygame.display.update()

    def quit(self):
        pygame.quit()
    

if __name__ == '__main__':
    main = Main()
    main.run()