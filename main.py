import os
import math
import random
import pygame

from map import *
from player import *
from enemy import *
from config import *


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
bubble_img = pygame.image.load(os.path.join(player_img_path, "ghost_in_bubble.png")).convert_alpha()

# Load emeny images
enemy_img_path = os.path.join(cur_path, 'images/enemy')
enemy_imgs = {
    'reaper': pygame.image.load(os.path.join(enemy_img_path, 'reaper.png')).convert_alpha(),
    'reaper2': pygame.image.load(os.path.join(enemy_img_path, 'reaper2.png')).convert_alpha(), # dangerous
    'reaper3': pygame.image.load(os.path.join(enemy_img_path, 'reaper3.png')).convert_alpha(),
    'reaper4': pygame.image.load(os.path.join(enemy_img_path, 'reaper4.png')).convert_alpha()
}

# Load background images
background_img_path = os.path.join(cur_path, 'images/background')
background = pygame.image.load(os.path.join(background_img_path, "night.png"))

# Load map images
map_img_path = os.path.join(cur_path, 'images/map')
map_imgs = {
    'brown': pygame.image.load(os.path.join(map_img_path, "brick.png")).convert_alpha()
}

# Create a Player
player = Player(images=player_imgs, screen_info=screen_info)

# Create bubble group
bubble_group = pygame.sprite.Group()

# Create enemy group
enemy_group = pygame.sprite.Group()

# Create a map
map_img = random.choice(list(map_imgs.values()))
map, brick_dict = create_map(map_img)

# Event Loop
running = True
round = 20
new_round = True
while running:
    clock.tick(fps) # FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # quit
            running = False

        elif event.type == pygame.KEYDOWN: # keyboard down
            if event.key == pygame.K_LEFT: # left key
                player_dir = LEFT # Set direction to left
                player_dx_left -= player_speed # Move to left
            elif event.key == pygame.K_RIGHT: # right key
                player_dir = RIGHT # Set direction to right
                player_dx_right += player_speed # Move to right
            elif event.key == pygame.K_UP and not is_jumpping: # up key
                is_jumpping = True # Jump
                player_dy = player_jumping_speed
            elif event.key == pygame.K_SPACE:
                player.shoot()
                if player.dir == RIGHT:
                    bubble_pos = (player.get_rect().right, player.get_pos()[1])
                else:
                    bubble_pos = (player.get_rect().left, player.get_pos()[1])

                bubble_group.add(Bubble(image=bubble_img, pos=bubble_pos, dir=player.dir, group=bubble_group))


        elif event.type == pygame.KEYUP: # keyboard up
            if event.key == pygame.K_LEFT:
                player_dx_left = 0 # Stop moving
            elif event.key == pygame.K_RIGHT:
                player_dx_right = 0
    
    # Draw background
    screen.blit(background, (0, 0))

    # Draw map
    map.draw(screen)

    # Draw player
    player.draw(screen)

    player.set_dir(player_dir) # Set player direction

    if player_dx_left + player_dx_right: # player is walking
        player.walk(player_dx_left + player_dx_right)
    else: # player is standing
        player.stand()
    
    if is_jumpping: # player is jumping
        if player_dy >= 0:
            player.jump(player_dy)
        else:
            is_jumpping = not player.land(player_dy, map)
        player_dy -= gravity
    
    else:
        if brick := pygame.sprite.spritecollideany(player, map):
            player.collided_brick = brick
            player_dy = -gravity
        else:
            player.land(player_dy, map)
            player_dy -= gravity
        player.set_correct_pos()
    
    # Draw enemy
    if new_round:
        for _ in range(round):
            enemy = Enemy(images=enemy_imgs, screen_info=screen_info, map=map)
            enemy_group.add(enemy)
        new_round = False

    for enemy in enemy_group:
        enemy.act_randomly()
        enemy.set_correct_pos()
        # enemy.draw(screen)
    enemy_group.draw(screen)

    # Draw bubble
    bubble_group.draw(screen)
    for bubble in bubble_group:
        bubble.shoot(map)



    
    pygame.display.update()


pygame.quit()    