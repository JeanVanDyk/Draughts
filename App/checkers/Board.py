import pygame
from .constants import ROWS, COLS, SQUARE_SIZE, DARK, LIGHT, WHITE, BLACK
from .Piece import Men, BlackMen, WhiteMen, King, BlackKing, WhiteKing
from .Move import Move, Capture
from .Stone import Stone

class Board:
    
    def __init__(self, color):

        self.__displayed_moves = []       # Legal moves displayed on the board
        self.__legal_moves = []           # Legal moves available to play
        self.__stones = []                # Stones displayed
        self.__nb_captures = 0            # Number of captures possible
        self.__color = color              # Color of the first player
        
        # Initialisation of the board
        self.__board = {(i, j): None for i in range(ROWS) for j in range(COLS)}
        self.normal_board(color)

        # initialisation of legal moves
        self.calculate_legal_moves(WHITE)
    
    # Calculate all legal moves and the piece that can capture from the board
    def calculate_legal_moves(self, color):

        # Reset the available moves
        self.__legal_moves = []
        self.__nb_captures = 0
        pieces_processed = [] 

        # Check all pieces across the board
        for i in range(ROWS):
            for j in range(COLS):
                piece = self.__board[i, j]
                
                if isinstance(piece, Men) and piece.get_color() == color:
                    nb_captures, moves = self.get_moves(piece)

                    # If the piece can capture more than any before, update the board's legal moves
                    if nb_captures > self.__nb_captures:
                        self.__nb_captures = nb_captures
                        piece.set_moves(moves)
                        piece.set_capture(True)

                        # Removing the moves of the other pieces
                        for piece_processed in pieces_processed:
                            piece_processed.set_moves([])
                            piece_processed.set_capture(False)

                        # Updating the legal moves
                        self.__legal_moves = []
                        self.__legal_moves += moves
                        pieces_processed = [piece]

                    # If the piece can capture as much as the previous ones
                    elif nb_captures == self.__nb_captures:
                        piece.set_moves(moves)
                        self.__legal_moves += moves
                        pieces_processed += [piece]
                        
                        if nb_captures > 0:
                            piece.set_capture(True)
                
                elif isinstance(piece, Men) and piece.get_color() != color:
                    piece.set_moves([])
                    piece.set_capture(False)
                
    # Get the legal moves for a Men or a King
    def get_moves(self, piece):
        direction = piece.get_direction()               # Diagonal to which the piece can move
        distance = piece.get_distance()                 # Distance to which the piece can move in a leap (2 for Men, 9 for King)
        row, col = piece.get_row_col()                  # Position of the piece
        board = self.__board                            # Board
        moves = []                                      # All moves that lead to the maximum number of capture
        captured = [(-1, -1) for _ in range(4)]         # Where the captured piece is
        open_diagonal = [True, True, True, True]        # Which diagonal we should still check for positions to go to
        capturing = [False, False, False, False]        # If we've already encounter a piece of an opposite color in each diagonal
        max_nb_captures = 0                             # Maximum number of captures at each point
        i = 1                                           # Distance to which we're looking at

        # If there is still a diagonal worth looking at
        while open_diagonal != [False, False, False, False]:
            
            bottom_right = (row + i, col + i)
            bottom_left = (row + i, col - i)
            top_right = (row - i, col + i)
            top_left = (row - i, col - i)
            potential_moves = [bottom_right, bottom_left, top_right, top_left]

            for j in range(4):

                # Check if the corresponding diagonal is open and if the distance is not too far
                if open_diagonal[j] and i <= distance:

                    # Check if the position is in the board
                    if potential_moves[j] in board:

                        # Check if there is a piece on the tile of an opposite color
                        if isinstance(board[potential_moves[j]], Men) and board[potential_moves[j]].get_color() != piece.get_color():
                            if capturing[j]:
                                open_diagonal[j] = False
                            else :
                                capturing[j] = True
                                captured[j] = potential_moves[j]

                        # Check if the tile is empty
                        elif isinstance(board[potential_moves[j]], type(None)) :
                            
                            # If it corresponds to a capture
                            if capturing[j] :
                                # Making copies for the recursion to work with an updated board
                                updated_pieces = board.copy()
                                updated_piece = piece.copy()

                                # Updating the board and piece
                                updated_piece.move(potential_moves[j][0], potential_moves[j][1])
                                updated_pieces[potential_moves[j]] = updated_piece
                                updated_pieces[captured[j]] = Stone(captured[j][0], captured[j][1])
                                updated_pieces[row, col] = None

                                # Making the recursive call
                                nb_captures = self.get_captures(updated_pieces, updated_piece, 0) + 1

                                # Check the number of capture from this point to force the player to play the longest capturing sequence
                                if nb_captures > max_nb_captures:
                                    max_nb_captures = nb_captures
                                    moves = [Capture(potential_moves[j][0], potential_moves[j][1], piece, self.__board[captured[j]])]
                                elif nb_captures == max_nb_captures:
                                    moves.append(Capture(potential_moves[j][0], potential_moves[j][1], piece, self.__board[captured[j]]))   

                            # If it doesn't correspond to a capture and it's in your direction
                            elif max_nb_captures == 0 and i <= direction[j] :
                               moves.append(Move(potential_moves[j][0], potential_moves[j][1], piece))

                        # Closing the diagonal if there is a piece on the tile of the same color or a Stone
                        else :
                            open_diagonal[j] = False
                    
                    # Closing the diagoanl if the position is not on the board
                    else :
                        open_diagonal[j] = False
                
                # Closing the diagonal if the distance is too far
                else :
                    open_diagonal[j] = False
            
            i += 1
        return max_nb_captures, moves

    def get_captures(self, pieces, piece, nb_captures):
        
        distance = piece.get_distance()
        row, col = piece.get_row_col()
        color = piece.get_color()
        open_diagonal = [True, True, True, True]
        capturing = [False, False, False, False]
        captured = [(-1, -1) for _ in range(4)]
        max_nb_captures = nb_captures
        i = 1

        # While there is still a diagonal to look at
        while open_diagonal != [False, False, False, False]:
            
            bottom_right = (row + i, col + i)
            bottom_left = (row + i, col - i)
            top_right = (row - i, col + i)
            top_left = (row - i, col - i)
            potential_moves = [bottom_right, bottom_left, top_right, top_left]

            for j in range(4):

                # Check if the corresponding diagonal is open
                if open_diagonal[j] and i <= distance:

                    # Check if the position is in the board
                    if potential_moves[j] in pieces:

                        # Check if there is a piece on the tile of an opposite color
                        if isinstance(pieces[potential_moves[j]], Men) and pieces[potential_moves[j]].get_color() != piece.get_color():
                            if capturing[j]:
                                open_diagonal[j] = False
                            else :
                                capturing[j] = True
                                captured[j] = potential_moves[j]

                        # Check if the tile is empty and if it corresponds to a capture
                        elif isinstance(pieces[potential_moves[j]], type(None)) and capturing[j] :

                                # Making copies for the recursion to work with an updated board
                                updated_pieces = pieces.copy()
                                updated_piece = piece.copy()


                                # Updating the board and piece
                                updated_piece.move(potential_moves[j][0], potential_moves[j][1])
                                updated_pieces[potential_moves[j]] = updated_piece
                                updated_pieces[captured[j]] = Stone(captured[j][0], captured[j][1])
                                updated_pieces[row, col] = None

                                # Making the recursive call
                                temp = self.get_captures(updated_pieces, updated_piece, nb_captures + 1)
                                max_nb_captures = max(max_nb_captures, temp)

                        # Closing the diagonal if there is a piece on the tile of the same color
                        elif isinstance(pieces[potential_moves[j]], Men) and  pieces[potential_moves[j]].get_color() == color :
                            open_diagonal[j] = False
                        
                        # Closing the diagonal if there is a Stone
                        elif isinstance(pieces[potential_moves[j]], Stone):
                            open_diagonal[j] = False
                    
                    # Closing the diagoanl if the position is not on the board
                    else :
                        open_diagonal[j] = False

                # Closing the diagonal if the distance is too far
                else :
                    open_diagonal[j] = False
            i += 1
        return max_nb_captures        
                      
    # Update the board after a move
    def move(self, selection: Move):
        row, col = selection.get_row_col()
        piece = selection.get_piece()

        # Updating the board
        self.set_none([piece])
        self.set_piece(row, col, piece)

        # Updating the piece's position
        piece.move(row, col)
    
    # Update the board after a capture
    def capture(self, capture: Capture):

        # Cleaning the board from the displayed moves
        self.reset_displayed_moves()

        # Moving the piece to its new location
        self.move(capture)

        # Putting up the stone over the captured piece
        captured = capture.get_captured()
        self.set_stone(captured)

        # Getting the new available moves of the piece
        piece = capture.get_piece()
        self.__nb_captures, moves = self.get_moves(piece)

        # If the piece can capture again, it has to
        if self.__nb_captures > 0:

            # Updating the piece's state
            piece.set_moves(moves)
            piece.set_capture(True)

            # Display the new moves 
            self.set_displayed_moves(piece)

            # Making the legal moves equal to the piece's moves
            self.__legal_moves = piece.get_moves()

        # If the piece can no longer capture, change turn and erase the stones
        else:
            piece.set_capture(False)
            self.reset_stones()
            self.__legal_moves = []
    
    # Checks the first and last rank for an available promotion
    def promotion(self):
        for i in range(ROWS):
            # First rank
            top_piece = self.__board[(0, i)]
            if isinstance(top_piece, Men) and top_piece.get_promotion() == 0 :
                self.promote(top_piece)
            # Last rank
            bot_piece = self.__board[(ROWS - 1, i)]
            if isinstance(bot_piece, Men) and bot_piece.get_promotion() == ROWS - 1 :
                self.promote(bot_piece)
                
    # Promote a piece
    def promote(self, piece: Men):
        bot_row, bot_col = piece.get_row_col()
        self.__board[(bot_row, bot_col)] = piece.promote()
    
    # Add legal move
    def add_legal_move(self, move: Move):
        self.__legal_moves.append(move)
    
    # Add a stone
    def add_stone(self, stone: Stone):
        row, col = stone.get_row_col()
        self.__board[row, col] = stone
        self.__stones.append(stone)

    # Return the legal moves available at this time    
    def get_legal_moves(self):
        return self.__legal_moves
    
    # Return what's on the board at the givzn coordinates
    def get_selection(self, row: int, col: int):
        return self.__board[row, col]
    
    # Return a copy of the board
    def get_board(self):
        return self.__board.copy()
    
    # Update the list of displayed moves and put them on the board
    def set_displayed_moves(self, piece: Men):
        self.__displayed_moves = piece.get_moves()
        self.set_list(self.__displayed_moves)
    
    # Update the list of legal moves with a new one
    def set_legal_moves(self, lis: list[Move]):
        self.__legal_moves = lis
    
    # Replace each element of a List with None on the board
    def set_none(self, lis: list):
        for el in lis :
            row, col = el.get_row_col()
            self.__board[row, col] = None
    
    # Take a piece and put it at the designated row and col
    def set_piece(self, row: int, col: int, piece):
        self.__board[row, col] = piece
    
    # Take a list of element with a method "get_row_col", and put them on the board at their corresponding coordinates
    def set_list(self, lis: list):
        for el in lis:
            row, col = el.get_row_col()
            self.__board[row, col] = el
    
    # Put a stone on the board at the desiganted row and col
    def set_stone(self, captured: Men):
        row, col = captured.get_row_col()
        stone = Stone(row, col)
        self.__board[row, col] = stone
        self.__stones.append(stone)
    
    # Empty the board from the displayed moves and empty the list of displayed moves
    def reset_displayed_moves(self):
        self.set_none(self.__displayed_moves)           
        self.__displayed_moves = []
    
    # Empty the board from the stones and empty the list of stones
    def reset_stones(self):
        self.set_none(self.__stones)
        self.__stones = []
    
    def normal_board(self, color):
        if color == WHITE:
            for i in range(ROWS):
                for j in range(1 - i % 2, COLS, 2):
                    if i < 4 :
                        self.__board[i, j] = BlackMen(i, j, -1)
                    if i > 5 :
                        self.__board[i, j] = WhiteMen(i, j, 1)
        else:
            for i in range(ROWS):
                for j in range(1 - i % 2, COLS, 2):
                    if i < 4 :
                        self.__board[i, j] = WhiteMen(i, j, -1)
                    if i > 5 :
                        self.__board[i, j] = BlackMen(i, j, 1)
    
    def copy(self):

        # Erasing the displayed moves on the board
        self.reset_displayed_moves()

        # Defining the new board
        board_copy = Board(self.__color)
        board_copy.set_legal_moves([])

        # Copying the pieces on the board
        for i in range(ROWS):
            for j in range(COLS):
                selection = self.get_selection(i, j)

                # Copy the pieve onto the new board
                if isinstance(selection, Men):
                    selection_copy = selection.copy()
                    board_copy.set_piece(i, j, selection_copy)
                
                # If it is a stone, add it to the list of copied stones
                elif isinstance(selection, Stone):
                    selection_copy = selection.copy()
                    board_copy.add_stone(selection_copy)

                # Otherwise, the tile is empty
                else:
                    board_copy.set_piece(i, j, selection)
        
        
        # Copying the legal moves
        for move in self.__legal_moves:

            # Getting the piece linked to the move on the copied board
            row, col = move.get_piece().get_row_col()
            piece = board_copy.get_selection(row, col)

            # If it is a capture, we need to retrieve also the copied captured piece
            if isinstance(move, Capture):

                # Getting the copied captured piece
                captured = move.get_captured()
                captured_row, captured_col = captured.get_row_col()
                captured_copy = board_copy.get_selection(captured_row, captured_col)

                # Making the copy
                move_copy = move.copy(piece, captured_copy)

                # Add the copy to its related piece
                piece.add_moves([move_copy])
            
            # Otherwise, it is a simple move
            else:
                move_copy = move.copy(piece)

                # Add the copy to its related piece
                piece.add_moves([move_copy])

            # Adding the move to the list of legal moves
            board_copy.add_legal_move(move_copy)

        return board_copy

    
    def kings_board(self):
        self.__board[0,0] = BlackKing(0,0)
        self.__board[5,5] = WhiteKing(5,5)
        self.__board[7,5] = WhiteKing(7,5)
        self.__board[9,5] = WhiteKing(9,5)
        self.__board[5,7] = WhiteKing(5,7)
        self.__board[3,5] = WhiteMen(3,5,1)
        self.__board[1,7] = WhiteMen(1,7,1)
    
    def draw_board(self):
        self.__board[6,9] = BlackMen(6,9,-1)
        self.__board[7,8] = WhiteKing(7,8)
        self.__board[9,8] = WhiteMen(9,8,1)
              

    def draw_squares(self, screen):
        screen.fill(DARK)
        for i in range(ROWS):
            for j in range(i % 2, COLS, 2):
                pygame.draw.rect(screen, LIGHT, (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def draw(self, screen):
        self.draw_squares(screen)
        for i in range(ROWS):
            for j in range(COLS):
                if self.__board[i, j] != None:
                    self.__board[i, j].draw(screen)
