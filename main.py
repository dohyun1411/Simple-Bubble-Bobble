import os

import pygame
from pygame.constants import SCALED

from util import Loader
from screen import ScreenConfig
from map import Map
from player import Player, PlayerConfig
from enemy import Enemy


class Main:

    def __init__(self):
        # initialize
        pygame.init()
        pygame.display.set_caption('Simple Bubble Bobble')

        self.screen = pygame.display.set_mode(ScreenConfig.width_height)
        self.clock = pygame.time.Clock()

        self.round = 0
        self.running = True

        # load bgm
        self.bgm = pygame.mixer.music
        self.bgm.load(os.path.join(Loader.sound_path, 'main_theme.mp3'))
        self.bgm.set_volume(ScreenConfig.volume)

        # load sound effect
        self.sounds = Loader.load_sounds()
        for sound in self.sounds.values():
            sound.set_volume(ScreenConfig.volume)

        # create background
        self.background_image = Loader.load_background_images()[ScreenConfig.background_image]
        self.background_pos = ScreenConfig.background_pos

        # create map
        brick_image = Loader.load_brick_images()['brick']
        _ = Map(brick_image)

        # create Player
        player_images = Loader.load_player_images()
        self.player = Player(player_images)

        # create enemy
        enemy_images = Loader.load_enemy_images()
        _ = Enemy(enemy_images, self.round)
    
    def run(self):
        # play BGM
        self.bgm.play(-1)
        
        # event loop
        while self.running:
            self.clock.tick(ScreenConfig.fps)
            
            # handle event
            self.handle_event()

            # player moving
            self.player.move()
            
            # draw
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
                
                elif event.key == pygame.K_UP:
                    if not self.player.is_jumpping:
                        self.player.dy = -PlayerConfig.y_speed # jump
                        self.player.is_jumpping = True
                        self.sounds['jumping'].play()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.dx_left = 0 # stop moving

                elif event.key == pygame.K_RIGHT:
                    self.player.dx_right = 0 # stop moving

    def draw(self):
        # draw background
        self.screen.blit(self.background_image, self.background_pos)

        # draw map
        Map.group.draw(self.screen)

        # text round
        round_font = pygame.font.SysFont(ScreenConfig.round_font, ScreenConfig.round_size)
        round_text = round_font.render(f"ROUND {self.round}", True, ScreenConfig.round_color)
        round_rect = round_text.get_rect(center=ScreenConfig.round_pos)
        self.screen.blit(round_text, round_rect)

        # draw player
        Player.group.draw(self.screen)

        # draw enemy
        Enemy.group.draw(self.screen)

        pygame.display.update()

    def quit(self):
        pygame.quit()
    

if __name__ == '__main__':
    main = Main()
    main.run()