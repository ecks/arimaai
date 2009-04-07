'''
Filename: Hash.py
Description: Hash class that is responsible for creating and modifying hashkey

@author: Hristo Asenov
'''

from DataTypes import *
import itertools
import random

class Hash:
  # initialize a two-dimensional board
  hash_board = [[' ' for col in range(LIMIT_ON_BOARD)] for row in range(LIMIT_ON_BOARD)]  

  ##
  # Hash constructor
  # Initializes three-dimensional list, the two dimensions 
  # being row and column, the third dimension being all 
  # the possible pieces that could be placed inside that position. 
  # Every item in the list has a very random hashkey
  def __init__(self):
	self.hashkey = 0
	self.tempHashkey = self.hashkey
	hash_board = self.hash_board
	# don't feel like calling with self everytime
	get_random_hashkey = self.get_random_hashkey
	for i in range(LIMIT_ON_BOARD):
	  for j in range(LIMIT_ON_BOARD):
	    # The following statement gives us an extra dimension, 
            # filled with 0s the length of MAX_COMBOS, 
            # needed to make every possible combination of pieces
	    hash_board[i][j] = map(lambda x : x, itertools.repeat(0,MAX_COMBOS))

	for i in range(LIMIT_ON_BOARD):
	  for j in range(LIMIT_ON_BOARD):
	    # set a unique value for each possible move
            hash_board[i][j][EMPTY] = get_random_hashkey();
            hash_board[i][j][GOLD+RABBIT] = get_random_hashkey();
            hash_board[i][j][GOLD+CAT] = get_random_hashkey();
            hash_board[i][j][GOLD+DOG] = get_random_hashkey();
            hash_board[i][j][GOLD+HORSE] = get_random_hashkey();
            hash_board[i][j][GOLD+CAMEL] = get_random_hashkey();
            hash_board[i][j][GOLD+ELEPHANT] = get_random_hashkey();
            hash_board[i][j][SILVER+RABBIT] = get_random_hashkey();
            hash_board[i][j][SILVER+CAT] = get_random_hashkey();
            hash_board[i][j][SILVER+DOG] = get_random_hashkey();
            hash_board[i][j][SILVER+HORSE] = get_random_hashkey();
            hash_board[i][j][SILVER+CAMEL] = get_random_hashkey();
            hash_board[i][j][SILVER+ELEPHANT] = get_random_hashkey();
	self.hash_board = hash_board

  ##
  # Generates the random number
  # @return value - 64-digit pseudo-random number
  def get_random_hashkey(self):
	value = 0
	randVal = 0
        
	# create 64-digit pseudo (hopefully not!) random number
	for i in range(0,64):
		randVal = random.getrandbits(1)
		value = (value<<1)+randVal

	return value

  ##
  # @return self.hash_board - accessor to the hash_board
  def get_hash_board(self):
	return self.hash_board


  ## 
  # Gives a final seeder value of the initial board. 
  # Should be called right after initializing the Hash object. 
  # @param board - two-dimensional list of the moves
  # @return hashkey - unique key that represents the initial board state
  def calculateHashkey(self, board):
         hashkey = 0
	 for i in range(LIMIT_ON_BOARD):
           for j in range(LIMIT_ON_BOARD):
	     stringOfPos = board[i][j]
             
             # Get the integer value of the pos in order to refer to it.
	     intValueOfPos = pieces[stringOfPos]

             # Get the actual hash code that we will use.
             # ^= is the equivalent to an xor.
	     hashkey ^= self.hash_board[i][j][intValueOfPos] 

         self.hashkey = hashkey


  ##
  # Resets the working hashkey to the original hashkey. 
  # This is necessary when we are generating a hashkey 
  # from the initial board, since we need to go 
  # back to the original hash
  def initTempHashKey(self):
	 self.tempHashkey = self.hashkey

  ##
  # Called when making an actual move. 
  # The old and new pieces are xored with the current 
  # hashkey in order to record the new position
  # @param row - the x coordinate
  # @param col - the y coordinate
  # @param oldPiece - the old piece to xor the current board state with
  # @param newPiece - the new piece to xor the current board state with
  def updateHashKey(self, row, col, oldPiece, newPiece):
	 intValOfOldPos = pieces[oldPiece]
	 intValOfNewPos = pieces[newPiece]
	 self.tempHashkey ^= self.hash_board[row][col][intValOfOldPos]
	 self.tempHashkey ^= self.hash_board[row][col][intValOfNewPos]

  ##
  # Should be called at the end, when the move is done. 
  # This returns the working hashkey and resets it to the original hashkey
  # @return retHashkey - the working hashkey generated so far
  def getFinalHash(self):
	  retHashkey = self.tempHashkey
	  self.initTempHashKey()
	  return retHashkey
