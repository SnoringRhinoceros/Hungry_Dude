import pygame
from constants import *
from button import Button

START_SCREEN_IMAGE = pygame.image.load(Path('graphics/start_screen'))


class StartScreenStates(Enum):
    def __init__(self):
        NORMAL = 1
        TUTORIAL = 2
        START = 3


class StartScreen:
    def __init__(self, surface):
        self.image = START_SCREEN_IMAGE
        self.rect = self.image.get_rect()
        self.surface = surface
        self.state = StartScreenStates.NORMAL
        self.start_button = Button(0, 0, 200, 200, 'Start', 'system_bold.tff', 30, self.surface, self.start_game)
        self.tutorial_button = Button(0, 500, 200, 200, 'Tutorial', 'system_bold.tff', 30, self.surface, self.start_tutorial)

    def start_game(self):
        self.state = StartScreenStates.START

    def start_tutorial(self):
        self.state = StartScreenStates.TUTORIAL

    def update(self):
        if self.state == StartScreenStates.NORMAL:
            self.surface.blit(self.image, self.rect)
            self.start_button.update()
        elif self.state == StartScreenStates.TUTORIAL:
            pass # Make tutorial class
