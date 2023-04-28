from constants import *
from sprites import Generic


class NaturalDisaster(Generic):
    def __init__(self, pos, image, group, speed):
        self.pos = pos
        self.image = image
        self.all_sprites = group
        self.status = None
        self.direction = pygame.math.Vector2()
        self.find_original_direction()
        self.speed = speed
        Generic.__init__(self, pos=self.pos, surface=self.image, groups=self.all_sprites)

    def find_original_direction(self):
        # Map.y+Map.height
        if self.pos[1] >= GROUND.get_height():
            self.direction.y = -1
            self.status = 'up'
        # Map.y
        elif self.pos[1] <= 0:
            self.direction.y = 1
            self.status = 'down'
        # Map.x
        if self.pos[0] <= 0:
            self.direction.x = -1
            self.status = 'left'
        # Map.x + Map.width
        elif self.pos[0] >= GROUND.get_width():
            self.direction.x = 1
            self.status = 'right'

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        print((self.rect.centerx, self.rect.centery))

    # Make sure to make an if off-screen method


class Tornado(NaturalDisaster):
    def __init__(self, pos, image, group, speed):
        NaturalDisaster.__init__(self, pos=pos, image=image, group=group)
        self.speed = speed

    def update(self):
        pass
    # Pos should be based off of position of the map not of the screen
    # Give TORNADO_SPEED
    # Make the tornado spawn randomly
    # Make the tornado move based off of speed
