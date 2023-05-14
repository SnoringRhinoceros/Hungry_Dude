
import pygame
from constants import *
from screen import ScreenManager
from player import Player
from sprites import Generic
from soil import SoilLayer
from plant import PlantLayer
from overlay import *
from global_timer import GlobalTimer
from natural_disaster import *


class Level:
    def __init__(self):
        self.setted_up = False
        self.display_surface = pygame.display.get_surface()
        self.started = False
        self.screen_manager = None
        self.all_sprites = None
        self.soil_layer = None
        self.plant_layer = None
        self.player = None
        self.inventory = None
        self.hunger_bar = None
        self.global_timer = None
        self.natural_disaster_spawner = None
        self.natural_disasters = None

    def start_setup(self):
        self.screen_manager = ScreenManager(self.display_surface)

    def start(self):
        self.screen_manager.update()

    def setup(self):
        self.all_sprites = CameraGroup()
        Generic(pos=(0, 0), surface=GROUND, groups=self.all_sprites)
        self.soil_layer = SoilLayer(self.all_sprites)
        self.plant_layer = PlantLayer(self.all_sprites, self.soil_layer)
        self.player = Player(PLAYER_SPAWN_LOC, self.all_sprites, self.soil_layer, self.plant_layer, self.all_sprites.offset)
        self.inventory = Inventory(self.player.selected_tool)
        self.hunger_bar = HungerBar()
        self.global_timer = GlobalTimer(GLOBAL_TIMER_POS)
        self.natural_disasters = []
        self.natural_disaster_spawner = NaturalDisasterSpawner(self.natural_disasters, self.all_sprites, self.soil_layer, self.plant_layer)
        self.setted_up = True

    def run(self, dt):
        if not self.check_end_con():
            self.display_surface.fill('blue')
            self.all_sprites.custom_draw(self.player)
            self.inventory.update(self.player.selected_tool)
            self.inventory.draw(self.display_surface, self.player.tool_num)
            self.hunger_bar.draw(self.display_surface, self.player.hunger_level)
            self.player.camera_offset = self.all_sprites.offset
            self.plant_layer.update()
            self.all_sprites.update(dt)
            self.player.mouse.update(self.all_sprites.offset)
            self.global_timer.update(dt)
            self.global_timer.draw(self.display_surface)
            self.natural_disaster_spawner.update()
        else:
            self.display_surface.blit(END_SCREEN_IMAGE, END_SCREEN_IMAGE.get_rect())
            self.global_timer.rect.x, self.global_timer.rect.y = 325, 209
            self.display_surface.blit(self.global_timer.image, self.global_timer.rect)

    def check_end_con(self):
        if self.player.game_over:
            return True
        # Natural disaster collision
        player_tile = self.soil_layer.tile_collision(self.player.feet_pos, ShapeTypes.POINT)[0]
        player_collided_tiles = self.player.surrounding_tiles
        for disaster in self.natural_disasters:
            if pygame.Rect.colliderect(self.player.hitbox, disaster.rect):
                return True
        return False


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
        # offset_rect = player.hitbox.copy()
        # offset_rect.center -= self.offset
        # self.display_surface.blit(PLAYER_HITBOX, offset_rect)

