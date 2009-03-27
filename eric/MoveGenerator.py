'''
Filename: MoveGenerator.py
Description: Generates all the possible moves given a board state.

@author: et
'''

import string
import re

class MoveGenerator(object):

    ##
    # MoveGenerator constructor
    # @param count - the turn number
    # @param color - whose turn is it (white or black)
    # @param steps - the steps taken so far
    # @param board - the parsed board, 2 dimensional array.
    def __init__(self, count, color, steps, board):
        self.count = count
        self.color = color
        self.steps = steps
        self.board = board
        
        # Going to need to hold onto the original board
        # state because we're going to making a lot of
        # new boards.
        self.original_board = board
        
    ##
    # Generates all possible moves for each piece.
    # @return moves - a list of moves (a move is a list of steps)
    def genMoves(self):
        
        moves = []
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                # Don't care for blank spaces or trap squares
                if piece == " " or re.match("x", piece, re.IGNORECASE):
                    continue
                                
                piece_color = self.__pieceColor(piece)
                
                # Only generate moves for the current player
                if piece_color == self.color:
                    # Get all the valid adjacent positions to this piece
                    adj_pos = self.__getAdjacentPieces(row, col)
                    
                    # Is the piece NOT frozen
                    if self.__isFrozen(piece, adj_pos) == False:
                        steps = self.__makeStep(piece, row, col, adj_pos)
                        moves.append(steps)
                
        
        print moves
                    
                    
                
    ##
    # Piece info returns the piece and it's color (white or black)
    # based on whether it's upper case or lower case.
    # If it's a blank space, color is returned as nothing.
    # @param piece - the piece
    # @return color - the piece's color            
    def __pieceColor(self, piece):
        if piece == " ":
            color = " "
        elif piece.isupper():
            color = "w"
        else:
            color = "b"
        
        return color
    
    ##
    # Returns whether this piece is frozen.
    # @param piece - the piece
    # @param adj_pos - the adjacent positions to this piece
    # @return True if the piece is frozen, False otherwise
    def __isFrozen(self, piece, adj_pos):
        for pos in adj_pos:
            adj_row = pos[0]
            adj_col = pos[1]
            adj_piece = self.board[adj_row][adj_col]
            if adj_piece == " ":
                continue
            elif self.__isStronger(adj_piece, piece):
                return True
        
        return False
        
    ##
    # Returns all the adjacent positions (not the actual
    # pieces themselves) to this piece that are empty.
    # Basically the positions north, south, east and west of this piece
    # only if it's still on the board
    # @param row - the piece's row
    # @param col - the pieces's column
    # @return pieces - the positions adjacent to this piece
    def __getAdjacentPieces(self, row, col):
        
        pieces = []
        
        # North
        if row - 1 >= 0 and re.match(" |x", self.board[row-1][col], re.IGNORECASE):
            pieces.append([row - 1, col])
        
        # South
        if row + 1 <= 7 and re.match(" |x", self.board[row+1][col], re.IGNORECASE):
            pieces.append([row + 1, col])
        
        # West
        if col - 1 >= 0 and re.match(" |x", self.board[row][col-1], re.IGNORECASE):
            pieces.append([row, col - 1])
        
        # East
        if col + 1 <= 7 and re.match(" |x", self.board[row][col+1], re.IGNORECASE):
            pieces.append([row, col + 1])
        
        return pieces
    
    ##
    # Returns whether or not the first piece
    # is stronger than the second piece.
    # @param a - the first piece
    # @param b - the second piece
    # @return True if the a is stronger than b, False otherwise
    def __isStronger(self, a, b):
        a = self.__pieceValue (a)
        b = self.__pieceValue (b)
        return (a > b) 
        pass
    
    ##
    # Returns the strength value of a given piece.
    # @param piece - the piece
    # @param strength - the piece's strength
    def __pieceValue(self, piece):
        piece = piece.lower()   # Make the piece lowercase.
        
        # Make the translation table for strengths
        transTable = string.maketrans("emhdcrx", "6543210")  
        strength = string.translate(piece, transTable)  # Translate the piece
        return strength
    
    ##
    # Constructs a step in proper notation
    # given a list of positions a piece can move into.
    # @param piece - the piece to move
    # @param row - the piece's current row
    # @param col - the piece's current column
    # @param adj_pos - the list of adjacent positions to move into.
    def __makeStep(self, piece, row, col, adj_pos):
        
        steps = []
        
        for pos in adj_pos:
            
            piece_row = row
            piece_col = col
            
            adj_row = pos[0]
            adj_col = pos[1]
            
            # Moving north
            if adj_row < piece_row:
                dir = "n"
            
            # Moving south
            elif adj_row > piece_row:
                dir = "s"
            
            # Moving west
            elif adj_col < piece_col:
                dir = "w"
            
            # Moving east
            elif adj_col > piece_col:
                dir = "e"
            
            
            # Arimaa notation starts at 1, not 0
            piece_row = piece_row + 1
            piece_col = piece_col + 1
            
            # Arimaa notation for rows is flipped upside down.
            piece_row = 9 - piece_row
            
                
            # Make the translation table for columns
            transTable = string.maketrans("12345678", "abcdefgh")
            piece_col_letter = string.translate(repr(piece_col), transTable)  # Translate the column
            
            step = piece + piece_col_letter + repr(piece_row) + dir
            
            steps.append(step)
        
        return steps
        
        
        
        
        