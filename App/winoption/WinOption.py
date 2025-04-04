import pygame
from constants import LIGHT, DARK, WHITE, BLACK
from winoption.constants import POPUP_HEIGHT, POPUP_WIDTH, POPUP_X, POPUP_Y
from winoption.constants import CHOICE_HEIGHT, CHOICE_WIDTH
from winoption.constants import WHITE_X, WHITE_Y
from winoption.constants import BLACK_X, BLACK_Y 
from winoption.constants import RANDOM_X, RANDOM_Y

class WinOption:
    def __init__(self, screen):
        self.__screen = screen
        self.__message = ""
    
    def reset(self):
        self.__message = "MENU"
    
    def menu(self):
        self.__message = "MENU"
    
    def select(self, x, y):
        if x > WHITE_X and x < WHITE_X + CHOICE_WIDTH :
            if y > WHITE_Y and y < WHITE_Y + CHOICE_HEIGHT :
                self.__message = "WHITE"
            
        if x > BLACK_X and x < BLACK_X + CHOICE_WIDTH :
            if y > BLACK_Y and y < BLACK_Y + CHOICE_HEIGHT :
                self.__message = "BLACK"
            
        if x > RANDOM_X and x < RANDOM_X + CHOICE_WIDTH :
            if y > RANDOM_Y and y < RANDOM_Y + CHOICE_HEIGHT :
                self.__message = "RANDOM"

    def update(self):
        self.draw(self.__screen)
        pygame.display.flip()
        return self.__message
    
    def draw(self, screen):
        pygame.font.init()
        my_font_30 = pygame.font.SysFont('Comic Sans MS', 30)

        # Text for choice
        txt_white = my_font_30.render('white', True, (0, 0, 0), WHITE)
        txt_white_l, txt_white_h = txt_white.get_size()
        txt_white_x = WHITE_X + CHOICE_WIDTH // 2 - txt_white_l // 2
        txt_white_y = WHITE_Y + CHOICE_HEIGHT // 2 - txt_white_h // 2

        txt_black = my_font_30.render('black', True, (255, 255, 255), BLACK)  
        txt_black_l, txt_black_h = txt_black.get_size()
        txt_black_x = BLACK_X + CHOICE_WIDTH // 2 - txt_black_l // 2
        txt_black_y = BLACK_Y + CHOICE_HEIGHT // 2 - txt_black_h // 2

        txt_random = my_font_30.render('random', True, (0, 0, 0), DARK)
        txt_random_l, txt_random_h = txt_random.get_size()
        txt_random_x = RANDOM_X + CHOICE_WIDTH // 2 - txt_random_l // 2
        txt_random_y = RANDOM_Y + CHOICE_HEIGHT // 2 - txt_random_h // 2

        # Pop Up
        pygame.draw.rect(screen, LIGHT, (POPUP_X, POPUP_Y, POPUP_WIDTH, POPUP_HEIGHT))

        # White button
        pygame.draw.rect(screen, WHITE, (WHITE_X, WHITE_Y, CHOICE_WIDTH, CHOICE_HEIGHT))
        screen.blit(txt_white, (txt_white_x, txt_white_y))

        # Black button
        pygame.draw.rect(screen, BLACK, (BLACK_X, BLACK_Y, CHOICE_WIDTH, CHOICE_HEIGHT))
        screen.blit(txt_black, (txt_black_x, txt_black_y))

        # Random button
        pygame.draw.rect(screen, DARK, (RANDOM_X, RANDOM_Y, CHOICE_WIDTH, CHOICE_HEIGHT))
        screen.blit(txt_random, (txt_random_x, txt_random_y))
