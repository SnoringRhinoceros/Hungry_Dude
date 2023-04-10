import pygame
from constants import *
from timer import Timer
from sprites import Generic


class PlantLayer:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.grid = []
        self.create_plant_grid()

    def create_plant_grid(self):
        horiz_tiles, verti_tiles = GROUND.get_width() // TILE_SIZE, GROUND.get_height() // TILE_SIZE
        # print(horiz_tiles)
        # print(verti_tiles)

        for col in range(horiz_tiles):
            current_row = []
            for row in range(verti_tiles):
                # soil_tile = Plant((col * TILE_SIZE, row * TILE_SIZE), Timer(PLANT_GROW_SPEED), self.all_sprites)
                current_row.append([])
            self.grid.append(current_row)

    def plant(self, index_pos, breed):
        if not self.grid[index_pos[0]][index_pos[1]]:
            self.grid[index_pos[0]][index_pos[1]].append(Plant((index_pos[0] * TILE_SIZE, index_pos[1] * TILE_SIZE), Timer(PLANT_GROW_SPEED), self.all_sprites, breed))


class Plant(Generic):
    def __init__(self, pos, timer, group, breed):
        self.breed = breed
        self.pos = pos
        self.state = CornStates.SEED
        self.has_water = False
        self.timer = timer
        self.surface = PLANT_IMAGES[self.state-1]
        super().__init__(pos=self.pos, surface=self.surface, groups=group)
        self.timer.activate()

    def change_state(self):
        self.state = self.state + 1
        print(self.state)

    def update(self, dt):
        if not self.timer.active:
            if self.state is not CornStates.ADULT:
                if self.has_water:
                    self.has_water = False
                    self.change_state()
                    self.timer = Timer(PLANT_GROW_SPEED)
                    self.timer.activate()
                self.image = PLANT_IMAGES[self.state]
                self.rect = self.image.get_rect()
            else:
                del self
