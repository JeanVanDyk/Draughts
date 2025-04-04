import random
from checkers.constants import ROWS, COLS, WHITE, BLACK
from checkers.Board import Board
from checkers.Move import Move, Capture
from checkers.Stone import Stone
from checkers.Piece import Men, King

class Bot():
    def __init__(self):
        pass

class GreedyBot(Bot):
    def __init__(self, color, player):
        super().__init__()
        self._color = color
        self._player = player

    def get_move(self, board: Board, depth: int):
        tree_board ={board:[]}

        # We do a breadth first tree search
        i = 0
        origin_boards = [board]
        while i <= depth :
            next_origin_boards = []
            for origin_board in origin_boards:
                if i % 2 == 0:
                    next_boards, next_moves = self.get_next_boards(origin_board, self._player)
                    next_origin_boards += next_boards
                else:
                    next_boards, next_moves = self.get_next_boards(origin_board, self._color)
                    next_origin_boards += next_boards
                if i == 0:
                    available_moves = next_moves
                tree_board[origin_board] = next_boards
            origin_boards = next_origin_boards
            i += 1
        
        print("boards", len(tree_board))
        # Get the score and retrieve the best move
        score = - 100
        best_moves = []
        d1_boards = tree_board[board]
        d1_size = len(d1_boards)
        print("d1_size", d1_size)
        print("available_moves", len(board.get_legal_moves()))

        for i in range(d1_size):
            d1_board = d1_boards[i]
            score_temp = self.get_score(d1_board, tree_board, depth-1, self._color)

            if score_temp > score:
                score = score_temp
                best_moves = [available_moves[i]]
            elif score_temp == score:
                best_moves.append(available_moves[i])
        
        best_move = random.choice(best_moves)
        print("score", score)

        return best_move

    # Get all the boards corresponding to the next turn with its corresponding move leading to it
    def get_next_boards(self, board: Board, turn):

        moves = board.get_legal_moves()
        next_moves = []
        next_boards = []

        # Going through all the legal moves
        for move in moves:
            next_board = board.copy()

            # Retrieving the related copied move from next_board
            move_copy = self.get_move_copy(move, next_board)

            # if it is a capture
            if isinstance(move_copy, Capture):
                next_board.capture(move_copy)
                piece = move_copy.get_piece()
                capture = piece.get_capture()

                next_boards += self.get_next_boards_seq(next_board, capture)
                next_moves += [move for _ in range(len(next_boards))]

            else:
                next_board.move(move_copy)
                next_boards.append(next_board)
                next_moves.append(move)
        
        for board in next_boards:
            board.calculate_legal_moves(turn)
            
        return next_boards, next_moves
    
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