import pygame
from constants import *
from timer import Timer
from sprites import Generic
import random


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
                current_row.append([])
            self.grid.append(current_row)

    def plant(self, index_pos, breed):
        if not self.grid[index_pos[0]][index_pos[1]]:
            self.grid[index_pos[0]][index_pos[1]].append(Plant(self.soil_layer.grid[index_pos[0]][index_pos[1]][0],
                                                               self.all_sprites, breed))

    def update(self):
        for col in range(len(self.grid)):
            for row in range(len(self.grid[col])):
                if self.grid[col][row] and self.grid[col][row][0].marked_for_deletion:
                    self.grid[col][row][0].kill()
                    self.grid[col][row].pop(0)
                else:
                    random_num = random.randint(0, 100000)
                    if not self.grid[col][row] and self.soil_layer.grid[col][row][0].state == SoilStates.NORMAL and random_num == 69:
                        self.grid[col][row].append(Seed(self.soil_layer.grid[col][row][0], self.all_sprites))


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
        self.object_type = ObjectTypes.PLANT
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


class Seed(Generic):
    def __init__(self, soil_tile, all_sprites):
        self.marked_for_deletion = False
        self.soil_tile = soil_tile
        self.pos = self.soil_tile.pos
        # print('a seed spawned at', self.pos)
        self.image = SEED_IMAGE
        self.rect = self.image.get_rect(topleft=self.pos)
        self.timer = Timer(SEED_DEATH_TIME, self.mark_for_deletion)
        self.object_type = ObjectTypes.SEED
        super().__init__(pos=self.pos, surface=self.image, groups=all_sprites)
        self.timer.activate()

    def mark_for_deletion(self):
        self.marked_for_deletion = True

    def update(self, dt):
        self.timer.update()
