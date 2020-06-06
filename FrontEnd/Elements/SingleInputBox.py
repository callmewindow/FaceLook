from FrontEnd.Elements.Element import Element
import pygame
from math import ceil


class InputBox(Element):
    cursor_image = pygame.image.load('./resources/input_cursor.png')

    # 位置，宽度，字体，字号，字色，背景色
    def __init__(self, process, location, width: int, font_type: str, font_size: int, font_color, background_color):
        Element.__init__(self, process)
        self.text = ''
        self.focused = False
        self.changed = False
        self.location = location
        self.font = pygame.font.SysFont(font_type, font_size)
        self.font_color = font_color
        self.size = (width, ceil(font_size * 1.05))
        self.cursor_index = 0
        self.base_x = 0
        self.cursor_x = 0
        self.cursor_count = 0
        self.cursor_image = pygame.transform.smoothscale(InputBox.cursor_image, (1, self.size[1]))
        self.surface = pygame.Surface(self.size)
        self.surface.fill(background_color)

    def add_char(self, ch):
        self.text = self.text[0:self.cursor_index] + ch + self.text[self.cursor_index:]
        self.cursor_index += len(ch)
        self.changed = True

    def backspace_char(self):
        if len(self.text) == 0 or self.cursor_index == 0:
            return
        self.text = self.text[0:self.cursor_index - 1] + self.text[self.cursor_index:]
        self.cursor_index -= 1
        self.changed = True

    def delete_char(self):
        if len(self.text) == self.cursor_index:
            return
        self.text = self.text[0:self.cursor_index] + self.text[self.cursor_index + 1:]
        self.changed = True

    def update(self):
        if self.changed:
            self.changed = False
            self.cursor_count = 0
            self.cursor_x = self.font.size(self.text[0:self.cursor_index])[0]
            update_x = self.cursor_x + self.base_x
            if update_x < 0:
                self.base_x -= update_x
            elif update_x >= self.size[0]:
                self.base_x -= (update_x - self.size[0] + 1)
        self.cursor_count = (self.cursor_count + 1) % 60

    def display(self):
        surface = self.surface.copy()
        if self.text != '':
            surface.blit(self.font.render(self.text, True, self.font_color), (self.base_x, 0))
        if self.focused and self.cursor_count < 30:
            surface.blit(self.cursor_image, (self.cursor_x + self.base_x, 0))
        return surface

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if self.pos_in(event.pos):
                    if not self.focused:
                        self.changed = True
                    self.focused = True
                else:
                    self.focused = False
                return
        if event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_BACKSPACE:
                self.backspace_char()
            if event.key == pygame.K_DELETE:
                self.delete_char()
            if event.key == pygame.K_LEFT and self.cursor_index > 0:
                self.cursor_index -= 1
                self.changed = True
            if event.key == pygame.K_RIGHT and self.cursor_index < len(self.text):
                self.cursor_index += 1
                self.changed = True
        if event.type == pygame.TEXTINPUT and self.focused:
            self.add_char(event.text)

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] \
                and self.location[1] < y < self.location[1] + self.size[1]:
            return True
        return False

    def get_text(self):
        return self.text
