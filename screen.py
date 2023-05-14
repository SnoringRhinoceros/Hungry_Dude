
from constants import *
from enum import Enum
from button import Button
from sprites import Generic


class ScreenManager:
    def __init__(self, surface):
        self.display_surface = surface
        self.state = ScreenStates.NORMAL

        self.start_screen_group = pygame.sprite.Group()
        self.start_screen = StartScreen(group=self.start_screen_group, display_surface=self.display_surface, start_game=self.start_game, start_tutorial=self.start_tutorial)

        self.tutorial_screen_group = pygame.sprite.Group()
        self.tutorial_screen = TutorialScreen(group=self.tutorial_screen_group, display_surface=self.display_surface, start_normal=self.start_normal)

    def start_game(self):
        self.state = ScreenStates.START
        for i in self.start_screen.buttons:
            i.pressed = True

    def start_tutorial(self):
        self.state = ScreenStates.TUTORIAL
        for i in self.tutorial_screen.buttons:
            i.pressed = False

    def start_normal(self):
        self.state = ScreenStates.NORMAL
        for i in self.start_screen.buttons:
            i.pressed = False

    def update(self):
        if self.state == ScreenStates.NORMAL:
            self.display_surface.blit(self.start_screen.image, self.start_screen.rect)
            for sprite in self.start_screen_group.sprites():
                sprite.update()
        elif self.state == ScreenStates.TUTORIAL:
            self.display_surface.blit(self.tutorial_screen.image, self.tutorial_screen.rect)
            for sprite in self.tutorial_screen_group.sprites():
                sprite.update()


class StaticScreen(Generic):
    def __init__(self, image, buttons, group):
        self.image = image
        self.buttons = buttons
        super().__init__((0, 0), self.image, group)


class StartScreen(StaticScreen):
    def __init__(self, group, display_surface, start_game, start_tutorial):
        self.start_button = Button(223, 260, 284, 102, 'Start', 'system_bold.tff', 30, display_surface, group, start_game)
        self.tutorial_button = Button(225, 435, 284, 102, 'Tutorial', 'system_bold.tff', 30, display_surface, group, start_tutorial)
        self.buttons = [self.start_button, self.tutorial_button]
        super().__init__(image=START_SCREEN_IMAGE, buttons=self.buttons, group=group)


class TutorialScreen(StaticScreen):
    def __init__(self, group, display_surface, start_normal):
        self.exit_button = Button(29, 677, 120, 50, 'Exit', 'system_bold.tff', 20, display_surface, group, start_normal)
        self.buttons = [self.exit_button]
        super().__init__(image=TUTORIAL_SCREEN_IMAGE, buttons=self.buttons, group=group)
