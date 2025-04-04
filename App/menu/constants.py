import pygame
import random

from constants import WIDTH, HEIGHT

# PVP button
START_PVP_LENGTH = WIDTH // 3
START_PVP_HEIGHT = HEIGHT // 10
START_PVP_X = WIDTH // 2 - START_PVP_LENGTH // 2
START_PVP_Y = 2 * HEIGHT // 3

# PVE button
START_PVE_LENGTH = WIDTH // 3
START_PVE_HEIGHT = HEIGHT // 10
START_PVE_X = WIDTH // 2 - START_PVE_LENGTH // 2
START_PVE_Y = 2 * HEIGHT // 3 + 1.5 * START_PVE_HEIGHT

#asset
CHAT = pygame.transform.scale(pygame.image.load('assets/chat.jpg'), (600, 450))
CHAT1 = pygame.transform.scale(pygame.image.load('assets/chat1.jpg'), (600, 450))
CHAT2 = pygame.transform.scale(pygame.image.load('assets/chat2.png'), (600, 450))
OIE = pygame.transform.scale(pygame.image.load('assets/oie.jpg'), (600, 450))
PICTURE = random.choice([CHAT, CHAT1, CHAT2, OIE])