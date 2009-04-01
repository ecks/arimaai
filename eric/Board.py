from DataTypes import *
import Hash
import Step
import copy
import sys
import re

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

     ##
     # Update the board with a new move.
     # @param step - the step to change the board with
     # @return final_steps - the steps including trapped piece steps
     def computeHash(self, steps):
	# save hashkey and board
	oldHashkey = self.hashkey
	oldboard = copy.deepcopy(self.board)

        final_steps = ""
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
                if not self.isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "c6x"
            elif step.end_row == 2 and step.end_col == 5:
                if not self.isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "f6x"
            elif step.end_row == 5 and step.end_col == 2:
                if not self.isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "c3x"
            elif step.end_row == 5 and step.end_col == 5:
                if not self.isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "f3x"
            else:
		beforeMove = self.board[step.end_row][step.end_col]

                self.board[step.end_row][step.end_col] = step.piece

		# update new position
                self.updateHashKey(step.end_row, step.end_col, beforeMove)
    
            
            if trapped_piece != "":
                final_steps = final_steps + " " + trapped_piece

        # save hashkey in order to return
	retHashkey = self.hashkey
	# restore hashkey and board
	self.hashkey = oldHashkey
	self.board = copy.deepcopy(oldboard)

        
        return retHashkey

 ## ------------ Eric's functions ------------------------------------------- ##
     ##      
     # Determines if two pieces are on the same team.
     # @param pieceA - the first piece
     # @param pieceB - the second piece
     # @return True if they are friends, False if they are enemies
     def areFriends(self, pieceA, pieceB):
        if pieceA.isupper() and pieceB.isupper or pieceA.islower() and pieceB.islower():
            return True
        else:
            return False
    
     ##
     # Simply returns whether or not a piece has a friendly
     # piece next to it in an adjacent square. Used to check
     # trap squares.
     # @param row - the row
     # @param col - the column
     # @return True if it's safe, False otherwise.
     def isSafe(self, row, col):
        adj_occ_pos = self.getAdjacentPositions(row, col, True)
        for pos in adj_occ_pos:
            adj_row = pos[0]
            adj_col = pos[1]
            adj_piece = self.board[adj_row][adj_col]
            piece = self.board[adj_row][adj_col]
            if self.areFriends(adj_piece, piece):
                return True
        
        return False
     
     # Returns all the adjacent positions (north, south, east, west),
     # that are on the board, to this piece.
     # @param row - the piece's row
     # @param col - the pieces's column
     # @param occupied - True to return only occupied space, False to return empty spaces.
     # @return pieces - the positions adjacent to this piece
     def getAdjacentPositions(self, row, col, occupied):
        
        positions = []
        
        if occupied:
            expr = "[^ x]"
        else:
            expr = "( |x)"
            
        
        # North
        if row - 1 >= 0 and re.match(expr, self.board[row-1][col], re.IGNORECASE):
            positions.append([row - 1, col])
        
        # South
        if row + 1 <= 7 and re.match(expr, self.board[row+1][col], re.IGNORECASE):
            positions.append([row + 1, col])
        
        # West
        if col - 1 >= 0 and re.match(expr, self.board[row][col-1], re.IGNORECASE):
            positions.append([row, col - 1])
        
        # East
        if col + 1 <= 7 and re.match(expr, self.board[row][col+1], re.IGNORECASE):
            positions.append([row, col + 1])
        
        return positions
 
    def displayBoard(self, b):
         print " ",
         for letter in range(97, 105):
             print chr(letter),
         print

         rowNum = 8
         for i in b:
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
## ------------------------ Eric's functions -----------------------------------

     def getHashKey(self):
	 return self.hashkey
   
     def updateHashKey(self, row, col, oldPiece):
	 intValOfOldPos = pieces[oldPiece]
	 intValOfNewPos = pieces[self.board[row][col]]
	 self.hashkey ^= self.hashboard[row][col][intValOfOldPos]
	 self.hashkey ^= self.hashboard[row][col][intValOfNewPos]


