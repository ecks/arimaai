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
    def __init__(self, board, color):
        self.hashkeysEvalsSteps = []
        self.evaluations = []
        
        self.eval = Evaluation.Evaluation()

        (self.start_row, self.start_col, self.end_row, self.end_col) = self.eval.getStrongestGrid(board, color)
        print "start row: " + str(self.start_row)
        print "start col: " + str(self.start_col) 
        print "end row: " + str(self.end_row)
        print "end col: " + str(self.end_col)

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
            strength = self.eval.evaluateBoard(board, color, True) #returns the strength value of the board 
            self.insertEntrySorted((hash.get_hashkey(), strength, steps), self.hashkeysEvalsSteps) 
            stepsSaved = map(lambda x: x[2], self.hashkeysEvalsSteps)
            return (strength, steps)
        
        b = beta
	    
        turnList = []
        
            
        # Construct a new MoveGenerator object for white and its board,
        # then generate all the possible moves.
        moveGen = MoveGenerator.MoveGenerator(count, color, board, hash)

	# make sure that there are no past moves being made, since 
	# the function will confuse it with push or pull
        moveGen.genMoves("", self.start_row, self.start_col, self.end_row, self.end_col)
        #moveGen.genMoves("")
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
            
	    if not self.isEntryInList(hashForBoard, currentHashKeys):
	        # original entry, need to reevaluate
            
                # descend one level and invert the function
                bTemp = (-1 * b[0],b[1])
                alphaTemp = (-1 * alpha[0], alpha[1])
                a = self.negascout(depth - 1, bTemp, alphaTemp, newBoardState, newColor, stepPerBoard, count, hash)
            else:
                # already got the evaluation of it, just return the evaluated value
		ins_pt = self.getInsPt()
                a = (self.hashkeysEvalsSteps[ins_pt][1],self.hashkeysEvalsSteps[ins_pt][2])
            
            a = (a[0] * -1,a[1])

	    # alpha-beta pruning
            if a[0] > alpha[0]:
                alpha = a
          
            if alpha[0] >= beta[0]:
                return (alpha[0], steps + " | " + alpha[1])
      
            if alpha[0] >= b[0]:
                betaTemp = (-1 * beta[0],beta[1])
                alphaTemp = (-1 * alpha[0],alpha[1])
                alpha = self.negascout(depth - 1, betaTemp, alphaTemp, newBoardState, newColor, stepPerBoard, count, hash)
                alpha = (alpha[0] * -1,alpha[1])

                if alpha[0] >= beta[0]:
                    return (alpha[0],steps + " | " + alpha[1])
      
                b = (alpha[0] + 1,alpha[1])
            
        return (alpha[0],steps + " | " + alpha[1])

    def insertEntrySorted(self, entry, list):
	    ins_pt = bisect.bisect_left(list, entry)
	    if len(list) == ins_pt or entry != list[ins_pt]:
                list.insert(ins_pt, entry)
	    else:
                raise Exception, "You are trying to append to list after evaluation, and the entry was found which is impossible!!!"
      
    def isEntryInList(self, entry, list):
	    ins_pt = bisect.bisect_left(list, entry)
	    if len(list) == ins_pt or entry != list[ins_pt]:
		self.found_ins_pt = -1
                return False
	    else:
                self.found_ins_pt = ins_pt
                return True

    def getInsPt(self):
            if self.found_ins_pt == -1:
                raise Exception, "Trying to access insertion point when it wasn't defined"
	    else:
                return self.found_ins_pt
 
