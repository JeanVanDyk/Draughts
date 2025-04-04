import pygame
from .constants import SQUARE_SIZE, GREY

class Stone:
    def __init__(self, row, col):
        self._row = row
        self._col = col
        self._x = 0
        self._y = 0
        self.calculate_position()
    
    def get_row_col(self):
        return self._row, self._col

    def calculate_position(self):
        self.__x = SQUARE_SIZE * self._col + SQUARE_SIZE // 2
        self.__y = SQUARE_SIZE * self._row + SQUARE_SIZE // 2

    def draw(self, screen):
        radius = SQUARE_SIZE // 2 - 10
        pygame.draw.circle(screen, GREY, (self.__x, self.__y), radius)
    
    def copy(self):
        return Stone(self._row, self._col)