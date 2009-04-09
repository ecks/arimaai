'''
Filename: Evaluation.py
Description: Finds best starting grid to generate moves.
It also evaluates a board's value.

@author: et
'''

import Piece
import Board
import re
import Values

class Evaluation(object):


    GRID_WIDTH = 3
    GRID_HEIGHT = 3

    def __init__(self):
        pass

    ##
    # Evaluates the given board based on set criteria
    # @param board - the current board state
    # @param color - the person whose turn it is.
    # @return the value of this board state
    def evaluateBoard(self, board, color, start_row = 0, start_col = 0, end_row = 7, end_col = 7):
        
        value = 0
        

        for row in range(start_row, end_row + 1):
            for col in range (start_col, end_row + 1):
                piece = board[row][col]
                    
                
                value = value + self.__getMaterialValue(board, color, piece)
                value = value + self.__getPositionValue(color, piece, row, col)
                    
        
        return value
    
    
    ##
    # Determines the best 3 x 3 grid to construct a
    # search space.
    # @param board - the current board state
    # @param color - the person's color.
    # @return best_pos - the best position to construct a search of.
    def strongestPosition(self, board, color):

        best_pos = [0,0]
        highestValue = 0
        
        
        for row in range(0, len(board) - Evaluation.GRID_WIDTH):
            for col in range (0, len(board) - Evaluation.GRID_HEIGHT):
                total = self.evaluateBoard(board, color, row, col, row + Evaluation.GRID_WIDTH, col + Evaluation.GRID_HEIGHT)
                if total > highestValue:
                    best_pos = [row, col]
                    highestValue = total
  
        return best_pos
    
    
    def __getMaterialValue(self, board, color, piece):
        
        value = 0
        
        if re.match("e", piece, re.IGNORECASE):     # Elephant
            value = 1800
        elif re.match("m", piece, re.IGNORECASE):   # Camel
            value = 1100
        elif re.match("h", piece, re.IGNORECASE):   # Horse
            value = 600
        elif re.match("d", piece, re.IGNORECASE):   # Dog
            value = 300
        elif re.match("c", piece, re.IGNORECASE):   # Cat
            value = 250
        elif re.match("r", piece, re.IGNORECASE):   # Rabbit
            
            num_rabbits_left = 0
            
            for row in range (len(board)):
                for col in range(len(board)):
                    cur_piece = board[row][col]
                    if cur_piece == piece:
                        num_rabbits_left = num_rabbits_left + 1
            
            if num_rabbits_left == 8:
                value = 100
            elif num_rabbits_left == 7:
                value = 150
            elif num_rabbits_left == 6:
                value = 200
            elif num_rabbits_left == 5:
                value = 250
            elif num_rabbits_left == 4:
                value = 300
            elif num_rabbits_left == 3:
                value = 400
            elif num_rabbits_left == 2:
                value = 500
            elif num_rabbits_left == 1:
                value = 1200
                
        return value 
    
    def __getPositionValue(self, color, piece, row, col):
        
        if color == "b":
            row = 7 - row
            col = 7 - col
        
        value = 0
        
        if re.match("e", piece, re.IGNORECASE):     # Elephant
            value = Values.elephant_pos_values[row][col]
        elif re.match("m", piece, re.IGNORECASE):   # Camel
            value = Values.camel_pos_values[row][col]
        elif re.match("h", piece, re.IGNORECASE):   # Horse
            value = Values.horse_pos_values[row][col]
        elif re.match("d", piece, re.IGNORECASE):   # Dog
            value = Values.dog_pos_values[row][col]
        elif re.match("c", piece, re.IGNORECASE):   # Cat
            value = Values.cat_pos_values[row][col]
        elif re.match("r", piece, re.IGNORECASE):   # Rabbit
            value = Values.rabbit_pos_values_normal[row][col]
            
            
        return value
    
    
    ##
    # This determines a value to give to this
    # piece if it has pieces frozen.
    # @param board - the current board state
    # @param row - the piece's row position
    # @param col - the piece's column position
    # @param piece - the piece
    # @param value - the value of this piece.
    def __hasPiecesFrozen(self, board, row, col, piece):
                
        value = 0
        piecesFrozen = 0
        
        # Generate all the occupied adjacent positions.
        adj_occ_pos = Board.getAdjacentPositions(board, row, col, True)
        for pos in adj_occ_pos:
            adj_row = pos[0]
            adj_col = pos[1]
            adj_piece = board[adj_row][adj_col]
            
            # Make sure you're not looking at piece that
            # you're friends with.
            if not Piece.areFriends(piece, adj_piece):
                
                # If you're stronger than the adjacent piece,
                # then you've frozen it.
                if Piece.isStronger(piece, adj_piece):
                    piecesFrozen = piecesFrozen + 1

        
        # Return a value now based on the number of pieces frozen.
        # If it has too many pieces frozen, then it has potential
        # to being trapped. So it needs to be careful.
        if piecesFrozen == 1:
            value = 100
        elif piecesFrozen == 2:
            value = 1000
        elif piecesFrozen == 3:
            value = -100
        if piecesFrozen == 4:
            value = -1000
            
        return value
