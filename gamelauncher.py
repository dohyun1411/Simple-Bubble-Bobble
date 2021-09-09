import os

import pygame

from config import *
from loader import Loader
from map import Map
from player import Player, DeadPlayer, Heart
from enemy import Enemy
from bubble import Bubble
from boom import Boom


class GameLauncher:

    def __init__(self):
        # initialize
        pygame.init()
        pygame.display.set_caption('Simple Bubble Bobble')

        self.screen = pygame.display.set_mode(ScreenConfig.width_height)
        self.clock = pygame.time.Clock()

        self.round = 1
        self.new_round = True
        self.gameover = False
        self.initial_gameover_sound = True
        self.running = True

        # load bgm
        self.bgm = pygame.mixer.music
        self.bgm.load(os.path.join(Loader.sound_path, 'main_theme.mp3'))
        self.bgm.set_volume(ScreenConfig.volume)

        # load sound effect
        self.sounds = Loader.load_sounds()
        for sound in self.sounds.values():
            sound.set_volume(ScreenConfig.volume)

        # load background image
        self.background_image = Loader.load_background_images()[ScreenConfig.background_image]
        self.background_pos = ScreenConfig.background_pos

        # load map image
        self.map_image = Loader.load_brick_images()['brick']

        # create player
        self.player_images = Loader.load_player_images()
        self.player = Player(self.player_images, self.sounds)
        
        # load enemy images
        self.enemy_images = Loader.load_enemy_images()

        # load bubble images
        self.bubble_images = Loader.load_bubble_images()
    
    def run(self):
        # play BGM
        self.bgm.play(-1)
        
        # event loop
        while self.running:
            self.clock.tick(ScreenConfig.fps)
            
            self.handle_event()

            if self.new_round:

                 # create map
                Map.group.empty()
                Map(self.map_image)

                # create enemy
                # if self.round - 1 < len(ScreenConfig.enemy_num_list):
                #     enemy_num = ScreenConfig.enemy_num_list[self.round - 1]
                # else:
                #     enemy_num += 10
                for _ in range(self.round):
                    enemy = Enemy(self.enemy_images, self.round)
                    enemy.new_round_delay = 0
                self.new_round = False

                self.new_round_delay = 0

            # create heart
            Heart.group.empty()
            for i in range(self.player.life):
                Heart(ScreenConfig.heart_pos[i], self.player_images['heart'])

            # player action
            self.player.move()
            self.player.new_round_delay = self.new_round_delay
            self.new_round_delay += 1

            # dead player action
            for dead_player in DeadPlayer.group:
                dead_player.fall()

            # enemy action
            for enemy in Enemy.group:
                enemy.act_randomly()
            
            # bubble action
            for bubble in Bubble.group:
                bubble.shoot()
            
            # boom action
            for boom in Boom.group:
                boom.act()
            
            # new round
            if Enemy.count == 0:
                self.new_round = True
                self.round += 1
            
            # game over
            self.gameover = self.player.life <= 0
            if self.initial_gameover_sound and self.gameover:
                self.bgm.stop()
                self.sounds['gameover'].play()
                self.initial_gameover_sound = False

            self.draw()

        # quit
        self.quit()
            
    def handle_event(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT: # quit
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # quit
                    self.running = False

                elif event.key == pygame.K_LEFT: # move left
                    self.player.dx_left = -PlayerConfig.x_speed

                elif event.key == pygame.K_RIGHT: # move right
                    self.player.dx_right = PlayerConfig.x_speed
                
                elif event.key == pygame.K_UP: # jump
                    if not self.player.is_jumpping:
                        self.player.dy = -PlayerConfig.y_speed
                        self.player.is_jumpping = True
                        self.sounds['jumping'].play()
                
                elif event.key == pygame.K_SPACE: # shoot bubble
                    if not self.new_round_delay < ScreenConfig.new_round_delay \
                        and not 0 < self.player.damaged_delay < ScreenConfig.new_round_delay:
                        self.player.shoot(self.bubble_images)
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT: # stop moving
                    self.player.dx_left = 0

                elif event.key == pygame.K_RIGHT: # stop moving
                    self.player.dx_right = 0

    def draw(self):
        # draw background
        self.screen.blit(self.background_image, self.background_pos)

        # draw map
        Map.group.draw(self.screen)

        # draw heart
        Heart.group.draw(self.screen)

        # text round
        round_font = pygame.font.SysFont(ScreenConfig.round_font, ScreenConfig.round_size)
        round_text = round_font.render(f"ROUND {self.round}", True, ScreenConfig.round_color)
        round_rect = round_text.get_rect(center=ScreenConfig.round_pos)
        self.screen.blit(round_text, round_rect)

        # text gameover
        if self.gameover:
            gameover_font = pygame.font.SysFont(ScreenConfig.gameover_font, ScreenConfig.gameover_size)
            gameover_text = gameover_font.render("GAME OVER", True, ScreenConfig.gameover_color)
            gameover_rect = gameover_text.get_rect(center=ScreenConfig.gameover_pos)
            self.screen.blit(gameover_text, gameover_rect)

        # draw enemy
        if self.new_round_delay < ScreenConfig.new_round_delay:
            if self.new_round_delay % ScreenConfig.blinking_interval in range(ScreenConfig.blinking_interval // 2):
                Enemy.group.draw(self.screen)
        else:
            Enemy.group.draw(self.screen)

        # draw dead player
        DeadPlayer.group.draw(self.screen)

        # draw player
        if self.new_round_delay < ScreenConfig.new_round_delay \
            or 0 < self.player.damaged_delay < ScreenConfig.new_round_delay:
            if self.new_round_delay % ScreenConfig.blinking_interval in range(ScreenConfig.blinking_interval // 2):
                Player.group.draw(self.screen)
        else:
            Player.group.draw(self.screen)
        
        # draw bubble
        Bubble.group.draw(self.screen)

        # draw boom
        Boom.group.draw(self.screen)

        pygame.display.update()

    def quit(self):
        pygame.quit()
    
    def set_initial_screen(self):
        pass


if __name__ == '__main__':
    gl = GameLauncher()
    gl.run()