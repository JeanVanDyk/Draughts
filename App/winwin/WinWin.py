import pygame
from constants import DARK, LIGHT, WHITE
from winwin.constants import POPUP_HEIGHT, POPUP_WIDTH, POPUP_X, POPUP_Y
from winwin.constants import MENU_HEIGHT, MENU_WIDTH, MENU_X, MENU_Y

class WinWin:
    def __init__(self, screen, color):
        self.__screen = screen
        self.__color = color
        self.__message = ""
    
    def reset(self):
        self.__message = ""
    
    def menu(self):
        self.__message = ""
    
    def select(self, x, y):
        if x > MENU_X and x < MENU_X + MENU_WIDTH:
            if y > MENU_Y and y < MENU_Y + MENU_HEIGHT:
                self.__message = "MENU"

    def update(self):
        self.draw(self.__screen)
        pygame.display.flip()
        return self.__message
    
    def draw(self, screen):
        pygame.font.init()
        my_font_40 = pygame.font.SysFont('Comic Sans MS', 40)
        my_font_30 = pygame.font.SysFont('Comic Sans MS', 30)

        # Text for pop up
        if self.__color == WHITE:
            winner = my_font_40.render('Félicitations aux blancs !!!', True, (0, 0, 0), LIGHT)
        else:
            winner = my_font_40.render('Félicitations aux noirs !!!', True, (0, 0, 0), LIGHT)  

        winner_l, winner_h = winner.get_size()
        winner_x = POPUP_X + POPUP_WIDTH // 2 - winner_l // 2
        winner_y = POPUP_Y + POPUP_HEIGHT // 2 - winner_h // 2

        # Text for menu
        menu = my_font_30.render("Retourner au menu", True, (0, 0, 0), LIGHT)
        menu_l, menu_h = menu.get_size()
        menu_x = MENU_X + MENU_WIDTH // 2 - menu_l // 2
        menu_y = MENU_Y + MENU_HEIGHT // 2 - menu_h // 2

        # Pop Up
        pygame.draw.rect(screen, self.__color, (POPUP_X-10, POPUP_Y-10, POPUP_WIDTH, POPUP_HEIGHT))
        pygame.draw.rect(screen, LIGHT, (POPUP_X, POPUP_Y, POPUP_WIDTH-20, POPUP_HEIGHT-20))
        screen.blit(winner, (winner_x, winner_y))
        # Menu
        pygame.draw.rect(screen, self.__color, (MENU_X-10, MENU_Y-10, MENU_WIDTH + 20, MENU_HEIGHT + 20))
        pygame.draw.rect(screen, LIGHT, (MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT))
        screen.blit(menu, (menu_x, menu_y))



