from checkers.Move import Move, Capture
from checkers.Piece import Men
from constants import WHITE


lis = []
men1 = Men(0, 0, WHITE)
men2 = Men(0, 0, WHITE)
move1 = Move(0, 0, men1)
move2 = Capture(0, 0, men1, men2)

def add_move(lis: list, move: Move):
    lis.append(move)

add_move(lis, move1)
add_move(lis, move2)

for move in lis:
    print(type(move))