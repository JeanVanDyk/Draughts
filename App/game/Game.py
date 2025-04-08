from App.checkers.constants import BLACK, WHITE, SQUARE_SIZE
from App.checkers.Move import Move, Capture
from App.engine.Bot import GreedyBot
from App.checkers.Board import Board

class Game:
    def __init__(self, board: Board):
        self._turn = WHITE
        self._board = board
    
    def change_turn(self):

        # Change color
        if self._turn == WHITE:
            self._turn = BLACK
        else:
            self._turn = WHITE
        
        # Calculate legal moves for the next player
        self._board.calculate_legal_moves(self._turn)
       
        # Checking for a stalemate or a win
        if self._board.get_legal_moves() == []:
            if self._turn == WHITE:
                return "BLACK_WIN"
            return "WHITE_WIN"

        # Check if a men is up for a promotion
        self._board.promotion()
        
        return ""
    
    # Process the selection of a Move or a Capture
    def process(self, selection: Move):
        piece = selection.get_piece()
        
        # If the selection is a Capture
        if isinstance(selection, Capture):
            self._board.capture(selection)

            # If the piece can no longer capture, change turn
            if not piece.get_capture():
                return self.change_turn()
            return ""
        
        # If the selection is a Move
        else:
            self._board.move(selection)
            return self.change_turn()

    def reset(self):
        self._init()
    
    def get_turn(self):
        return self._turn
    
class Game_PVP(Game):
    def __init__(self, board: Board):
        super().__init__(board)

class Game_PVE(Game):
    def __init__(self, board: Board, color):
        super().__init__(board)
        self.__player = color
        if self.__player == WHITE :
            self.__bot_color = BLACK
        else:
            self.__bot_color = WHITE
        self.__bot = GreedyBot(self.__bot_color, self.__player)
        #  self.__bot = RandomBot()
    
    def play_bot(self):
        selection = self.__bot.get_move(self._board, 2)
        #  selection = self.__bot.get_move(self._board)
        return super().process(selection)
        
    def get_player(self):
        return self.__player

class Game_EVE(Game):  
    def __init__(self, board: Board, color):
        super().__init__(board)
        self.__color_bot1 = WHITE
        self.__color_bot2 = BLACK
        self.__depth = 2
        self.__bot1 = GreedyBot(self.__color_bot1, self.__color_bot2)
        self.__bot2 = GreedyBot(self.__color_bot2, self.__color_bot1)
    
    def play_bot(self):
        if self._turn == self.__color_bot1:
            selection = self.__bot1.get_move(self._board, self.__depth)
            return super().process(selection)

        selection = self.__bot2.get_move(self._board, self.__depth)
        return super().process(selection)
        
    def get_player(self):
        return self.__player