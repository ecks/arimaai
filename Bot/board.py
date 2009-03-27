
class Board:
  board = []
  numMoves = 0
  turn = 'w'

  def __init__(self, board, numMoves, turn):
    self.board = board
    self.numMoves = numMoves
    self.turn = turn
