import pygame
from App.constants import WIDTH, DARK, LIGHT
from App.menu.constants import START_PVP_X, START_PVP_Y, START_PVP_HEIGHT, START_PVP_LENGTH
from App.menu.constants import START_PVE_X, START_PVE_Y, START_PVE_HEIGHT, START_PVE_LENGTH
from App.menu.constants import START_EVE_X, START_EVE_Y, START_EVE_HEIGHT, START_EVE_LENGTH
from App.menu.constants import PICTURE

class WinMenu:

    def __init__(self, screen):
        self.__screen = screen
        self.__message = ""
        self.draw()

    def update(self):
        self.draw()
        pygame.display.flip()
        return self.__message

    def select(self, x, y):
        if x > START_PVP_X and x < START_PVP_X + START_PVP_LENGTH :
            if y > START_PVP_Y and y < START_PVP_Y + START_PVP_HEIGHT :
                self.__message = "GAME_PVP"
        
        if x > START_PVE_X and x < START_PVE_X + START_PVE_LENGTH :
            if y > START_PVE_Y and y < START_PVE_Y + START_PVE_HEIGHT :
                self.__message = "GAME_PVE"
        
        if x > START_EVE_X and x < START_EVE_X + START_EVE_LENGTH :
            if y > START_EVE_Y and y < START_EVE_Y + START_EVE_HEIGHT :
                self.__message = "GAME_EVE" 
    
    def resest(self):
        self.__message = "MENU"
    
    def menu(self):
        self.__message = "MENU"
    
    def draw(self):
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)

        # Start PVP text
        txt_pvp = my_font.render('PvP', True, (0, 0, 0), LIGHT)
        txt_pvp_l, txt_pvp_h = txt_pvp.get_size()
        txt_pvp_x = START_PVP_X + START_PVP_LENGTH // 2 - txt_pvp_l // 2
        txt_pvp_y = START_PVP_Y + START_PVP_HEIGHT // 2 - txt_pvp_h // 2

        # Start PVE text
        txt_pve = my_font.render('PvE', True, (0, 0, 0), LIGHT)
        txt_pve_l, txt_pve_h = txt_pve.get_size()
        txt_pve_x = START_PVE_X + START_PVE_LENGTH // 2 - txt_pve_l // 2
        txt_pve_y = START_PVE_Y + START_PVE_HEIGHT // 2 - txt_pve_h // 2

        # Start EVE text
        txt_eve = my_font.render('EvE', True, (0, 0, 0), LIGHT)
        txt_eve_l, txt_eve_h = txt_pve.get_size()
        txt_eve_x = START_EVE_X + START_EVE_LENGTH // 2 - txt_eve_l // 2
        txt_eve_y = START_EVE_Y + START_EVE_HEIGHT // 2 - txt_eve_h // 2

        self.__screen.fill(DARK)

        # Start PVP
        pygame.draw.rect(self.__screen, LIGHT, (START_PVP_X, START_PVP_Y, START_PVP_LENGTH, START_PVP_HEIGHT))
        self.__screen.blit(txt_pvp, (txt_pvp_x, txt_pvp_y))

        # Start PVE
        pygame.draw.rect(self.__screen, LIGHT, (START_PVE_X, START_PVE_Y , START_PVE_LENGTH, START_PVE_HEIGHT))
        self.__screen.blit(txt_pve, (txt_pve_x, txt_pve_y))

        # Start EVE
        pygame.draw.rect(self.__screen, LIGHT, (START_EVE_X, START_EVE_Y , START_EVE_LENGTH, START_EVE_HEIGHT))
        self.__screen.blit(txt_eve, (txt_eve_x, txt_eve_y))

        # Picture
        self.__screen.blit(PICTURE, (WIDTH // 2 - PICTURE.get_width() // 2, 20))

