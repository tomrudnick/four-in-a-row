import pygame

def render_text(screen, text, font, color, startposition, offset=0):
    text_split = text.splitlines()
    for line in text_split:
        screen_text = font.render(line, True, color)
        screen.blit(screen_text, startposition)
        startposition[1] += screen_text.get_height() + offset

