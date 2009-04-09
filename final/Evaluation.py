'''
Filename: Evaluation.py
Description: Responsible for finding an optimal move based on
its evaluation function.

@author: Hristo Asenov, et, Paul Abbazia
'''

import Common
import MoveGenerator
import math
import copy
import string
import bisect
import Piece

class Evaluation(object):


    GRID_WIDTH = 3
    GRID_HEIGHT = 3

    def __init__(self):
      self.nextColor = string.maketrans("wb", "bw")
      self.hashkeysEvalsSteps = []
      self.evaluations = []

    ##
    # Negascout algorithm
    # @param depth - 
    # @param alpha -
    # @param beta
    # @param board
    # @param color
    # @param steps
    # @param count
    # @param hash
    # @return 
    def negascout(self, depth, alpha, beta, board, color, steps, count, hash):
	allsteps = steps
        if (depth == 0):
            eval = self.evaluate(board, color)#returns the strength value of the board 
            self.hashkeysEvalsSteps.append((hash.get_hashkey(),eval,steps)) 
            self.hashkeysEvalsSteps.sort() # warning !!! may not be the best way to do this !!!
            return (eval,allsteps)
        
        b = beta
        m= ""
	    
        turnList = []
        bestPos = self.boardStrength(board)
        
        # Create a 5 x 5 grid around the best possible position.
        lowRow = bestPos[0][0]-2
        lowCol = bestPos[0][1]-2
        highRow = lowRow + 4
        highCol = lowCol + 4
            
        # Ensure that 5x5 grid is within the correct bounds.
        if lowRow < 0:
            lowRow = 0
                
        if lowCol < 0:
            lowCol = 0
            
        if highRow > 7:
            highRow = 7
            
        if highCol > 7:
            highCol = 7
            
        # Construct a new MoveGenerator object for white and its board,
        # then generate all the possible moves.
        moveGen = MoveGenerator.MoveGenerator(count, color, board, hash)
        # moveGen.genMoves("", lowRow, lowCol, highRow, highCol)
        moveGen.genMoves("")
        
        # The list of possible moves is stored in moveGen.moveStepHashes
        # as a list of tuples of the form (the board, the steps taken
        # to get to that board, and hash key for that board).
        turnList = moveGen.moveStepHashes
	    
        if color == 'w': #white's turn
            print lowRow
            print lowCol
            print highRow
            print highCol
   
        elif color == 'b': #black's turn
            pass


        for turn in turnList:
            newBoardState = turn[0]
            stepPerBoard = turn[1]
            hashForBoard = turn[2]
            
	        # reset from initial board hash to new board hash
            hash.resetInitialHashKey(hashForBoard)
            
            currentHashKeys = map(lambda x: x[0], self.hashkeysEvalsSteps)
            
            ins_pt = bisect.bisect_left(currentHashKeys, hashForBoard)
        
            if len(currentHashKeys) == ins_pt or hashForBoard != currentHashKeys[ins_pt]:
	        # original entry, need to reevaluate
            
                # descend one level and invert the function
                (a,m) = self.negascout(depth - 1, -b, -alpha, newBoardState, string.translate(color, self.nextColor), stepPerBoard, count, hash)
            else:
                # already got the evaluation of it, just return the evaluated value
                (a,m) = (self.hashkeysEvalsSteps[ins_pt][1],self.hashkeysEvalsSteps[ins_pt][2])
            
	    a = a * -1

            allsteps = m + " | " + allsteps
            
	    # alpha-beta pruning
	    if a > alpha:
	      alpha = a
          
	    if alpha >= beta:
	      return (alpha,m)
      
	    if alpha >= b:
	      (alpha,m) = self.negascout(depth - 1, -beta, -alpha, newBoardState, string.translate(color, self.nextColor), stepPerBoard, count, hash)
	      alpha = alpha * -1
            
            if alpha >= beta:
	      allsteps = m + " | " + allsteps
              return (alpha,allsteps)
          
            b = alpha + 1
            
        return (alpha,allsteps)    

    ##
    # Evaluates the given board based on set criteria
    # Board value is given by:
    #       - Player gains pieceValue * distance across 
    #         board for all pieces except rabbits
    #       - Player gains pieceValue * distance ^ 2 for rabbits
    #       - Player 'gains' sum of square of own pieces - sum of square enemy pieces
    # @param board - the board state to evaluate
    # @return the value of this board state
    def evaluate(self, board, color):
        
        value = 0
        

        for row in range(0, 8):
            for col in range (0, 8):
                piece = board[row][col]
                    
                    
                # Add the rabbits value to the current value.
                # If it's my own rabbit, then I add rabbit value ^ 2
                # to the current value. If it's my opponent's rabbit,
                # then I subtract the opponent's rabbit value from
                # the current value.
                if (piece == "R" or piece == "r"):
                    if self.myPiece(piece, color):
                        value = value + self.getRabbitValue(row, color)
                    else:
                        value = value - self.getRabbitValue(row, color)
                else:
                    
                    # else, just add the piece value to value.
                    if self.myPiece(piece, color):                    
                        value = value + Piece.Piece.pieceValue(piece) * 2
                    else:
                        value = value + Piece.Piece.pieceValue(piece) * 2
                    
                    
        
        return value
    
    def myPiece(self, piece, color):
        if piece.isupper and (color == "w" or color == "g"):
            return True
        elif piece.islower and (color == "b" or color == "s"):
            return True
        else:
            return False
    
    ##
    # Gets the value of the rabbit determined
    # by how far it is across the board.
    # The smallest value a rabbit can have in this
    # evaluation is 2.
    # For example, if the user has a black rabbit at row 0,
    # the rabbit's value is 2 ^ (row + 1) = 2
    # But if black's rabbit is at row 6 (one move from getting in the goal),
    # then it's value is 2 ^ (row + 1) = 128.
    # So as the rabbit progresses further down the board,
    # it's value gets exponentially bigger.
    def getRabbitValue(self, row, color):
        
        rabbitValue = Piece.Piece.pieceValue("r") * 2
        
        if color == "w" or color == "g":
            rabbitValue = rabbitValue ** (len(board) - row)
        elif color == "b" or color == "s":
            rabbitValue = rabbitValue ** (row + 1)
            
        return rabbitValue
            

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
                total = self.calculateGridValue(row, col, board, color)
                if total > highestValue:
                    best_pos = [row, col]
                    highestValue = total
  
        return best_pos


    ##
    # Computes the value of the grid given a position.
    # This is taken from a receiving a position and
    # adding up the strength values of the pieces around it.
    # @param row_pos - the row position.
    # @param col_pos - the column position
    # @param board - the board state currently
    # @param color - whose turn it is.
    # @return the value of the grid
    def calculateGridValue(self, row_pos, col_pos, board, color):
        
        total = 0
        
        for row in range (row_pos, row_pos + Evaluation.GRID_WIDTH):
            for col in range (col_pos, col_pos + Evaluation.GRID_HEIGHT):
                
                if row < len(board) and col < len(board):
                
                    piece = board[row][col]
                    
                    if color == "w" or color == "g":
                        if piece.isupper():
                            total = total + Piece.Piece.pieceValue(piece)
                    elif color == "b" or color == "s":
                        if piece.islower():
                            total = total + Piece.Piece.pieceValue(piece)
                            
        return total
