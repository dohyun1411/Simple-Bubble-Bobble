import os

import pygame


class Loader:

    cur_path = os.path.dirname(__file__)
    image_path = os.path.join(cur_path, 'images')
    sound_path = os.path.join(cur_path, 'sounds')

    @staticmethod
    def load_background_images():
        print("LOAD BACKGROUND IMAGES")
        background_image_path = os.path.join(Loader.image_path, 'background')
        background_images = {
            'night': pygame.image.load(os.path.join(background_image_path, "night.png")).convert_alpha()
        }
        return background_images
    
    @staticmethod
    def load_brick_images():
        print("LOAD BRICK IMAGES")
        brick_image_path = os.path.join(Loader.image_path, 'map')
        brick_images = {
            'brick': pygame.image.load(os.path.join(brick_image_path, "brick.png")).convert_alpha()
        }
        return brick_images
    
    @staticmethod
    def load_player_images():
        print("LOAD PLAYER IMAGES")
        player_image_path = os.path.join(Loader.image_path, 'player')
        player_images = {
            'standing': pygame.image.load(os.path.join(player_image_path, "standing.png")).convert_alpha(),
            'walking': pygame.image.load(os.path.join(player_image_path, "walking.png")).convert_alpha(),
            'jumping': pygame.image.load(os.path.join(player_image_path, "jumping.png")).convert_alpha(),
            'landing': pygame.image.load(os.path.join(player_image_path, "landing.png")).convert_alpha(),
            'shooting': pygame.image.load(os.path.join(player_image_path, "shooting.png")).convert_alpha(),
            'dead': pygame.image.load(os.path.join(player_image_path, "dead.png")).convert_alpha(),
            'ghost': pygame.image.load(os.path.join(player_image_path, "ghost.png")).convert_alpha()
        }
        return player_images
    
    @staticmethod
    def load_sounds():
        print("LOAD SOUNDS")
        player_sounds = {
            'jumping': pygame.mixer.Sound(os.path.join(Loader.sound_path, 'jump.mp3')),
            'shooting': pygame.mixer.Sound(os.path.join(Loader.sound_path, 'bubble.mp3')),
            'damaged': pygame.mixer.Sound(os.path.join(Loader.sound_path, 'player_damaged.mp3')),
            
        }
        return player_sounds
    
    @staticmethod
    def load_enemy_images():
        print("LOAD ENEMY IMAGES")
        enemy_image_path = os.path.join(Loader.image_path, 'enemy')
        enemy_images = {
            'reaper1': pygame.image.load(os.path.join(enemy_image_path, 'reaper.png')).convert_alpha(),
            'reaper2': pygame.image.load(os.path.join(enemy_image_path, 'reaper2.png')).convert_alpha(), # dangerous
            'reaper3': pygame.image.load(os.path.join(enemy_image_path, 'reaper3.png')).convert_alpha(),
            'reaper4': pygame.image.load(os.path.join(enemy_image_path, 'reaper4.png')).convert_alpha()
        }
        return enemy_images