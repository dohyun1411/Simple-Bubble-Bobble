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