class Board:
     GOLD = 0x0
     def __init__(self):
         self.board = {}
         self.nextToMove = self.GOLD;
	 self.totalMoves = 0;

