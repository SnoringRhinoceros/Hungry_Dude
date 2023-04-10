
import pygame
from constants import *


class Overlay:
    def __init__(self, selected_tool):
        self.pos = OVERLAY_POS
        self.width = OVERLAY_WIDTH
        self.length = OVERLAY_LENGTH
        self.selected_images = OVERLAY_SELECTED_IMAGES
        self.unselected_images = OVERLAY_UNSELECTED_IMAGES
        self.image_names = OVERLAY_IMAGE_NAMES
        self.images = []
        self.rects = []
        self.selected_tool = selected_tool

    def draw(self, surface):
        # Image order: [background.png, hoe.png seeds.png, water.png] (alphabetical)
        self.images = []
        for i in range(len(self.unselected_images)):
            if not self.image_names[i] == self.selected_tool+'.png':
                self.images.append(self.unselected_images[i])
            else:
                self.images.append(self.selected_images[i-1])
        self.rects = [i.get_rect() for i in self.images]
        self.rects[0].x, self.rects[0].y = self.pos
        self.rects[1].x, self.rects[1].y = self.pos[0]+OVERLAY_SLOT_SIDE_WIDTH, self.pos[1]+OVERLAY_SLOT_SIDE_LENGTH
        self.rects[3].x, self.rects[3].y = self.pos[0]+OVERLAY_SLOT_SIDE_WIDTH+TILE_SIZE+OVERLAY_SLOT_MIDDLE_WIDTH, self.pos[1]+OVERLAY_SLOT_SIDE_LENGTH
        self.rects[2].x, self.rects[2].y = self.pos[0]+OVERLAY_SLOT_SIDE_WIDTH+TILE_SIZE+OVERLAY_SLOT_MIDDLE_WIDTH+TILE_SIZE+OVERLAY_SLOT_MIDDLE_WIDTH, self.pos[1]+OVERLAY_SLOT_SIDE_LENGTH

        for i in range(len(self.images)):
            surface.blit(self.images[i], self.rects[i])

    def update(self, selected_tool):
        self.selected_tool = selected_tool
