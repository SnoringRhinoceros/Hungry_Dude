import pygame
from constants import *

START_SCREEN_IMAGE = pygame.image.load(Path('graphics/start_screen'))


class StartScreen:
    def __init__(self):
        self.image = START_SCREEN_IMAGE
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
