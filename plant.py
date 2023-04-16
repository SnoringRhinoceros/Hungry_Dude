import pygame
from constants import *
from timer import Timer
from sprites import Generic


class PlantLayer:
    def __init__(self, all_sprites, soil_layer):
        self.all_sprites = all_sprites
        self.soil_layer = soil_layer
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
            self.grid[index_pos[0]][index_pos[1]].append(Plant(self.soil_layer.grid[index_pos[0]][index_pos[1]][0],
                                                               self.all_sprites, breed))

    def update(self):
        for col in self.grid:
            for row in col:
                if row and row[0].marked_for_deletion:
                    row[0].kill()
                    row.pop(0)


class Plant(Generic):
    def __init__(self, soil_tile, all_sprites, breed):
        self.marked_for_deletion = False
        self.breed = breed
        self.soil_tile = soil_tile
        self.pos = self.soil_tile.pos
        self.state = CornStates.SEED
        self.has_water = True
        self.timer = Timer(PLANT_GROW_SPEED, self.change_state)
        self.image = PLANT_IMAGES[self.state.value-1]
        super().__init__(pos=self.pos, surface=self.image, groups=all_sprites)
        self.timer.activate()

    def change_state(self):
        if self.has_water:
            self.has_water = False
            if self.state is not CornStates.ADULT:
                self.state = CornStates(self.state.value+1)
            self.timer = Timer(PLANT_GROW_SPEED, self.change_state)
            self.soil_tile.state = SoilStates.TILLED
            self.timer.activate()

        else:
            self.marked_for_deletion = True

    def update(self, dt):
        self.timer.update()
        if self.soil_tile.state == SoilStates.WATERED:
            self.has_water = True
        else:
            self.has_water = False
        self.image = PLANT_IMAGES[self.state.value-1]
        self.rect = self.image.get_rect(topleft=self.pos)
