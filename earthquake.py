import pygame
from constants import *
from natural_disaster import NaturalDisaster


class Earthquake(NaturalDisaster):
    def __init__(self, middle_tile, soil_layer, plant_layer, image, group):
        self.middle_tile = middle_tile
        self.marked_for_deletion = False
        self.soil_layer = soil_layer
        self.plant_layer = plant_layer
        self.all_tiles = self.find_all_tiles()
        NaturalDisaster.__init__(self, pos=self.all_tiles[7], image=image, group=group, speed=0)
        self.frame_index = 0
        self.image = EARTHQUAKE_ANIMATIONS[self.frame_index]
        self.destroy()

    def find_all_tiles(self):
        middle_collided_tile = self.soil_layer.tile_collision(self.middle_tile.pos, ShapeTypes.POINT)[0]
        middle_collided_tile_index = middle_collided_tile[0] // TILE_SIZE, middle_collided_tile[1] // TILE_SIZE
        return [(middle_collided_tile_index[0]+i[0], middle_collided_tile_index[1]+i[1]) for i in EARTHQUAKE_SURROUNDING_INTERVAL if GROUND.get_width >= middle_collided_tile_index[0]+i[0] >= 0 and GROUND.get_height() >= middle_collided_tile_index[1]+i[1] <= 0]

    def animate(self, dt):
        self.frame_index += 4*dt
        if self.frame_index <= len(EARTHQUAKE_ANIMATIONS):
            self.image = EARTHQUAKE_ANIMATIONS[int(self.frame_index)]
        else:
            self.marked_for_deletion = True

    def destroy(self):
        for i in self.all_tiles:
            # make it animate
            self.plant_layer[i[0]][i[1]].marked_for_deletion = True
            self.soil_layer[i[0]][i[1]].state = SoilStates.NORMAL

    def update(self, dt):
        self.animate(dt)
        if self.marked_for_deletion:
            self.kill()
