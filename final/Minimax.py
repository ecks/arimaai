'''
Filename: Minimax.py
Description: Responsible for finding an optimal move based on
its evaluation function.

@author: Eric Thomas
'''

import Evaluation
import MoveGenerator
import string
import Common
import bisect

class Minimax(object):

    ##
    # Constructor Minimax
    def __init__(self, board, color):
        self.hashkeysEvalsSteps = []
        self.evaluations = []
        
        self.eval = Evaluation.Evaluation()

        (self.start_row, self.start_col, self.end_row, self.end_col) = self.eval.getStrongestGrid(board, color)
        #print "start row: " + str(self.start_row)
        #print "start col: " + str(self.start_col) 
        #print "end row: " + str(self.end_row)
       # print "end col: " + str(self.end_col)

#        self.start_row = 0
#        self.start_col = 0
#        self.end_row = 7
#        self.end_col = 7
    



    def minimax(self, depth, board, color, steps, count, hash):
        return self.maxmove(depth, board, color, steps, count, hash, (99999999,steps,board) , (-99999999,steps,board))

    def maxmove(self, depth, board, color, steps, count, hash, alpha, beta):
        if (depth == 0):
            strength = self.eval.evaluateBoard(board, color, True)
	    return (strength,steps,board)

        else:
            best_move = (-999999,steps,board)
            moveGen = MoveGenerator.MoveGenerator(count, color, board, hash)
            moveGen.genMoves("")
            turnList = moveGen.moveStepHashes

            for turn in turnList:
                newBoardState = turn[0]
                stepPerBoard = turn[1]   
       
                if depth == 1:
		  newColor = color
		else:
                  if color == "w":
                     newColor = "b"
                  else:
                     newColor = "b"

                temp = self.minmove(depth - 1, newBoardState, newColor, stepPerBoard, count, hash, alpha, beta)
      
                if temp > best_move:
                    best_move = temp
                    alpha = temp

                if beta > alpha:
                    print "Max cutoff " + stepPerBoard
                    return (best_move[0],steps + " | " + best_move[1],best_move[2])
          
 #               steps = stepPerBoard
            
            print "Max " + steps;
            return (best_move[0],steps + " | " + best_move[1],best_move[2])

    def minmove(self, depth, board, color, steps, count, hash, alpha, beta):
	   
        if (depth == 0):
            strength = self.eval.evaluateBoard(board, color, True) #returns the strength value of the board 
            return (strength,steps,board)
        
	else:    
           
            best_move = (-99999999,steps,board)

            turnList = []
            # Construct a new MoveGenerator object for white and its board,
            # then generate all the possible moves.
            moveGen = MoveGenerator.MoveGenerator(count, color, board, hash)

	    # make sure that there are no past moves being made, since 
	    # the function will confuse it with push or pull
            moveGen.genMoves("", self.start_row, self.start_col, self.end_row, self.end_col)
            # The list of possible moves is stored in moveGen.moveStepHashes
            # as a list of tuples of the form (the board, the steps taken
            # to get to that board, and hash key for that board).
            turnList = moveGen.moveStepHashes
	    
            for turn in turnList:
                newBoardState = turn[0]
                stepPerBoard = turn[1]

                if depth == 1:
		  newColor = color
		else:
                  if color == "w":
                     newColor = "b"
                  else:
                     newColor = "w"
            
                temp = self.maxmove(depth - 1, newBoardState, newColor, stepPerBoard, count, hash, alpha, beta)
                if temp[0] > best_move[0]:
                    best_move = temp
                    beta = temp

                if beta[0] < alpha[0]:
                    print "Min-cutoff " + stepPerBoard
                    return (best_move[0],steps + " | " + best_move[1],best_move[2])
                
#                steps = stepPerBoard

            print "Min: " + steps
            return (best_move[0], steps + " | " + best_move[1],best_move[2])
