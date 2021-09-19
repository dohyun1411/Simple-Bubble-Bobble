import pygame


class Direction:

    LEFT = -1
    RIGHT = 1


class Character(pygame.sprite.Sprite):

    def __init__(self):
        super(Character, self).__init__()
        self.angle = 0

    @property
    def flip(self):
        return True if self.dir == Direction.LEFT else False

    @property
    def image(self):
        image = pygame.transform.flip(self.original_image, self.flip, False)
        self._image = self.rotate_image(image, self.angle)
        return self._image
    
    def rotate_image(self, image, angle):
        return pygame.transform.rotozoom(image, angle, 1)

    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self._rect = self.image.get_rect(center=pos)
    
    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        self._rect = rect
        self.pos = rect.center
    
    @property
    def dx(self):
        return self._dx
    
    @dx.setter
    def dx(self, dx):
        self._dx = dx
        if dx > 0:
            self.dir = Direction.RIGHT
        elif dx < 0:
            self.dir = Direction.LEFT
    
    @property
    def dx_left(self):
        return self._dx_left
    
    @dx_left.setter
    def dx_left(self, dx_left):
        self._dx_left = dx_left
        try:
            self.dx = dx_left + self.dx_right
        except AttributeError:
            self.dx = dx_left
    
    @property
    def dx_right(self):
        return self._dx_right
    
    @dx_right.setter
    def dx_right(self, dx_right):
        self._dx_right = dx_right
        try:
            self.dx = self.dx_left + dx_right
        except AttributeError:
            self.dx = dx_right
    
    def move_to_y(self):
        self.rect.y += self.dy
        self.rect = self.rect