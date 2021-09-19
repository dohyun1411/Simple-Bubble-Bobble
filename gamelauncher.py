import os
import random

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
        self.new_round_delay = 0
        self.time = ScreenConfig.max_time
        self.time_color = ScreenConfig.time_color
        self.gameover = False
        self.initial_gameover_sound = True
        self.running = True
        self.restart = False
        self.blinking_delay = 0

        # load bgm
        self.bgm = pygame.mixer.music
        self.bgm.load(os.path.join(Loader.sound_path, 'main_theme.mp3'))
        self.bgm.set_volume(ScreenConfig.volume)

        # load sound effect
        self.sounds = Loader.load_sounds()
        for sound in self.sounds.values():
            sound.set_volume(ScreenConfig.volume)

        # load background image
        self.background_images = Loader.load_background_images()
        self.background_image = self.background_images[ScreenConfig.background_image]
        self.background_pos = ScreenConfig.background_pos

        # load map image
        self.map_image = Loader.load_brick_images()['brick']

        # create player
        Player.group.empty()
        DeadPlayer.group.empty()
        self.player_images = Loader.load_player_images()
        self.player = Player(self.player_images, self.sounds)
        
        # load enemy images
        Enemy.group.empty()
        Enemy.count = 0
        self.enemy_images = Loader.load_enemy_images()

        # load bubble images
        Bubble.group.empty()
        self.bubble_images = Loader.load_bubble_images()

        Boom.group.empty()
    
    def run(self): # TODO: make it depend on self.mode
        # play BGM
        self.bgm.play(-1)

        # event loop
        while self.running:
            self.clock.tick(ScreenConfig.fps)
            
            if not self.gameover and self.new_round_delay >= ScreenConfig.new_round_delay:
                self.time -= 1
            self.handle_event()

            if self.new_round:

                if not self.gameover:
                    self.time = ScreenConfig.max_time

                 # create map
                Map.group.empty()
                Map(self.map_image)

                # create enemy
                if self.mode == ScreenConfig.EASY or self.mode == ScreenConfig.HARD: # TODO: EASY와 HARD 분리
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
            
            # time warning
            if self.time == ScreenConfig.warning_time:
                self.sounds['hurry'].set_volume(1)
                self.sounds['hurry'].play()

            # game over
            self.gameover = self.player.life <= 0 or self.time <= 0
            if self.initial_gameover_sound and self.gameover:
                self.player.life = 0
                if self.time <= 0:
                    self.player.sounds['damaged'].play()
                    Boom(self.player.images['boom'], self.player.pos)
                    DeadPlayer(self.player.images['dead'], self.player.dir, self.player.pos)
                self.bgm.stop()
                self.sounds['gameover'].play()
                self.initial_gameover_sound = False
            if self.restart:
                self.running = False

            self.draw()
        
        # self.quit()
            
    def handle_event(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT: # quit
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # quit
                    self.running = False
                
                elif event.key == pygame.K_r and self.gameover: # restart
                    self.restart = True

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
        
        if self.time <= ScreenConfig.warning_time:
            self.time_color = ScreenConfig.RED
        else:
            self.time_color = ScreenConfig.WHITE

        # text time
        time_font = pygame.font.SysFont(ScreenConfig.time_font, ScreenConfig.time_size)
        time_text = time_font.render(f"TIME {self.time // ScreenConfig.fps}", True, self.time_color)
        time_rect = time_text.get_rect(center=ScreenConfig.time_pos)
        self.screen.blit(time_text, time_rect)

        # text round
        round_font = pygame.font.SysFont(ScreenConfig.round_font, ScreenConfig.round_size)
        round_text = round_font.render(f"ROUND {self.round}", True, ScreenConfig.round_color)
        round_rect = round_text.get_rect(center=ScreenConfig.round_pos)
        self.screen.blit(round_text, round_rect)

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

        if self.gameover:
            # text gameover
            gameover_font = pygame.font.SysFont(ScreenConfig.gameover_font, ScreenConfig.gameover_size)
            gameover_text = gameover_font.render("GAME OVER", True, ScreenConfig.gameover_color)
            gameover_rect = gameover_text.get_rect(center=ScreenConfig.gameover_pos)
            self.screen.blit(gameover_text, gameover_rect)

            # test info
            info_font = pygame.font.SysFont(ScreenConfig.info_font, ScreenConfig.info_size)
            info_text = info_font.render("PRESS R TO RESTART", True, ScreenConfig.info_color)
            info_rect = info_text.get_rect(center=ScreenConfig.info_pos)
            if self.blinking_delay in range(2 * ScreenConfig.max_blinking_delay // 3):
                self.screen.blit(info_text, info_rect)
            self.blinking_delay += 1
            self.blinking_delay %= ScreenConfig.max_blinking_delay

        pygame.display.update()

    def quit(self):
        pygame.quit()
    
    def start(self):
        self.sounds['init'].play()
        self.easy_color = ScreenConfig.RED
        self.hard_color = ScreenConfig.WHITE
        self.mode = ScreenConfig.EASY
        is_pressed = False
        blinking_delay = 0
        while self.running:
            self.clock.tick(ScreenConfig.fps)

            # draw background
            self.screen.fill(ScreenConfig.BLACK)

            # draw gamename
            self.screen.blit(self.background_images['gamename'], ScreenConfig.gamename_pos)

            # text level: easy
            easy_font = pygame.font.SysFont(ScreenConfig.easy_font, ScreenConfig.easy_size)
            easy_text = easy_font.render("EASY", True, self.easy_color)
            easy_rect = easy_text.get_rect(center=ScreenConfig.easy_pos)
            self.screen.blit(easy_text, easy_rect)     

            # text level: hard
            hard_font = pygame.font.SysFont(ScreenConfig.hard_font, ScreenConfig.hard_size)
            hard_text = hard_font.render("HARD", True, self.hard_color)
            hard_rect = hard_text.get_rect(center=ScreenConfig.hard_pos)
            self.screen.blit(hard_text, hard_rect)

            # text info
            info_font = pygame.font.SysFont(ScreenConfig.info_font, ScreenConfig.info_size)
            if is_pressed:
                info_text = info_font.render("PRESS SPACE TO START", True, ScreenConfig.info_color)
            else:
                info_text = info_font.render("PRESS LEFT/RIGHT TO SELECT LEVEL", True, ScreenConfig.info_color)
            info_rect = info_text.get_rect(center=ScreenConfig.info_pos)
            if blinking_delay in range(2 * ScreenConfig.max_blinking_delay // 3):
                self.screen.blit(info_text, info_rect)
            blinking_delay += 1
            blinking_delay %= ScreenConfig.max_blinking_delay          
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT: # quit
                    self.running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: # quit
                        self.running = False
                    
                    elif event.key == pygame.K_LEFT:
                        self.easy_color = ScreenConfig.RED
                        self.hard_color = ScreenConfig.WHITE
                        self.mode = ScreenConfig.EASY
                        is_pressed = True
                    
                    elif event.key == pygame.K_RIGHT:
                        self.easy_color = ScreenConfig.WHITE
                        self.hard_color = ScreenConfig.RED
                        self.mode = ScreenConfig.HARD
                        is_pressed = True
                    
                    elif event.key == pygame.K_SPACE:
                        self.load()
                        
            pygame.display.update()
    
    def load(self):
        self.sounds['init'].stop()
        self.sounds['loading'].play()
        loading = 0
        max_loading = ScreenConfig.loading_sound_time * ScreenConfig.fps
        player = Player(self.player_images, self.sounds)
        player.dx = 2
        player.pos = (player.pos[0] + 160, player.pos[1])
        while self.running:
            self.clock.tick(ScreenConfig.fps)

            if loading > max_loading:
                break
            player.walk()
            
            # player action
            # if stop - 20 < loading < stop + 20:
            #     player.stand()
            # else:
            #     if loading == turn:
            #         player.dx *= -1
            #     elif loading == int(0.58 * max_loading):
            #         player.dx *= -1
            #     player.walk()

            # draw background
            self.screen.fill(ScreenConfig.BLACK)

            # draw gamename
            self.screen.blit(self.background_images['gamename'], ScreenConfig.gamename_pos)

            # text level: easy
            easy_font = pygame.font.SysFont(ScreenConfig.easy_font, ScreenConfig.easy_size)
            easy_text = easy_font.render("EASY", True, self.easy_color)
            easy_rect = easy_text.get_rect(center=ScreenConfig.easy_pos)
            self.screen.blit(easy_text, easy_rect)     

            # text level: hard
            hard_font = pygame.font.SysFont(ScreenConfig.hard_font, ScreenConfig.hard_size)
            hard_text = hard_font.render("HARD", True, self.hard_color)
            hard_rect = hard_text.get_rect(center=ScreenConfig.hard_pos)
            self.screen.blit(hard_text, hard_rect)

            # draw player
            self.screen.blit(player.image, player.rect)
                        
            loading += 1

            for event in pygame.event.get():

                if event.type == pygame.QUIT: # quit
                    self.running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: # quit
                        self.running = False
                    
                    elif event.key == pygame.K_SPACE:
                        loading = max_loading

            pygame.display.update()

        Player.group.remove(player)
        self.sounds['loading'].stop()
        self.run()


if __name__ == '__main__':
    restart = True
    while restart:
        gl = GameLauncher()
        gl.start()
        restart = gl.restart
    gl.quit()