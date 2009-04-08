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
import Step

class Evaluation(object):


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
        if color == 'w':
            for col in range(0,8):
                for row in range(0,8):
                    piece = board[row][col]
                    if piece.isupper():
                        value += Step.Step.pieceValue(piece)**2
                        if piece != 'R':
                            value += Step.Step.pieceValue(piece) * (row+1)
                        elif piece == 'R':
                            value += Step.Step.pieceValue(piece) * (row+1)**2

                    if piece.islower():
                        value -= Step.Step.pieceValue(piece)**2
        elif color == 'b':
            for col in range(0,8):
                for row in range(0,8):
                    piece = board[row][col]
                    if piece.islower():
                        value += Step.Step.pieceValue(piece)**2
                        if piece != 'r':
                            value += Step.Step.pieceValue(piece) * (row+1)
                        elif piece == 'r':
                            value += Step.Step.pieceValue(piece) * (row+1)**2

                    if piece.isupper():
                        value -= Step.Step.pieceValue(piece)**2
        return value
            

    ##
    # Computes a running average of piece values to narrow search space 
    # (a 5 x 5 grid is chosen to try to contain pieces that could 
    # potentially effect the area)
    # @param board - the current board state
    # @return the center of the strongest position for each player
    def boardStrength(self, board):
        
        # Copy the original boards.
        white = copy.deepcopy(board)
        black = copy.deepcopy(board)
        
        bestWhite = 0
        bestBlack = 0
        
        bestWhitePos = [0,0]
        bestBlackPos = [0,0]
        
        for row in range(0,len(board[0])):
            for col in range(0,len(board[0])):
                indices = [] #the indices of the moves concerned
                for x in range(-2,3): #subscript a 5x5 moving grid
                    for y in range(-2,3):
                        newRow = abs(row+x)
                        
			newCol = abs(col+y)
            
			if newRow > 7:
				newRow = newRow - 2
                
			if newCol > 7:
				newCol = newCol - 2
                
			indices.append([newRow, newCol])#take the absolute value to avoid going negative out of bounds
            white[row][col] = self.average(indices,25,board,1)
                
            if white[row][col] > bestWhite:
                bestWhite = white[row][col]
                bestWhitePos = [row,col]
            
            black[row][col] = self.average(indices,25,board,-1)
                
            if black[row][col] > bestBlack:
                bestBlack = black[row][col]
                bestBlackPos = [row,col]

        return [bestWhitePos, bestBlackPos]

    ##
    # Computes the average value of the given grid on the board
    # @param indices - the points to average
    # @param gridSize - the size of the grid being averaged
    # @param board - the board concerned
    # @param player - 1 for white, -1 for black
    # @return the averaged position state
    def average(self, indices,gridSize, board, player):
        total = 0
        for point in indices:
            piece  = board[point[0]][point[1]]
            if player == 1:
                if piece.isupper(): #white piece
                    total = total + Step.Step.pieceValue(piece)
            elif player == -1:
                if piece.islower(): #black piece
                    total = total + Step.Step.pieceValue(piece)
        return total / (gridSize * 1)
