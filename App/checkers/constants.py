import pygame
from App.constants import WIDTH

ROWS, COLS = 10, 10
SQUARE_SIZE = WIDTH // COLS

#RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (184, 139, 74)
LIGHT = (227, 193, 111)
RED = (255, 0, 0)
GREY = (128, 128, 128)
YELLOW = (244, 192, 69)

#asset
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44,25))