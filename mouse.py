
import pygame
from sprites import Generic
from constants import *


class Mouse:
    def __init__(self, soil_layer):
        self.pos = (0, 0)
        self.selectable = False
        self.soil_layer = soil_layer
        self.mouse_sprites = pygame.sprite.Group()
        self.tile = MouseTile(self.pos, self.selectable, self.mouse_sprites)

    def find_tile(self):
        collided_tile_pos = self.soil_layer.tile_collision(self.pos, ShapeTypes.POINT)
        # print(collided_tile_index)
        if collided_tile_pos:
            collided_tile_pos = collided_tile_pos[0][0], collided_tile_pos[0][1]
            self.tile.pos = collided_tile_pos
        # print(self.tile.pos)
        # change mousetile to change colors

    def update(self, offset):
        window_position = pygame.mouse.get_pos()
        self.pos = (window_position[0]+offset.x, window_position[1]+offset.y)
        self.find_tile()


class MouseTile(Generic):
    def __init__(self, pos, selectable, mouse_sprites):
        self.pos = pos
        self.selectable = selectable
        self.image = pygame.image.load(Path('graphics/mouse/select.png'))
        self.rect = self.image.get_rect(topleft=self.pos)
        super().__init__(pos=self.pos, surface=self.image, groups=mouse_sprites)

    def update(self, dt):
        self.rect = self.image.get_rect(topleft=self.pos)