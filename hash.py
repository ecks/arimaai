from board import *
import random

class Hash:
  # initialize a two-dimensional board
  hash_board = init_a_board(LIMIT_ON_BOARD, [])  
  def get_random_hashkey(self):
	value = 0
	randVal = 0
        
	# create 64-digit pseudo (hopefully not!) random number
	for i in range(0,64):
		randVal = random.getrandbits(1)
		value = (value<<1)+randVal

	return value

  def __init__(self):
	hash_board = self.hash_board
	# don't feel like calling with self everytime
	get_random_hashkey = self.get_random_hashkey
	for i in range(LIMIT_ON_BOARD):
	  for j in range(LIMIT_ON_BOARD):
	    # the following statement gives us an extra dimension, filled with 0s the length of MAX_COMBOS, needed to make every possible combination of pieces
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

  def get_hash_board(self):
	return self.hash_board


