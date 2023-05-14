import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, font, font_size, surface, group, on_click_func=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        pygame.font.init()
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, font_size)
        self.text_surface = self.font.render(text, False, (20, 20, 20))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.display_surface = surface
        self.button_surface = pygame.Surface((self.width, self.height))
        self.colors = {
            'normal': '#C1C8B9',
            'hovered': '#818B83',
            'pressed': '#545959'
        }
        self.on_click_func = on_click_func
        self.pressed = False
        super().__init__(group)

    def draw(self):
        self.button_surface.blit(self.text_surface, (self.rect.width/2 - self.text_surface.get_rect().width/2, self.rect.height/2 - self.text_surface.get_rect().height/2))
        self.display_surface.blit(self.button_surface, self.rect)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.colors['pressed'])
                self.pressed = True
                self.on_click_func()
            else:
                self.button_surface.fill(self.colors['hovered'])
        else:
            self.button_surface.fill(self.colors['normal'])
        if not self.pressed:
            self.draw()
