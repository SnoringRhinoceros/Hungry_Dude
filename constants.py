from enum import IntEnum
from enum import Enum
import pygame
from pathlib import Path
import os

BLACK = (0, 0, 0)

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

GLOBAL_TIMER_POS = (100, 100)
pygame.font.init()
GLOBAL_TIMER_FONT = pygame.font.SysFont('system_bold.tff', 30)
GLOBAL_TIMER_BACKGROUND = pygame.image.load(Path('graphics/timer/background.png'))

OVERLAY_INVENTORY_SELECTED_IMAGES = [pygame.image.load(Path('graphics/overlay/inventory/' + f)) for f in os.listdir(Path('graphics/overlay/inventory')) if not f == 'Thumbs.db' and 'selected' in f]
OVERLAY_INVENTORY_UNSELECTED_IMAGES = [pygame.image.load(Path('graphics/overlay/inventory/' + f)) for f in os.listdir(Path('graphics/overlay/inventory')) if not f == 'Thumbs.db' and 'selected' not in f]
OVERLAY_INVENTORY_IMAGE_NAMES = [f for f in os.listdir(Path('graphics/overlay/inventory')) if not f == 'Thumbs.db' and 'selected' not in f]
OVERLAY_INVENTORY_POS = (64, 576)
OVERLAY_INVENTORY_LENGTH = 320
OVERLAY_INVENTORY_WIDTH = 128
OVERLAY_INVENTORY_SLOT_SIDE_WIDTH = 20
OVERLAY_INVENTORY_SLOT_MIDDLE_WIDTH = 44
OVERLAY_INVENTORY_SLOT_SIDE_LENGTH = 32
OVERLAY_INVENTORY_FONT = pygame.font.SysFont('system_bold.tff', 15)
OVERLAY_INVENTORY_TEXT_OFFSET = 45

OVERLAY_HUNGER_BAR_FILLED_IMAGE = pygame.image.load(Path('graphics/overlay/hunger_bar/hunger_bar_filled.png'))
OVERLAY_HUNGER_BAR_EMPTY_IMAGE = pygame.image.load(Path('graphics/overlay/hunger_bar/hunger_bar_empty.png'))
OVERLAY_HUNGER_BAR_POS = OVERLAY_INVENTORY_POS[0], OVERLAY_INVENTORY_POS[1]-64
OVERLAY_HUNGER_BAR_TOTAL = 5
OVERLAY_HUNGER_BAR_IMAGE_DISTANCE = 69
HUNGER_BAR_TICK_TIME = 5000

PLANT_IMAGES = [pygame.image.load(Path('graphics/crops/corn/' + f)) for f in os.listdir(Path('graphics/crops/corn')) if not f == 'Thumbs.db']
PLANT_GROW_SPEED = 5000
SEED_IMAGE = pygame.image.load(Path('graphics/objects/seeds.png'))
SEED_DEATH_TIME = 10000

TORNADO_SPEED = 100
TORNADO_IMAGE = pygame.image.load(Path('graphics/natural_disasters/tornado/0.png'))

END_SCREEN_IMAGE = pygame.image.load(Path('graphics/end_screen/end_screen.png'))


class ObjectTypes(Enum):
    PLANT = 1
    SEED = 2


class CornStates(Enum):
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
