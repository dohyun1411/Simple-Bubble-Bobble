import os
import math
import random
import pygame

from player import *
from global_variables import *


# Initialize
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simple Bubble Bobble')
clock = pygame.time.Clock()

# Load player images
cur_path = os.path.dirname(__file__)
player_img_path = os.path.join(cur_path, 'images/player')
player_imgs = {
    'standing': pygame.image.load(os.path.join(player_img_path, "standing.png")).convert_alpha(),
    'walking': pygame.image.load(os.path.join(player_img_path, "walking.png")).convert_alpha(),
    'jumping': pygame.image.load(os.path.join(player_img_path, "jumping.png")).convert_alpha(),
    'landing': pygame.image.load(os.path.join(player_img_path, "landing.png")).convert_alpha(),
    'shooting': pygame.image.load(os.path.join(player_img_path, "shooting.png")).convert_alpha(),
    'dead': pygame.image.load(os.path.join(player_img_path, "dead.png")).convert_alpha(),
    'ghost': pygame.image.load(os.path.join(player_img_path, "ghost.png")).convert_alpha()
}

# Load background images
background_img_path = os.path.join(cur_path, 'images/background')
background_imgs = {
    'ground': pygame.image.load(os.path.join(background_img_path, "ground.png")),
    'night': pygame.image.load(os.path.join(background_img_path, "night.png")),
    'jungle': pygame.image.load(os.path.join(background_img_path, "jungle.png")),
    'ocean': pygame.image.load(os.path.join(background_img_path, "ocean.png")),
    'volcano': pygame.image.load(os.path.join(background_img_path, "volcano.png"))
}

# Create a Player
player = Player(images=player_imgs, screen_info=screen_info)

# background
normal_background_list = ['ground', 'night', 'jungle', 'ocean']
normal_background = background_imgs[random.choice(normal_background_list)]

# Event Loop
running = True
while running:
    clock.tick(30) # FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # quit
            running = False

        elif event.type == pygame.KEYDOWN: # keyboard down
            if event.key == pygame.K_LEFT: # left key
                player_dir = LEFT # Set direction to left
                player_dx -= player_speed # Move to left
            elif event.key == pygame.K_RIGHT: # right key
                player_dir = RIGHT # Set direction to right
                player_dx += player_speed # Move to right

        elif event.type == pygame.KEYUP: # keyboard up
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_dx = 0 # Stop moving
    
    # Draw background
    screen.blit(normal_background, (0, 0))

    # Draw player
    player.set_dir(player_dir) # Set player direction
    if player_dx: # player is walking
        player.walk(player_dx)
    else: # player is standing
        player.stand()
    player.draw(screen)

    pygame.display.update()

pygame.quit()    