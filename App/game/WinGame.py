import pygame
import random
from App.constants import WHITE, BLACK
from App.checkers.Board import Board
from App.checkers.Piece import Men
from App.checkers.Move import Move
from App.game.Game import Game, Game_PVP, Game_PVE
from App.utils import get_row_col_from_mouse

class WinGame:
    def __init__(self, screen):
        self.__init()
        self._screen = screen

    def __init(self):
        self._board = Board(WHITE)
        self._game = Game(self._board)
        self._message = ""
    
    def update(self):
        self._board.draw(self._screen)
        pygame.display.flip()
        return self._message

    def reset(self):
        self.__init()
    
    def menu(self):
        self._message = "MENU"
    
    def select(self, x, y):   
        row, col = get_row_col_from_mouse(x, y)
        selection = self._board.get_selection(row, col)

        # Reset the already displayed legal moves
        self._board.reset_displayed_moves()

        # Checking if the selection is a Men (or a King)
        if isinstance(selection, Men):
            self._board.set_displayed_moves(selection)

        # Making a move and updating the game
        elif isinstance(selection, Move):
            self._message = self._game.process(selection)


class WinGamePVP(WinGame):
    def __init__(self, screen):
        super().__init__(screen)
        self._game = Game_PVP(self._board)
    
    def reset(self):
        super().reset()
        self._game = Game_PVP(self._board)

class WinGamePVE(WinGame):
    def __init__(self, screen, color):
        super().__init__(screen)
        self._board = Board(color)
        self._game = Game_PVE(self._board, color)
    
    def reset(self):
        super().reset()
        color = random.choice([WHITE, BLACK])
        self._game = Game_PVE(self._board, color)
    
    def select(self, x, y):
        if self._game.get_turn() == self._game.get_player():
            super().select(x, y)
        else :
            self._message = self._game.play_bot()