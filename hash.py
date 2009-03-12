from board import *
import random

class Hash:
  hash_board = init_a_board(LIMIT_ON_BOARD, [])
  def get_random_hashkey(self):
	value = 0
	randVal = 0

	for i in range(0,64):
		randVal = random.getrandbits(1)
		value = (value<<1)+randVal

	return value

  def __init__(self):
	hash_board = self.hash_board
	get_random_hashkey = self.get_random_hashkey
	for i in range(LIMIT_ON_BOARD):
	  for j in range(LIMIT_ON_BOARD):
	    hash_board[i][j] = map(lambda x : x, itertools.repeat(0,MAX_COMBOS))

	for i in range(LIMIT_ON_BOARD):
	  for j in range(LIMIT_ON_BOARD):
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


  def 
