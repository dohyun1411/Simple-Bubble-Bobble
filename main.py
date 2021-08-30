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
    'ghost': pygame.image.load(os.path.join(player_img_path, "ghost.png")).convert_alpha(),
    'boom': pygame.image.load(os.path.join(player_img_path, "boom.png")).convert_alpha(),
}
bubble_imgs = {
    'bubble': pygame.image.load(os.path.join(player_img_path, "bubble.png")).convert_alpha(),
    'reaper': pygame.image.load(os.path.join(player_img_path, "reaper_in_bubble.png")).convert_alpha(),
    'reaper3': pygame.image.load(os.path.join(player_img_path, "reaper3_in_bubble.png")).convert_alpha(),
    'reaper4': pygame.image.load(os.path.join(player_img_path, "reaper4_in_bubble.png")).convert_alpha(),
    'boom': pygame.image.load(os.path.join(player_img_path, "boom.png")).convert_alpha()
}

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
background = pygame.image.load(os.path.join(background_img_path, "night.png")).convert_alpha()

# Load map images
map_img_path = os.path.join(cur_path, 'images/map')
map_imgs = {
    'brown': pygame.image.load(os.path.join(map_img_path, "brick.png")).convert_alpha()
}

sound_path = os.path.join(cur_path, 'sounds')
pygame.mixer.music.load(os.path.join(sound_path, 'main_theme.mp3'))
pygame.mixer.music.play(-1)
jump_sound = pygame.mixer.Sound(os.path.join(sound_path, 'jump.mp3'))
bubble_sound = pygame.mixer.Sound(os.path.join(sound_path, 'bubble.mp3'))
bubble_kill_sound = pygame.mixer.Sound(os.path.join(sound_path, 'bubble_kill.mp3'))

# Create a Player
player = Player(images=player_imgs, screen_info=screen_info)

# Create bubble group
bubble_group = pygame.sprite.Group()

# Create enemy group
enemy_group = pygame.sprite.Group()
enemy_list = []

# Create a map
map_img = random.choice(list(map_imgs.values()))
map, brick_dict = create_map(map_img)

# Event Loop
running = True
game_over = False
round = 0
new_round = True
bubble_delay = 0
new_round_delay = 0
attack_delay = 0
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
                jump_sound.play()
                is_jumpping = True # Jump
                player_dy = player_jumping_speed
            elif event.key == pygame.K_SPACE:
                bubble_sound.play()
                player.shoot()
                if player.dir == RIGHT:
                    bubble_pos = (player.get_rect().right, player.get_pos()[1])
                else:
                    bubble_pos = (player.get_rect().left, player.get_pos()[1])

                bubble_group.add(Bubble(images=bubble_imgs, pos=bubble_pos, dir=player.dir, group=bubble_group, screen=screen))
                

        elif event.type == pygame.KEYUP: # keyboard up
            if event.key == pygame.K_LEFT:
                player_dx_left = 0 # Stop moving
            elif event.key == pygame.K_RIGHT:
                player_dx_right = 0
    
    # Draw background
    screen.blit(background, (0, 0))
    round_font = pygame.font.SysFont('comicsansms', 30)
    txt_round = round_font.render(f"ROUND {round}", True, WHITE)
    rect_round = txt_round.get_rect(center=(int(screen_width / 2), 60))
    screen.blit(txt_round, rect_round)

    # Draw map
    map.draw(screen)

    # Player
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
        if new_round_delay == 0:
            map, brick_dict = create_map(map_img)
            if round < 8:
                enemy_num = [1, 2, 3, 5, 7, 10, 15, 20][round]
            else:
                enemy_num = 20 + 10 * (round - 7)
            for _ in range(enemy_num):
                enemy = Enemy(images=enemy_imgs, map=map, group=enemy_group, list_=enemy_list)
                enemy_group.add(enemy)
                enemy_list.append(enemy)
            new_round = False
            round += 1
            attack_delay = 1
        new_round_delay += 1
        new_round_delay %= 20


    for enemy in enemy_group:
        enemy.act_randomly()
        enemy.set_correct_pos()
    enemy_group.draw(screen)

    # Draw bubble
    bubble_group.draw(screen)
    for bubble in bubble_group:
        bubble.shoot(map)

    bubble_enemy = pygame.sprite.groupcollide(bubble_group, enemy_group, False, False)
    for bubble, enemies in bubble_enemy.items():
        enemy = enemies[0]
        if enemy.type != 'reaper2' and bubble.power and bubble_delay == 0:
            enemy.remove()
            bubble.attack(enemy)
            bubble_delay += 1
    bubble_delay = bubble_delay + 1 if bubble_delay else 0
    if bubble_delay > 6:
        bubble_delay = 0

    if bubble := pygame.sprite.spritecollideany(player, bubble_group):
        bubble_kill_sound.play()
        bubble.remove()
    
    if pygame.sprite.spritecollideany(player, enemy_group) or game_over:
        if (attack_delay and attack_delay > 120) or game_over:
            attack_delay = 0
            player.dead(screen)
            game_font = pygame.font.SysFont('aladinregular', 60)
            txt_game_over = game_font.render("GAME OVER", True, WHITE)
            rect_game_over = txt_game_over.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
            screen.blit(txt_game_over, rect_game_over)
            # running = False
            game_over = True
    
    if attack_delay:
        attack_delay += 1

    if not enemy_list:
        new_round = True
        
    # Draw player
    if not game_over:
        player.draw(screen)
    
    pygame.display.update()

pygame.quit()    