class ScreenConfig:

    width = 1200
    height = 720
    width_height = (width, height)
    x_offset = 36
    y_offset = 60

    fps = 60

    volume = 0.5

    new_round_delay = 120
    blinking_interval = 20

    background_image = 'night'
    background_pos = (0, 0)

    heart_pos = [(40 * i, 40) for i in range(1, 4)]

    WHITE = (255, 255, 255)
    round_font = 'comicsansms'
    round_size = 30
    round_color = WHITE
    round_pos = (width / 2, y_offset)