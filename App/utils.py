from checkers.constants import SQUARE_SIZE

def get_row_col_from_mouse(x, y):
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col