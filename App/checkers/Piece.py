import pygame
from .constants import SQUARE_SIZE, WHITE, BLACK, CROWN, YELLOW

class Men:
    def __init__(self, row, col, color):
        self._row = row
        self._col = col
        self._color = color
        self._x = 0
        self._y = 0
        self._capture = False
        self._moves = []
        self._direction = [-1, -1, 1, 1]
        self._distance = 2
        self._promotion = 4.5
        self.calculate_position()
    
    def calculate_position(self):
        self._x = SQUARE_SIZE * self._col + SQUARE_SIZE // 2
        self._y = SQUARE_SIZE * self._row + SQUARE_SIZE // 2

    def copy(self):
        copy = Men(self._row, self._col, self._color)
        copy.set_moves([])
        return copy

    def add_moves(self, moves):
        self._moves += moves
    
    def set_moves(self, moves):
        self._moves = moves
    
    def set_capture(self, capture):
        self._capture = capture
    
    def move(self, row, col):
        self._row = row
        self._col = col
        self.calculate_position()

    def get_moves(self):
        return self._moves
    
    def get_row_col(self):
        return self._row, self._col
    
    def get_color(self):
        return self._color
    
    def get_capture(self):
        return self._capture
    
    def get_direction(self):
        return self._direction

    def get_distance(self):
        return self._distance
    
    def get_promotion(self):
        return self._promotion

    def draw(self, screen):
        radius = SQUARE_SIZE // 2 - 10
        if self._capture:
            pygame.draw.circle(screen, YELLOW, (self._x, self._y), radius+5)
        pygame.draw.circle(screen, self._color, (self._x, self._y), radius)

class BlackMen(Men):
    def __init__(self, row, col, direction):
        super().__init__(row, col, BLACK)
        self._direction = [direction * element for element in self._direction]
        self._promotion = int(self._promotion - direction * self._promotion)

    def copy(self):
        copy = BlackMen(self._row, self._col, self._direction[2])
        return copy
    
    def promote(self):
        return BlackKing(self._row, self._col)

class WhiteMen(Men):
    def __init__(self, row, col, direction):
        super().__init__(row, col, WHITE)
        self._direction = [direction * element for element in self._direction]
        self._promotion = int(self._promotion - direction * self._promotion)
    
    def copy(self):
        copy = WhiteMen(self._row, self._col, self._direction[2])
        return copy
    
    def promote(self):
        return WhiteKing(self._row, self._col)

class King(Men):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self._direction = [9, 9, 9, 9] 
        self._distance = 9
    
    def copy(self):
        copy = King(self._row, self._col, self._color)
        return copy
    
    def draw(self, screen):
        super().draw(screen)
        screen.blit(CROWN, (self._x - CROWN.get_width() // 2, self._y - CROWN.get_height() // 2))

class BlackKing(King):
    def __init__(self, row, col):
        super().__init__(row, col, BLACK)
    
    def copy(self):
        copy = BlackKing(self._row, self._col)
        return copy

class WhiteKing(King):
    def __init__(self, row, col):
        super().__init__(row, col, WHITE)
    
    def copy(self):
        copy = WhiteKing(self._row, self._col)
        return copy