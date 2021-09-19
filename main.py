import argparse

from bubble_bobble.gamelauncher import GameLauncher


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--heart", type=int, default=3)
    parser.add_argument("-f", "--fast", action="store_true")
    args = parser.parse_args()

    restart = True
    while restart:
        gl = GameLauncher()
        if args.fast:
            gl.run()
        else:
            gl.start()
        restart = gl.restart
    gl.quit()