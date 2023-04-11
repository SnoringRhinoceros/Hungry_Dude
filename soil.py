import pygame
from constants import *
from sprites import Generic


class SoilLayer:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites

        self.grid = []
        self.create_soil_grid()

    def create_soil_grid(self):
        horiz_tiles, verti_tiles = GROUND.get_width() // TILE_SIZE, GROUND.get_height() // TILE_SIZE
        # print(horiz_tiles)
        # print(verti_tiles)

        for col in range(horiz_tiles):
            current_row = []
            for row in range(verti_tiles):
                soil_tile = SoilTile((col * TILE_SIZE, row * TILE_SIZE), SoilStates.NORMAL, self.all_sprites)
                current_row.append([soil_tile])
            self.grid.append(current_row)

    def tile_collision(self, shape, shape_type):
        collided_tiles = []
        for i in self.grid:
            for j in i:
                if shape_type == ShapeTypes.RECT:
                    if pygame.Rect.colliderect(j[0].rect, shape):
                        collided_tiles.append(j[0].pos)
                elif shape_type == ShapeTypes.POINT:
                    if pygame.Rect.collidepoint(j[0].rect, shape):
                        collided_tiles.append(j[0].pos)
        if collided_tiles:
            return collided_tiles
        else:
            return None


class SoilTile(Generic):
    def __init__(self, pos, state, all_sprites):
        self.pos = pos
        self.state = state
        self.tilled_surface = TILLED_SURFACE
        self.normal_surface = NORMAL_SURFACE
        self.watered_surface = WATERED_SURFACE
        self.image = self.normal_surface
        super().__init__(pos=self.pos, surface=self.image, groups=all_sprites)

    def till(self):
        if self.state == SoilStates.NORMAL:
            self.state = SoilStates.TILLED
        elif self.state == SoilStates.TILLED:
            self.state = SoilStates.NORMAL

    def water(self):
        if self.state == SoilStates.TILLED:
            self.state = SoilStates.WATERED

    def update(self, dt):
        if self.state == SoilStates.NORMAL:
            self.image = self.normal_surface
            self.rect = self.image.get_rect(topleft=self.pos)
        elif self.state == SoilStates.TILLED:
            self.image = self.tilled_surface
            self.rect = self.image.get_rect(topleft=self.pos)
        elif self.state == SoilStates.WATERED:
            self.image = self.watered_surface
            self.rect = self.image.get_rect(topleft=self.pos)
