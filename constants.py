from enum import IntEnum
from enum import Enum
import pygame
from pathlib import Path
import os

PLAYER_SPAWN_LOC = (640, 360)
PLAYER_SPEED = 400
PLAYER_HITBOX_X = 0.6
PLAYER_HITBOX_Y = 0.9

TILE_SIZE = 64
SURROUNDING_TILE_INTERVAL = [(-TILE_SIZE, 0), (TILE_SIZE, 0), (0, TILE_SIZE), (0, -TILE_SIZE)]
GROUND = pygame.image.load(Path('graphics/world/ground.png'))

SCREEN_SCALE = 0.3
SCREEN_WIDTH = GROUND.get_width() * SCREEN_SCALE
SCREEN_HEIGHT = GROUND.get_height() * SCREEN_SCALE

TILLED_SURFACE = pygame.image.load(Path('graphics/soil/soil.png'))
NORMAL_SURFACE = pygame.image.load(Path('graphics/soil/transparent.png'))
WATERED_SURFACE = pygame.image.load(Path('graphics/soil/watered_soil.png'))

OVERLAY_SELECTED_IMAGES = [pygame.image.load(Path('graphics/inventory/' + f)) for f in os.listdir(Path('graphics/inventory')) if not f == 'Thumbs.db' and 'selected' in f]
OVERLAY_UNSELECTED_IMAGES = [pygame.image.load(Path('graphics/inventory/' + f)) for f in os.listdir(Path('graphics/inventory')) if not f == 'Thumbs.db' and 'selected' not in f]
OVERLAY_IMAGE_NAMES = [f for f in os.listdir(Path('graphics/inventory')) if not f == 'Thumbs.db' and 'selected' not in f]
OVERLAY_POS = (64, 576)
OVERLAY_LENGTH = 320
OVERLAY_WIDTH = 128
OVERLAY_SLOT_SIDE_WIDTH = 20
OVERLAY_SLOT_MIDDLE_WIDTH = 44
OVERLAY_SLOT_SIDE_LENGTH = 32

PLANT_IMAGES = [pygame.image.load(Path('graphics/crops/corn/' + f)) for f in os.listdir(Path('graphics/crops/corn')) if not f == 'Thumbs.db']
PLANT_GROW_SPEED = 1000


class CornStates(IntEnum):
    SEED = 1
    SEEDLING = 2
    YOUNG = 3
    ADULT = 4


class SoilStates(Enum):
    NORMAL = 1
    TILLED = 2
    WATERED = 3
    PLANT = 4


class ShapeTypes(Enum):
    RECT = 1
    POINT = 2
