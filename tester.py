# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from math import *

RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)
CYAN_COLOR = (0, 255, 255)
BROWN_COLOR = (100, 100, 0)
BLACK_COLOR = (0, 0, 0)


def draw_image(window):

    width, height = window.get_size()
    house_x, house_y = width // 2, height * 2 // 3
    house_width = width // 3
    house_height = 4 * house_width // 3

    draw_background(window, 0, 0, width, height)
    draw_house(window, house_x, house_y, house_width, house_height)


def draw_background(window, x, y, width, height):

    pygame.draw.rect(window, GREEN_COLOR, pygame.Rect((0, height // 2),
                                                      (width, height // 2)))
    pygame.draw.rect(window, CYAN_COLOR, pygame.Rect((0, 0),
                                                     (width, height // 2)))


def draw_house(window, x, y, width, height):

    foundation_height = height // 8
    walls_height = height // 2
    walls_width = 7 * width // 8
    roof_height = height - walls_height - foundation_height

    draw_house_foundation(window, x, y, width, foundation_height)
    draw_house_walls(window, x, y - foundation_height,
                     walls_width, walls_height)
    draw_house_roof(window, x, y - foundation_height - walls_height,
                    width, roof_height)


def draw_house_foundation(window, x, y, width, height):
 
    pygame.draw.rect(window, BROWN_COLOR,
                     pygame.Rect((x - width // 2, y - height), (width, height)))


def draw_house_walls(window, x, y, width, height):
 
    pygame.draw.rect(window, RED_COLOR,
                     pygame.Rect((x - width // 2, y - height), (width, height)))
    draw_house_window(window, x, y - height//4, width//3, height//2)


def draw_house_window(window, x, y, width, height):

    print("Функция draw_house_window() вызвана.")


def draw_house_roof(window, x, y, width, height):
    """
    Рисует двускатную крышу домика в заданной ширины width и высоты height.
    Внимание! Опорная точка (x, y) находится в середине основания треугольника.
    Крыша изображается ровно *над* этой точкой.
    """
    pygame.draw.polygon(window, BLUE_COLOR,
                        [(x - width // 2, y),
                         (x + width // 2, y),
                         (x, y - height)])


pygame.init()
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption("HOUSE")

## Здесь можно писать команды рисования из модуля draw библиотеки Pygame
draw_image(window)

pygame.display.update()
going_to_quit = False
while not going_to_quit:
    for event in pygame.event.get():
        if (event.type == QUIT or
                event.type == KEYDOWN and event.key == K_ESCAPE):
            going_to_quit = True
pygame.quit()