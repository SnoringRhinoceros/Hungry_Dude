
# Credit to Cup Nooble for the Sprout Lands asset pack and UI expansion https://cupnooble.itch.io/
# Credit to the ClearCode YouTube Channel for
# help with player movement (delta time), the camera, and sprite class structure videos
# I watched: https://www.youtube.com/watch?v=T4IX36sP_0c, https://www.youtube.com/watch?v=rWtfClpWSb8m,
# and https://www.youtube.com/watch?v=u7LPRqrzry8&t=143s

import pygame
import sys
from constants import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # pygame.RESIZABLE
        # pygame.FULL_SCREEN
        pygame.display.set_caption("Hungry Dude")
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.level.start_setup()


def main():
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        if not game.level.screen_manager.state == ScreenStates.START:
            game.level.start()
        else:
            if not game.level.setted_up:
                game.level.setup()
            dt = game.clock.tick() / 1000
            game.level.run(dt)
        pygame.display.update()


main()
