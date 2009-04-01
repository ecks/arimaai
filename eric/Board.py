from DataTypes import *
import Hash
import Step
import copy
import sys

class Board:
     def __init__(self, board, hashboard):
	 self.board = copy.deepcopy(board)
#         self.board = board  # be careful !!! reference, not actual assignment
         self.hashboard = hashboard
         self.hashkey = 0

     # helper
     def printHashKey(self):
	 print "Current hashkey: " + str(self.hashkey)

     # called in the beginning, initializes the hashkey
     def calculateHashkey(self):
         hashkey = 0
	 for i in range(LIMIT_ON_BOARD):
           for j in range(LIMIT_ON_BOARD):
	     stringOfPos = self.board[i][j]
	     intValueOfPos = pieces[stringOfPos] # get the integer value of the pos in order to refer to it
	     hashkey ^= self.hashboard[i][j][intValueOfPos] # get the actual hash code that we will use
         self.hashkey = hashkey
	 self.printHashKey()

     ##
     # Update the board with a new move.
     # @param step - the step to change the board with
     # @return final_steps - the steps including trapped piece steps
     def updateBoard(self, steps):
        final_steps = ""
	print steps
        for step in steps.split():
            final_steps = final_steps + " " + step 
	    step = Step.Step(step)
        
            piece = self.board[step.start_row][step.start_col]
	    beforeMove = self.board[step.start_row][step.start_col]
            self.board[step.start_row][step.start_col] = " "
	    
	    # update old position
	    self.updateHashKey(step.start_row, step.start_col, beforeMove)

            trapped_piece = ""
            
            # Is the piece in a trap square?
            if step.end_row == 2 and step.end_col == 2:
                if not self.__isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "c6x"
            elif step.end_row == 2 and step.end_col == 5:
                if not self.__isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "f6x"
            elif step.end_row == 5 and step.end_col == 2:
                if not self.__isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "c3x"
            elif step.end_row == 5 and step.end_col == 5:
                if not self.__isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "f3x"
            else:
		beforeMove = self.board[step.end_row][step.end_col]

                self.board[step.end_row][step.end_col] = step.piece

		# update new position
                self.updateHashKey(step.end_row, step.end_col, beforeMove)
    
            
            if trapped_piece != "":
                final_steps = final_steps + " " + trapped_piece

        
        
        return final_steps
   
     def displayBoard(self):
         print " ",
         for letter in range(97, 105):
             print chr(letter),
         print

         rowNum = 8
         for i in self.board:
           print rowNum,
           for j in i:
             print j,
           print rowNum,
           print
           rowNum = rowNum - 1

         print " ",
         for letter in range(97, 105):
             print chr(letter),
         print
         print

     def updateHashKey(self, row, col, oldPiece):
	 intValOfOldPos = pieces[oldPiece]
	 intValOfNewPos = pieces[self.board[row][col]]
	 self.hashkey ^= self.hashboard[row][col][intValOfOldPos]
	 self.hashkey ^= self.hashboard[row][col][intValOfNewPos]
	 self.printHashKey()


