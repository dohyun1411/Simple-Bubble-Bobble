class ScreenConfig:

    width = 1200
    height = 720
    width_height = (width, height)
    x_offset = 36
    y_offset = 60

    fps = 60

    volume = 0.5

    enemy_num_list = [1, 2, 3, 5, 7, 10, 15, 20]
    new_round_delay = 120
    player_damaged_delay = 120
    blinking_interval = 20

    background_image = 'night'
    background_pos = (0, 0)

    num_heart = 3
    heart_pos = [(50 * i, 50) for i in range(1, num_heart + 1)]

    WHITE = (255, 255, 255)
    round_font = 'comicsansms'
    round_size = 30
    round_color = WHITE
    round_pos = (width / 2, y_offset)

    gameover_font = 'aladinregular'
    gameover_size = 60
    gameover_color = WHITE
    gameover_pos =(width / 2, height / 2)


class BrickConfig:
    
    size = 40


class PlayerConfig:

    x_speed = 6
    y_speed = 20 # jumping speed
    gravity = 1

    life = ScreenConfig.num_heart

    max_walking_image_delay = 4 # delay for walking image
    max_shooting_image_delay = 8 # delay for shooting image
    
    brick_intersection = 4 # intersection between player and collided brick
    dead_brick_intersection = 20


class EnemyConfig:
    
    name = 'reaper'
    num_type = 4

    max_time_being_invincible = 700
    max_walking_action_delay = 16
    max_action_delay_list_coef = [3, 6, 12, 15]
    max_action_delay_list = [c * 16 for c in max_action_delay_list_coef] # 16 = max_walking_action_delay
    max_jumping_action_delay = 20

    brick_intersection = 20

    y_speed = 2
    invincible_x_speed = 1 # x speed for invincible enemy

    flying_x_speed_range = range(1, 1 + 6) # 6 is player x_speed
    flying_y_speed = 20
    flying_gravity = 0.5
    flying_angular_speed = 20

    walking_weights = [0., 1., 0.]
    walking_jumping_weights = [0., 0.5, 0.5]
    standing_walking_weights = [0.4, 0.6, 0.]
    standing_walking_jumping_weights = [0.3, 0.3, 0.4]


class BubbleConfig:

    max_x_speed = 12 # shooting speed
    x_acc = 1
    x_speed = 1
    y_speed = 1
    angular_speed = 1
    max_angle = 20


class BoomConfig:

    delay = 6