import pygame
import random

from App.constants import WIDTH, HEIGHT

# PVP button
START_PVP_LENGTH = WIDTH // 3
START_PVP_HEIGHT = HEIGHT // 10
START_PVP_X = WIDTH // 2 - START_PVP_LENGTH // 2
START_PVP_Y = 490

# PVE button
START_PVE_LENGTH = WIDTH // 3
START_PVE_HEIGHT = HEIGHT // 10
START_PVE_X = WIDTH // 2 - START_PVE_LENGTH // 2
START_PVE_Y = 490 + 1.1 * START_PVE_HEIGHT

# EVE button
START_EVE_LENGTH = WIDTH // 3
START_EVE_HEIGHT = HEIGHT // 10
START_EVE_X = WIDTH // 2 - START_PVE_LENGTH // 2
START_EVE_Y = 490 + 2.2 * START_PVE_HEIGHT

#asset
CHAT = pygame.transform.scale(pygame.image.load('assets/chat.jpg'), (600, 450))
CHAT1 = pygame.transform.scale(pygame.image.load('assets/chat1.jpg'), (600, 450))
CHAT2 = pygame.transform.scale(pygame.image.load('assets/chat2.png'), (600, 450))
OIE = pygame.transform.scale(pygame.image.load('assets/oie.jpg'), (600, 450))
PICTURE = random.choice([CHAT, CHAT1, CHAT2, OIE])