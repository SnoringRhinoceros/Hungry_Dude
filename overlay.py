
import pygame
from constants import *


class Inventory:
    def __init__(self, selected_tool):
        self.pos = OVERLAY_INVENTORY_POS
        self.width = OVERLAY_INVENTORY_WIDTH
        self.length = OVERLAY_INVENTORY_LENGTH
        self.selected_images = OVERLAY_INVENTORY_SELECTED_IMAGES
        self.unselected_images = OVERLAY_INVENTORY_UNSELECTED_IMAGES
        self.image_names = OVERLAY_INVENTORY_IMAGE_NAMES
        self.images = []
        self.rects = []
        self.selected_tool = selected_tool

    def draw(self, surface, tool_num):
        # Image order: ['background.png', 'hoe.png', 'seeds.png', 'water.png', 'wheat.png', 'wheat_pressed.png']
        # (alphabetical)
        self.images = []
        for i in range(len(self.unselected_images)):
            if not self.image_names[i] == self.selected_tool+'.png':
                self.images.append(self.unselected_images[i])
            else:
                self.images.append(self.selected_images[i-1])
        self.rects = [i.get_rect() for i in self.images]
        self.rects[0].x, self.rects[0].y = self.pos
        self.rects[1].x, self.rects[1].y = self.pos[0]+OVERLAY_INVENTORY_SLOT_SIDE_WIDTH, self.pos[1]+OVERLAY_INVENTORY_SLOT_SIDE_LENGTH
        self.rects[3].x, self.rects[3].y = self.pos[0]+OVERLAY_INVENTORY_SLOT_SIDE_WIDTH+TILE_SIZE+OVERLAY_INVENTORY_SLOT_MIDDLE_WIDTH, self.pos[1]+OVERLAY_INVENTORY_SLOT_SIDE_LENGTH
        self.rects[2].x, self.rects[2].y = self.pos[0]+OVERLAY_INVENTORY_SLOT_SIDE_WIDTH+TILE_SIZE+OVERLAY_INVENTORY_SLOT_MIDDLE_WIDTH+TILE_SIZE+OVERLAY_INVENTORY_SLOT_MIDDLE_WIDTH, self.pos[1]+OVERLAY_INVENTORY_SLOT_SIDE_LENGTH
        self.rects[4].x, self.rects[4].y = self.pos[0]+OVERLAY_INVENTORY_SLOT_SIDE_WIDTH+TILE_SIZE+OVERLAY_INVENTORY_SLOT_MIDDLE_WIDTH+TILE_SIZE+OVERLAY_INVENTORY_SLOT_MIDDLE_WIDTH+TILE_SIZE+OVERLAY_INVENTORY_SLOT_MIDDLE_WIDTH, self.pos[1]+OVERLAY_INVENTORY_SLOT_SIDE_LENGTH
        tool_num_indexes_to_draw = [i for i in range(len(tool_num)) if tool_num[i] is not None]
        tool_num_text = [OVERLAY_INVENTORY_FONT.render(str(i), True, BLACK) for i in tool_num if tool_num is not None]
        tool_num_text_rects = [i.get_rect() for i in tool_num_text]
        for i in range(len(tool_num_text_rects)):
            if i+1 == 2:
                tool_num_text_rects[i].x, tool_num_text_rects[i].y = self.rects[i+2].x+OVERLAY_INVENTORY_TEXT_OFFSET, self.rects[i+2].y+OVERLAY_INVENTORY_TEXT_OFFSET
            elif i+1 == 3:
                tool_num_text_rects[i].x, tool_num_text_rects[i].y = self.rects[i].x + OVERLAY_INVENTORY_TEXT_OFFSET, self.rects[i].y + OVERLAY_INVENTORY_TEXT_OFFSET
            else:
                tool_num_text_rects[i].x, tool_num_text_rects[i].y = self.rects[i+1].x+OVERLAY_INVENTORY_TEXT_OFFSET, self.rects[i+1].y+OVERLAY_INVENTORY_TEXT_OFFSET

        for i in range(len(self.images)):
            surface.blit(self.images[i], self.rects[i])
        for i in range(len(tool_num_text)):
            if i in tool_num_indexes_to_draw:
                surface.blit(tool_num_text[i], tool_num_text_rects[i])

    def update(self, selected_tool):
        self.selected_tool = selected_tool


class HungerBar:
    def __init__(self):
        self.pos = OVERLAY_HUNGER_BAR_POS
        self.image_distance = OVERLAY_HUNGER_BAR_IMAGE_DISTANCE
        self.image = OVERLAY_HUNGER_BAR_FILLED_IMAGE
        self.rect = self.image.get_rect()
        self.player_hunger_level = None

    def draw(self, surface, player_hunger_level):
        self.player_hunger_level = player_hunger_level
        for i in range(OVERLAY_HUNGER_BAR_TOTAL):
            if i >= self.player_hunger_level:
                self.image = OVERLAY_HUNGER_BAR_EMPTY_IMAGE
            else:
                self.image = OVERLAY_HUNGER_BAR_FILLED_IMAGE
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.pos[0] + i*OVERLAY_HUNGER_BAR_IMAGE_DISTANCE, self.pos[1]
            surface.blit(self.image, self.rect)
