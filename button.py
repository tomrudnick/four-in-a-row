import pygame

class Button():
    def __init__(self, button_pos, button_size, text, color, active_color, screen, radius=0):
        self.button_rect = [button_pos[0], button_pos[1], button_size[0], button_size[1]]
        self.button_pos = button_pos
        self.button_size = button_size
        self.text = text
        self.color = color
        self.active_color = active_color
        self.radius = radius
        self.screen = screen


    def drawButton(self, mouse):
        if self.button_pos[0] <= mouse[0] <= self.button_pos[0] + self.button_size[0] and self.button_pos[1] <= mouse[1] <= self.button_pos[1] + self.button_size[1]:
            pygame.draw.rect(self.screen, self.active_color, self.button_rect, 0, self.radius)
        else:
            pygame.draw.rect(self.screen, self.color, self.button_rect, 0, self.radius)

        button_pos_x = self.button_pos[0] + self.button_size[0] / 2 - self.text.get_width() / 2
        button_pos_y = self.button_pos[1] + self.button_size[1] / 2 - self.text.get_height() / 2
        self.screen.blit(self.text, (button_pos_x, button_pos_y))

    def pressed(self, mouse):
        if self.button_pos[0] <= mouse[0] <= self.button_pos[0] + self.button_size[0] and self.button_pos[1] <= mouse[1] <= self.button_pos[1] + self.button_size[1]:
            return True
        else:
            return False