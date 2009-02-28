# another comment
# eric2 test comment
class Board:
     GOLD = 0x0
     def __init__(self):
         self.board = {}
	 self.board[0][2] = "X"
         self.nextToMove = self.GOLD;
	 self.totalMoves = 0;

