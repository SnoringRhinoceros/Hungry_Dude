from constants import *
import math


class GlobalTimer:
    def __init__(self, pos):
        self.pos = pos
        self.starting_time = 0
        self.current_time = 0
        self.text = '0'
        self.image = None
        self.rect = None

    def activate(self):
        self.starting_time = pygame.time.get_ticks()

    def add_zeros(self, integer):
        if len(str(integer)) == 1:
            return '0' + str(integer)
        else:
            return str(integer)

    def print_time(self, milliseconds):
        seconds = math.floor(milliseconds / 1000)
        minutes = math.floor(seconds / 60)
        hours = math.floor(minutes / 60)
        return self.add_zeros(hours) + ':' + self.add_zeros(minutes) + ':' + self.add_zeros(seconds)

    def update(self, dt):
        self.current_time = pygame.time.get_ticks()
        self.text = self.print_time(self.current_time - self.starting_time)
        self.image = GLOBAL_TIMER_FONT.render(self.text, True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)
