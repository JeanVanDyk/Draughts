import random
from App.checkers.constants import ROWS, COLS, WHITE, BLACK
from App.checkers.Board import Board
from App.checkers.Move import Move, Capture
from App.checkers.Stone import Stone
from App.checkers.Piece import Men, King

class Bot():
    def __init__(self):
        pass

class GreedyBot(Bot):
    def __init__(self, color, player):
        super().__init__()
        self._color = color
        self._player = player

    def get_move(self, board: Board, depth: int):

        moves = board.get_legal_moves()
        best_moves = []
        score = -100

        for move in moves:
            origin_boards = self.get_next_boards(board, move, self._player)
            for origin_board in origin_boards:
                score_temp = self.alpha_beta(origin_board, depth, -100, 100, self._player)
                if score_temp > score:
                    score = score_temp
                    best_moves = [move]
                elif score_temp == score:
                    best_moves.append(move)
        
        print("alpha_beta")
        print("score", score)
        print("best_moves", len(best_moves))
        
        best_move = random.choice(best_moves)
        return best_move
    
    def alpha_beta(self, board: Board, depth: int, alpha: int, beta: int, maximizing_player):
        
        # If we've hit target depth
        if depth == 0:
            return self.get_score_board(board)
        # Or if there are no legal moves
        elif board.get_legal_moves() == []:
            if maximizing_player:
                return -100
            else:
                return 100
        
        # If it's the bot's turn, we want to maximize the score
        if maximizing_player == self._color:
            value = -100
            moves = board.get_legal_moves().copy()
            while moves != [] and value < beta:
                move = moves.pop()
                childs = self.get_next_boards(board, move, self._player)
                for child in childs:
                    value = max(value, self.alpha_beta(child, depth - 1, alpha, beta, self._player))
                    if value >= beta:
                        break
                    alpha = max(alpha, value)
            return value
        
        # If it's not, we want to minimize the score
        else:
            value = 100
            moves = board.get_legal_moves().copy()
            while moves != [] and value > alpha:
                move = moves.pop()
                childs = self.get_next_boards(board, move, self._color)
                for child in childs:
                    value = min(value, self.alpha_beta(child, depth - 1, alpha, beta, self._color))
                    if value <= alpha:
                        break
                    beta = min(beta, value)
            return value

    # Get all the boards corresponding to the next turn with its corresponding move leading to it
    def get_next_boards(self, board: Board, move: Move, turn):

        next_boards = []
        next_board = board.copy()

        # Retrieving the related copied move from next_board
        move_copy = self.get_move_copy(move, next_board)

        # if it is a capture
        if isinstance(move_copy, Capture):
            next_board.capture(move_copy)
            piece = move_copy.get_piece()
            capture = piece.get_capture()

            next_boards += self.get_next_boards_seq(next_board, capture)

        else:
            next_board.move(move_copy)
            next_boards.append(next_board)

        for board in next_boards:
            board.calculate_legal_moves(turn)
            
        return next_boards
    
    def get_next_boards_seq(self, board: Board, capture: bool):
        seq_cap = [board]

        while capture:
            next_seq_cap = []

            # Getting all the boards leading to the end of the capture
            for board_seq in seq_cap:
                still_capturing = board_seq.get_legal_moves()
                for capture in still_capturing :
                    next_board = board_seq.copy()
                    capture_copy = self.get_move_copy(capture, next_board)
                    next_board.capture(capture_copy)
                    next_seq_cap.append(next_board)

            seq_cap = next_seq_cap

            # We get a board to test if capturing is still possible.
            # Doesn't matter which one since they all should have the same capturing sequence length
            test_board = seq_cap[0]
            if test_board.get_legal_moves() == []:
                capture = False
        
        return seq_cap

    
    # Get a board's move from the board's copy
    def get_move_copy(self, move: Move, board_copy: Board):

        # Getting its related piece position
        move_row, move_col = move.get_row_col()
        origin_piece = move.get_piece()
        piece_row, piece_col = origin_piece.get_row_col()

        # Getting the copied piece
        piece_copy = board_copy.get_selection(piece_row, piece_col)

        # Display its move so that the copied move is displayed on the board
        for move_copy in board_copy.get_legal_moves():
            if move_copy.get_row_col() == (move_row, move_col) and piece_copy == move_copy.get_piece():
                res = move_copy

        return res
    
    # Get the opposite color of a piece's related move played
    def get_opposite_color(self, piece: Men):
        previous_turn = piece.get_color()

        # Getting next turn's color if we need to change turn
        if previous_turn == WHITE:
            next_turn = BLACK
        else:
            next_turn = WHITE
        
        return next_turn
    
    # Get the score from the tree.
    # I've choose to do a recursion function since the maximum nb of recursive caal should be equal to the tree's depth
    def get_score(self, origin_board: Board, tree_board : dict[Board: Board], depth: int, turn):

        # If there are no legal moves, return the turn's victory score
        if origin_board.get_legal_moves() == []:
            if turn == self._color:
                return 100
            else:
                return -100

        # If get to the end, return the score of the board
        if depth <= 0 :
            return self.get_score_board(origin_board)
        
        # Else, return max score from each children board if it's bot's turn, min otherwise
        boards = tree_board[origin_board]

        if turn == self._color:
            score = -100
            for board in boards[:]:
                score = max(score, self.get_score(board, tree_board, depth - 1, self._player))
        else:
            score = 100
            for board in boards[:]:
                score = min(score, self.get_score(board, tree_board, depth - 1, self._color))
                
        return score

    # Get the score from a board
    def get_score_board(self, board: Board):
        score = 0

        # Checking every tile on the board
        for i in range(ROWS):
            for j in range(COLS):
                selection = board.get_selection(i, j)

                # If there is a Men/King on the tile, then update the score
                if isinstance(selection, Men):
                    score += self.get_score_selection(selection)
        
        return score
        
    # Get the score from a selection
    def get_score_selection(self, selection: Men):
        score = 0

        # Set the score as 1 if the piece is bot color, -1 otherwise
        if selection.get_color()  == self._color:
            score += 1
        else:
            score -= 1

        # If the piece is a King, multiply the score by 5   
        if isinstance(selection, King):
                score = score * 5
        
        return score

    # Return the turn of the board based on its legal moves
    def get_turn(self, board: Board):
        moves = board.get_legal_moves()
        move = moves[0]
        piece = move.get_piece()
        return piece.get_color()