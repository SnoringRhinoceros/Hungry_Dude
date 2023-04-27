from constants import *
from sprites import Generic


class GlobalTimer(Generic):
    def __init__(self, pos):
        self.pos = pos
        self.starting_time = 0
        self.current_time = 0
        self.image = GLOBAL_TIMER_FONT.render(str(self.current_time-self.starting_time), True, BLACK)
        self.rect = self.image.get_rect()

    def activate(self):
        self.starting_time = pygame.time.get_ticks()

    def update(self, dt):
        self.current_time = pygame.time.get_ticks()
        self.image = GLOBAL_TIMER_FONT.render(str(self.current_time - self.starting_time), True, BLACK)
        self.rect = self.image.get_rect()
        print(self.current_time - self.starting_time)

    def draw(self):
        # make it draw
