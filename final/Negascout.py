'''
Filename: Negascout.py
Description: Responsible for finding an optimal move based on
its evaluation function.

@author: Hristo Asenov
'''

import Evaluation
import MoveGenerator
import string
import Common
import bisect

class Negascout(object):

    ##
    # Constructor Negascout
    def __init__(self):
        self.hashkeysEvalsSteps = []
        self.evaluations = []

	self.eval = Evaluation.Evaluation()

        # To-do: Determine best starting grid

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
	    
        if (depth == 0):
            strength = self.eval.evaluateBoard(board, color) #returns the strength value of the board 
            self.hashkeysEvalsSteps.append((hash.get_hashkey(), strength, steps)) 
            self.hashkeysEvalsSteps.sort() # warning !!! may not be the best way to do this !!!
            return (strength, steps)
        
        b = beta
        m = ""
	    
        turnList = []
        
            
        # Construct a new MoveGenerator object for white and its board,
        # then generate all the possible moves.
        moveGen = MoveGenerator.MoveGenerator(count, color, board, hash)
        # moveGen.genMoves("", lowRow, lowCol, highRow, highCol)
        moveGen.genMoves("")
        
        # The list of possible moves is stored in moveGen.moveStepHashes
        # as a list of tuples of the form (the board, the steps taken
        # to get to that board, and hash key for that board).
        turnList = moveGen.moveStepHashes
	    

        for turn in turnList:
            newBoardState = turn[0]
            stepPerBoard = turn[1]
            hashForBoard = turn[2]
            
	    # reset from initial board hash to new board hash
            hash.resetInitialHashKey(hashForBoard)
    
            newColor = color
	    if depth > 1:
	      # if depth is 1, we need to evaluate the actual board with the same color
              newColor = string.translate(color, Common.nextColor)

            
            currentHashKeys = map(lambda x: x[0], self.hashkeysEvalsSteps)
            
            ins_pt = bisect.bisect_left(currentHashKeys, hashForBoard)
        
            if len(currentHashKeys) == ins_pt or hashForBoard != currentHashKeys[ins_pt]:
	        # original entry, need to reevaluate
            
                # descend one level and invert the function
		bTemp = (-1 * b[0],b[1])
		alphaTemp = (-1 * alpha[0], alpha[1])
                a = self.negascout(depth - 1, bTemp, alphaTemp, newBoardState, newColor, stepPerBoard, count, hash)
            else:
                # already got the evaluation of it, just return the evaluated value
                a = (self.hashkeysEvalsSteps[ins_pt][1],self.hashkeysEvalsSteps[ins_pt][2])
            
	    a = (a[0] * -1,a[1])

	    print "a: " + str((a,m,b))
	    # alpha-beta pruning
	    if a[0] > alpha[0]:
	      print "Change alpha: " + str(alpha[0]) + " a => " + str(a[0])
	      alpha = a
          
	    print "alpha: " + str((alpha,m,b))

	    if alpha[0] >= beta[0]:
	      return (alpha[0], steps + " | " + alpha[1])
      
	    if alpha[0] >= b[0]:
	      betaTemp = (-1 * beta[0],beta[1])
	      alphaTemp = (-1 * alpha[0],alpha[1])
	      alpha = self.negascout(depth - 1, betaTemp, alphaTemp, newBoardState, newColor, stepPerBoard, count, hash)
	      alpha = (alpha[0] * -1,alpha[1])
	      print "in alpha >= b: alpha ==> " + str(alpha)
              if alpha[0] >= beta[0]:
                return (alpha[0],steps + " | " + alpha[1])
          
            b = (alpha[0] + 1,alpha[1])
            
        return (alpha[0],steps + " | " + alpha[1])
