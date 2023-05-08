import pygame


class Button:
    def __init__(self, x, y, width, height, text, font, font_size, surface, on_click_func=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        pygame.font.init()
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, font_size)
        self.text_surface = self.font.render(text, True, (20, 20, 20))
        self.rect = self.text_surface.get_rect()
        self.surface = surface
        self.colors = {
            'normal': '#example_color',
            'hovered': '#example_color',
            'pressed': '#example_color'
        }
        self.on_click_func = on_click_func
        self.pressed = False

    def draw(self):
        self.surface.blit(self.text_surface, self.rect)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.text_surface.fill(self.colors['pressed'])
                self.pressed = True
                self.on_click_func()
            else:
                self.text_surface.fill(self.colors['hovered'])
        else:
            self.text_surface.fill(self.colors['normal'])
        if not self.pressed:
            self.draw()
