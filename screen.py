
from constants import *
from enum import Enum
from button import Button
from sprites import Generic

START_SCREEN_IMAGE = pygame.image.load(Path('graphics/start_screen/NORMAL.png'))
TUTORIAL_SCREEN_IMAGE = pygame.image.load(Path('graphics/tutorial_screen/TUTORIAL.png'))


class ScreenStates(Enum):
    START = 1
    TUTORIAL = 2
    NORMAL = 3


class ScreenManager:
    def __init__(self, surface):
        # Screen manager should be declared in level.py
        # It's update method also needs to be called
        self.display_surface = surface
        self.state = ScreenStates.NORMAL

        self.start_screen_group = pygame.sprite.Group()
        self.start_screen = StartScreen(group=self.start_screen_group, display_surface=self.display_surface, start_game=self.start_game, start_tutorial=self.start_tutorial)

        self.tutorial_screen_group = pygame.sprite.Group()
        self.tutorial_screen = TutorialScreen(group=self.tutorial_screen_group, display_surface=self.display_surface, start_normal=self.start_normal)

    def start_game(self):
        self.state = ScreenStates.START

    def start_tutorial(self):
        self.state = ScreenStates.TUTORIAL

    def start_normal(self):
        self.state = ScreenStates.NORMAL

    def update(self):
        if self.state == ScreenStates.NORMAL:
            self.display_surface.blit(self.start_screen.image)
            for sprite in self.start_screen_group.sprites():
                sprite.update()
        elif self.state == ScreenStates.TUTORIAL:
            self.display_surface.blit(self.tutorial_screen.image)
            for sprite in self.tutorial_screen_group.sprites():
                sprite.update()


class StaticScreen(Generic):
    def __init__(self, image, buttons, group):
        self.image = image
        self.buttons = buttons
        super().__init__(self, self.image, group)


class StartScreen(StaticScreen):
    def __init__(self, group, display_surface, start_game, start_tutorial):
        # Change the pos of the buttons later
        self.start_button = Button(0, 0, 200, 200, 'Start', 'system_bold.tff', 30, display_surface, start_game)
        self.tutorial_button = Button(0, 500, 200, 200, 'Tutorial', 'system_bold.tff', 30, display_surface, start_tutorial)
        self.buttons = [self.start_button, self.tutorial_button]
        super().__init__(image=START_SCREEN_IMAGE, buttons=self.buttons, group=group)


class TutorialScreen(StaticScreen):
    def __init__(self, group, display_surface, start_normal):
        # Change the pos of the buttons later
        self.exit_button = Button(0, 0, 64, 64, 'Exit', 'system_bold.tff', 20, display_surface, start_normal)
        super().__init__(image=TUTORIAL_SCREEN_IMAGE, buttons=self.buttons, group=group)
