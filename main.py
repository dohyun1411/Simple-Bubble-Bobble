from bubble_bobble.gamelauncher import GameLauncher


restart = True
while restart:
    gl = GameLauncher()
    gl.start()
    restart = gl.restart
gl.quit()