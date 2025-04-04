import pygame
from .constants import SQUARE_SIZE, RED

class Move:
    def __init__(self, row, col, piece):
        self._row = row
        self._col = col
        self._x = SQUARE_SIZE * self._col + SQUARE_SIZE // 2
        self._y = SQUARE_SIZE * self._row + SQUARE_SIZE // 2
        self._piece = piece
    
    def copy(self, piece):
        return Move(self._row, self._col, piece)

    def draw(self, screen):
        radius = SQUARE_SIZE // 2 - 20
        pygame.draw.circle(screen, RED, (self._x, self._y), radius)
    
    def get_row_col(self):
        return self._row, self._col

    def get_piece(self):
        return self._piece
    
class Capture(Move):
    def __init__(self, row, col, piece, captured):
        super().__init__(row, col, piece)
        self.__captured = captured
    
    def copy(self, piece, captured):
        return Capture(self._row, self._col, piece, captured)
    
    def get_captured(self):
        return self.__captured
