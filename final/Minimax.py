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
    # @param board - board from which we want to generate all moves
    # @param color - color of the initial board
    def __init__(self, board, color):
        self.hashkeysEvalsSteps = []
        self.evaluations = []
        
        self.eval = Evaluation.Evaluation()

        #print "start row: " + str(self.start_row)
        #print "start col: " + str(self.start_col) 
        #print "end row: " + str(self.end_row)
       # print "end col: " + str(self.end_col)

#        self.start_row = 0
#        self.start_col = 0
#        self.end_row = 7
#        self.end_col = 7
    


    ##
    # Minimax with alpha-beta pruning
    # Source: http://ai-depot.com/articles/minimax-explained/
    def minimax(self, depth, board, color, steps, count, hash):
        return self.maxmove(depth, board, color, steps, count, hash, (-99999999,steps,board,hash.get_hashkey()) , (99999999,steps,board,hash.get_hashkey()))

    def maxmove(self, depth, board, color, steps, count, hash, alpha, beta):
        if (depth == 0):
            strength = self.eval.evaluateBoard(board, color, True)
	    self.insertEntrySorted((hash.get_hashkey(),strength,steps,board), self.hashkeysEvalsSteps)
	    return (strength,steps,board,hash.get_hashkey())

        else:
            (start_row, start_col, end_row, end_col) = self.eval.getStrongestGrid(board, color)
            moveGen = MoveGenerator.MoveGenerator(count, color, board, hash)
            moveGen.genMoves("",start_row,start_col,end_row,end_col)
            turnList = moveGen.moveStepHashes

            for turn in turnList:
                newBoardState = turn[0]
                stepPerBoard = turn[1]   
		hashForBoard = turn[2]
      
                hash.resetInitialHashKey(hashForBoard)

                if depth == 1:
		  newColor = color
		else:
                  if color == "w":
                     newColor = "b"
                  else:
                     newColor = "w"

		#print stepPerBoard

#		print "Inside Maxmove " + stepPerBoard + " " + str(hashForBoard)
                currentHashKeys = map(lambda x: x[0], self.hashkeysEvalsSteps)
               
                # need to change this in future because as of right now, will short circuit,
		# i just know that this is useless with depth of 2 and searching through list 
		# will take more unnecessary processing time
		if depth == 1 and self.isEntryInList(hashForBoard, currentHashKeys):
		  ins_pt = self.getInsPt()
		  temp = (self.hashkeysEvalsSteps[ins_pt][1],stepPerBoard,self.hashkeysEvalsSteps[ins_pt][2],self.hashkeysEvalsSteps[ins_pt][0])
		else:
                  temp = self.minmove(depth - 1, newBoardState, newColor, stepPerBoard, count, hash, alpha, beta)

#		print "Returned to Maxmove: " + str(temp[0]) + " for " + temp[1]
      
                if temp[0] > alpha[0]:
                    alpha = temp

                if alpha[0] > beta[0]:
                    return (beta[0],steps + " | " + beta[1],beta[2],beta[3])
          
 #               steps = stepPerBoard
            
            return (alpha[0],steps + " | " + alpha[1],alpha[2],alpha[3])

    def minmove(self, depth, board, color, steps, count, hash, alpha, beta):
	   
        if (depth == 0):
            strength = self.eval.evaluateBoard(board, color, True) #returns the strength value of the board 
	    self.insertEntrySorted((hash.get_hashkey(),strength,steps,board),self.hashkeysEvalsSteps)
            return (strength,steps,board,hash.get_hashkey())
        
	else:    
           

            turnList = []
            (start_row, start_col, end_row, end_col) = self.eval.getStrongestGrid(board, color)
            # Construct a new MoveGenerator object for white and its board,
            # then generate all the possible moves.
            moveGen = MoveGenerator.MoveGenerator(count, color, board, hash)

	    # make sure that there are no past moves being made, since 
	    # the function will confuse it with push or pull
       #     moveGen.genMoves("", self.start_row, self.start_col, self.end_row, self.end_col)
            moveGen.genMoves("",start_row,start_col,end_row,end_col)
            # The list of possible moves is stored in moveGen.moveStepHashes
            # as a list of tuples of the form (the board, the steps taken
            # to get to that board, and hash key for that board).
            turnList = moveGen.moveStepHashes

#	    print len(turnList)

            for turn in turnList:
                newBoardState = turn[0]
                stepPerBoard = turn[1]
		hashForBoard = turn[2]

		hash.resetInitialHashKey(hashForBoard)

                if depth == 1:
		  newColor = color
		else:
                  if color == "w":
                     newColor = "b"
                  else:
                     newColor = "w"
            
#                print "Inside Minmove " + stepPerBoard + " " + str(hashForBoard)
                currentHashKeys = map(lambda x: x[0], self.hashkeysEvalsSteps)

                if self.isEntryInList(hashForBoard,currentHashKeys) and depth == 1:
		  ins_pt = self.getInsPt()
		  temp = (self.hashkeysEvalsSteps[ins_pt][1],stepPerBoard,self.hashkeysEvalsSteps[ins_pt][2],self.hashkeysEvalsSteps[0])
		else:
		  temp = self.maxmove(depth - 1, newBoardState, newColor, stepPerBoard, count, hash, alpha, beta)
#                print "result: " + str(temp[0])

		if temp[0] < beta[0]:
                    beta = temp

                if beta[0] < alpha[0]:
                    return (alpha[0],steps + " | " + alpha[1],alpha[2],alpha[3])
                

            return (beta[0], steps + " | " + beta[1],beta[2],beta[3])

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
 
