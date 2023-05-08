from constants import *
from sprites import Generic
from timer import Timer
import random


class NaturalDisaster(Generic):
    def __init__(self, pos, image, group, speed):
        self.pos = pos
        self.image = image
        self.all_sprites = group
        self.direction = pygame.math.Vector2()
        self.find_original_direction()
        self.speed = speed
        self.marked_for_deletion = False
        Generic.__init__(self, pos=self.pos, surface=self.image, groups=self.all_sprites)

    def find_original_direction(self):
        if self.pos[1] <= 0:
            self.direction.y = 1
        elif self.pos[1] >= GROUND.get_height():
            self.direction.y = -1

        if self.pos[0] <= 0:
            self.direction.x = 1
        elif self.pos[0] >= GROUND.get_width():
            self.direction.x = -1

    def move(self, dt):
        self.pos = (self.pos[0] + self.direction.x * self.speed * dt, self.pos[1] + self.direction.y * self.speed * dt)

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    # Make sure to make an if off-screen method


class NaturalDisasterSpawner:
    def __init__(self, natural_disasters, all_sprites):
        self.natural_disasters = natural_disasters
        self.all_sprites = all_sprites
        self.tornado_timer = Timer(random.randint(NATURAL_DISASTER_SPAWN_TIMES['tornado'][0], NATURAL_DISASTER_SPAWN_TIMES['tornado'][1]), self.spawn, 'tornado')
        self.earthquake_timer = Timer(random.randint(NATURAL_DISASTER_SPAWN_TIMES['earthquake'][0], NATURAL_DISASTER_SPAWN_TIMES['earthquake'][1]), self.spawn, 'earthquake')
        self.timers = {'tornado': self.tornado_timer, 'earthquake': self.earthquake_timer}
        for timer in self.timers.values():
            timer.activate()

    def append_disaster(self, disaster):
        if disaster == 'tornado':
            all_sides = ['up', 'right', 'down', 'left']
            chosen_side = random.choice(all_sides)
            if chosen_side == 'up':
                self.natural_disasters.append(Tornado((random.randrange(0, GROUND.get_width(), 64), -TILE_SIZE), TORNADO_IMAGE, self.all_sprites, TORNADO_SPEED))
            elif chosen_side == 'right':
                self.natural_disasters.append(Tornado((GROUND.get_width()+TILE_SIZE, random.randrange(0, GROUND.get_height(), 64)), TORNADO_IMAGE, self.all_sprites, TORNADO_SPEED))
            elif chosen_side == 'down':
                self.natural_disasters.append(Tornado((random.randrange(0, GROUND.get_width(), 64), GROUND.get_height()+TILE_SIZE), TORNADO_IMAGE, self.all_sprites, TORNADO_SPEED))
            elif chosen_side == 'left':
                self.natural_disasters.append(Tornado((-TILE_SIZE, random.randrange(0, GROUND.get_height(), 64)), TORNADO_IMAGE, self.all_sprites, TORNADO_SPEED))

    def spawn(self, disaster):
        self.timers[disaster] = Timer(random.randint(NATURAL_DISASTER_SPAWN_TIMES[disaster][0], NATURAL_DISASTER_SPAWN_TIMES[disaster][0]), self.spawn, disaster)
        self.append_disaster(disaster)
        self.timers[disaster].activate()

    def update(self):
        for timer in self.timers.values():
            timer.update()
        indexes_to_kill = []
        for disaster in range(len(self.natural_disasters)):
            if self.natural_disasters[disaster].marked_for_deletion:
                indexes_to_kill.append(disaster)
        indexes_to_kill = sorted(indexes_to_kill, reverse=True)
        for i in indexes_to_kill:
            if i < len(self.natural_disasters):
                self.natural_disasters.pop(i)


class Tornado(NaturalDisaster):
    def __init__(self, pos, image, group, speed):
        NaturalDisaster.__init__(self, pos=pos, image=image, group=group, speed=speed)

    def check_offscreen(self):
        if ((self.direction.x == 1 and self.pos[0] > GROUND.get_width()) or (self.direction.x == -1 and self.pos[0] < 0) or self.direction.x == 0) and ((self.direction.y == 1 and self.pos[1] > GROUND.get_height()) or (self.direction.y == -1 and self.pos[1] < 0) or self.direction.y == 0):
            self.marked_for_deletion = True

    def update(self, dt):
        self.check_offscreen()
        self.move(dt)
