from constants import *
from timer import Timer


class GlobalTimer(Timer):
    def __init__(self):
        self.pos = (100, 100)
        super().__init__(None, None)
        self.current_time = None
        self.activate()

    def update(self):
        self.current_time = pygame.time.get_ticks()
        print(self.current_time)
