import os

import pygame


class ImageLoader:

    cur_path = os.path.dirname(__file__)
    image_path = os.path.join(cur_path, 'images')

    @staticmethod
    def load_player_images():
        player_image_path = os.path.join(ImageLoader.image_path, 'player')
        player_images = {
            'standing': pygame.image.load(os.path.join(player_image_path, "standing.png")).convert_alpha(),
            'walking': pygame.image.load(os.path.join(player_image_path, "walking.png")).convert_alpha(),
            'jumping': pygame.image.load(os.path.join(player_image_path, "jumping.png")).convert_alpha(),
            'landing': pygame.image.load(os.path.join(player_image_path, "landing.png")).convert_alpha(),
            'shooting': pygame.image.load(os.path.join(player_image_path, "shooting.png")).convert_alpha(),
            'dead': pygame.image.load(os.path.join(player_image_path, "dead.png")).convert_alpha(),
            'ghost': pygame.image.load(os.path.join(player_image_path, "ghost.png")).convert_alpha(),
            'boom': pygame.image.load(os.path.join(player_image_path, "boom.png")).convert_alpha(),
        }
        return player_images