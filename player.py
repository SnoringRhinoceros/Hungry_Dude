
import pygame
from constants import *
from support import *
from timer import Timer
from mouse import Mouse


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, soil_layer, plant_layer, camera_offset):
        super().__init__(group)

        self.game_over = False
        self.animations = None
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = PLAYER_HITBOX.get_rect(center=pos)
        self.camera_offset = camera_offset

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED
        self.feet_pos = self.pos[0], self.pos[1] + (self.rect.height//2)-28
        self.surrounding_tiles = []
        self.hunger_level = 5

        self.tools = ['hoe', 'water', 'seeds', 'wheat']
        self.tool_num = [None, None, 0, 0]
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        self.timers = {'tool_use': Timer(350, self.use_tool), 'tool_switch': Timer(200), 'hunger_bar': Timer(HUNGER_BAR_TICK_TIME, self.hunger_bar_tick)}
        self.timers['hunger_bar'].activate()

        self.soil_layer = soil_layer
        self.plant_layer = plant_layer
        self.mouse = Mouse(self.soil_layer)
        group.add(self.mouse.tile)

    def use_tool(self):
        collided_tile_index = self.print_tile()
        if collided_tile_index is not None:
            collided_tile_pos = collided_tile_index[0] * TILE_SIZE, collided_tile_index[1] * TILE_SIZE
            for i in self.surrounding_tiles:
                if i == collided_tile_pos:
                    # surrounding tile order [left, right, down, up]
                    if self.surrounding_tiles.index(i) == 0:
                        self.status = 'left_' + self.status.split('_')[1]
                    elif self.surrounding_tiles.index(i) == 1:
                        self.status = 'right_' + self.status.split('_')[1]
                    elif self.surrounding_tiles.index(i) == 2:
                        self.status = 'down_' + self.status.split('_')[1]
                    elif self.surrounding_tiles.index(i) == 3:
                        self.status = 'up_' + self.status.split('_')[1]

            # Tool order ['hoe', 'water', 'seeds', 'wheat']
            if self.check_selectable(collided_tile_pos):
                if self.tool_num[self.tools.index(self.selected_tool)] is None or self.tool_num[self.tools.index(self.selected_tool)] > 0:
                    if self.selected_tool == 'hoe' and not self.plant_layer.grid[collided_tile_index[0]][collided_tile_index[1]]:
                        self.soil_layer.grid[collided_tile_index[0]][collided_tile_index[1]][0].till()
                    elif self.selected_tool == 'water':
                        self.soil_layer.grid[collided_tile_index[0]][collided_tile_index[1]][0].water()
                    elif self.selected_tool == 'seeds':
                        if self.soil_layer.grid[collided_tile_index[0]][collided_tile_index[1]][0].state == SoilStates.WATERED:
                            self.plant_layer.plant((collided_tile_index[0], collided_tile_index[1]), 'corn')
                            self.tool_num[2] -= 1
                    elif self.selected_tool == 'wheat':
                        if self.hunger_level < 5:
                            self.tool_num[3] -= 1
                            self.hunger_level += 1

    def check_selectable(self, collided_tile_pos):
        return (collided_tile_pos[0] + TILE_SIZE > self.mouse.pos[0] > collided_tile_pos[0]) and (
                collided_tile_pos[1] + TILE_SIZE > self.mouse.pos[1] > collided_tile_pos[1])

    def find_surrounding_tiles(self, collided_tile):
        self.surrounding_tiles = []
        for i in SURROUNDING_TILE_INTERVAL:
            self.surrounding_tiles.append((collided_tile[0] + i[0], collided_tile[1] + i[1]))

    def print_tile(self):
        collided_tile = self.soil_layer.tile_collision(self.feet_pos, ShapeTypes.POINT)
        if collided_tile is not None:
            # print('mouse pos: ' + str((int(self.mouse.tile.pos[0]), int(self.mouse.tile.pos[1]))))
            collided_tile = collided_tile[0]
            self.find_surrounding_tiles(collided_tile)

            for i in self.surrounding_tiles:
                if i == (int(self.mouse.tile.pos[0]), int(self.mouse.tile.pos[1])):
                    # print('tile pos: ' + str((self.mouse.tile.pos[0], self.mouse.tile.pos[1])))
                    return i[0] // TILE_SIZE, i[1] // TILE_SIZE
            return None

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [], 'left_idle': [],
                           'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [], 'right_axe': [],
                           'left_axe': [], 'up_axe': [],
                           'down_axe': [], 'right_water': [], 'left_water': [], 'up_water': [], 'down_water': [],
                           'up_seeds': [], 'down_seeds': [], 'left_seeds': [], 'right_seeds': [],
                           'up_wheat': [], 'down_wheat': [], 'left_wheat': [], 'right_wheat': []}
        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4*dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        if not self.timers['tool_use'].active:
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if mouse[0]:
                self.timers['tool_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            if keys[pygame.K_e] and not self.timers['tool_switch'].active:
                self.timers['tool_switch'].activate()
                self.tool_index += 1
                if self.tool_index >= len(self.tools):
                    self.tool_index = 0
                self.selected_tool = self.tools[self.tool_index]

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        if self.timers['tool_use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def check_seed_collision(self, collided_tile):
        if self.plant_layer.grid[collided_tile[0]][collided_tile[1]][0].object_type == ObjectTypes.SEED:
            self.tool_num[2] += 1
            self.plant_layer.grid[collided_tile[0]][collided_tile[1]][0].mark_for_deletion()

    def check_plant_collision(self, collided_tile):
        if self.plant_layer.grid[collided_tile[0]][collided_tile[1]][0].object_type == ObjectTypes.PLANT and self.plant_layer.grid[collided_tile[0]][collided_tile[1]][0].state == CornStates.ADULT:
            self.tool_num[3] += 1
            self.plant_layer.grid[collided_tile[0]][collided_tile[1]][0].marked_for_deletion = True

    def check_all_collisions(self):
        collided_tile = self.soil_layer.tile_collision(self.feet_pos, ShapeTypes.POINT)[0]
        collided_tile = collided_tile[0] // TILE_SIZE, collided_tile[1] // TILE_SIZE
        if collided_tile is not None and self.plant_layer.grid[collided_tile[0]][collided_tile[1]]:
            self.check_seed_collision(collided_tile)
            self.check_plant_collision(collided_tile)

    def hunger_bar_tick(self):
        if self.hunger_level >= 1:
            self.hunger_level -= 1
            if self.hunger_level == 0:
                print('you lose :(')
                self.game_over = True
            else:
                self.timers['hunger_bar'] = Timer(HUNGER_BAR_TICK_TIME, self.hunger_bar_tick)
                self.timers['hunger_bar'].activate()

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt

        if self.pos.x < self.rect.width/2:
            self.pos.x = self.rect.width/2
        if self.pos.x > GROUND.get_width()-(self.rect.width/2):
            self.pos.x = GROUND.get_width()-(self.rect.width/2)
        if self.pos.y < self.rect.height/2:
            self.pos.y = self.rect.height/2
        if self.pos.y > GROUND.get_height()-(self.rect.height/2):
            self.pos.y = GROUND.get_height()-(self.rect.height/2)

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.hitbox.centerx = self.pos.x
        self.hitbox.centery = self.pos.y

        self.feet_pos = self.pos[0], self.pos[1] + (self.rect.height//2)-28

    def update(self, dt):
        self.input()
        self.get_status()
        self.check_all_collisions()
        self.update_timers()
        self.move(dt)
        self.animate(dt)
