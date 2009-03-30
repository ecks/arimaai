from DataTypes import *
import Hash
import copy
import sys

class Board:
     def __init__(self, board, hashboard):
	 self.board = copy.deepcopy(board)
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


