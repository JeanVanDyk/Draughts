import pygame
import random
import sys
from constants import WIDTH, HEIGHT, WHITE, BLACK
from game.WinGame import WinGamePVP, WinGamePVE
from winoption.WinOption import WinOption
from menu.WinMenu import WinMenu
from winwin.WinWin import WinWin

FPS = 60

# pygame setup
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')
    clock = pygame.time.Clock()
    running = True

    win = WinMenu(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                win.select(x, y)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    win.reset()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    win.menu() 

        message = win.update()
        clock.tick(FPS)

        if message == "GAME_PVP":
            win = WinGamePVP(screen)
        
        elif message == "GAME_PVE":
            win = WinOption(screen)
        
        elif message == "WHITE":
            win = WinGamePVE(screen, WHITE)
        
        elif message == "BLACK":
            win = WinGamePVE(screen, BLACK)
        
        elif message == "RANDOM":
            win = WinGamePVE(screen, random.choice([WHITE, BLACK]))
        
        elif message == "BLACK_WIN":
            win.update()
            win = WinWin(screen, BLACK)
        
        elif message == "WHITE_WIN":
            win.update()
            win = WinWin(screen, WHITE)
        
        elif message == "MENU":
            win = WinMenu(screen)

    pygame.quit()

main()