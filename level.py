
import pygame
from constants import *
from player import Player
from sprites import Generic
from soil import SoilLayer
from plant import PlantLayer
from overlay import *
from global_timer import GlobalTimer


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.soil_layer = None
        self.plant_layer = None
        self.player = None
        self.inventory = None
        self.hunger_bar = None
        self.global_timer = None

    def setup(self):
        Generic(pos=(0, 0), surface=GROUND, groups=self.all_sprites)
        self.soil_layer = SoilLayer(self.all_sprites)
        self.plant_layer = PlantLayer(self.all_sprites, self.soil_layer)
        self.player = Player(PLAYER_SPAWN_LOC, self.all_sprites, self.soil_layer, self.plant_layer, self.all_sprites.offset)
        self.inventory = Inventory(self.player.selected_tool)
        self.hunger_bar = HungerBar()
        self.global_timer = GlobalTimer(GLOBAL_TIMER_POS)

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
        else:
            self.display_surface.blit(END_SCREEN_IMAGE, END_SCREEN_IMAGE.get_rect())

    def check_end_con(self):
        if self.player.game_over:
            return True
        else:
            return False


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        # print(self.offset.x, self.offset.y)
        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
        # pygame.draw.rect(self.display_surface, (255, 0, 0), player.hitbox)

