import pygame


class Direction:
    LEFT = -1
    RIGHT = 1


class Character(pygame.sprite.Sprite):

    def __init__(self, screen):
        super(Character, self).__init__()
        self.screen = screen

    @property
    def flip(self):
        return True if self.dir == Direction.LEFT else False

    @property
    def image(self):
        self._image = pygame.transform.flip(self.original_image, self.flip, False)
        return self._image

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status):
        self._status = status
        self.original_image = self.images[status]

    # @property
    # def pos(self):
    #     return self._pos
    
    # @pos.setter
    # def pos(self, pos):
    #     self._pos = pos
    #     self._rect = self.image.get_rect(center=pos)
    
    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        self._rect = rect
        self.pos = rect.center
    
    def move_to_x(self, dx):
        self.rect.x += dx
    
    def move_to_y(self, dy):
        self.rect.y += dy

    def draw(self):
        self.screen.blit(self.image, self.rect)