import itertools

# another comment
# eric2 test comment


# Sample board.
# 7g 
#  +-----------------+
# 8|   r   r r   r   |
# 7| m   h     e   c |
# 6|   r x r r x r   |
# 5| h   d     c   d |
# 4| E   H         M |
# 3|   R x R R H R   |
# 2| D   C     C   D |
# 1|   R   R R   R   |
#  +-----------------+
#    a b c d e d g h




class Board:
 
     cToNum = dict(zip(map(chr,range(97,105)),range(0,8))) # easy way to go from char to int, so cToNum['a'] => 0 .. cToNum['h'] => 7

     color = {'g' : "Gold", 's' : "Silver"}
     pieces = {'E' : "Gold Elephant",
               'e' : "Silver Elephant",
               
               'M' : "Gold Camel",
               'm' : "Silver Camel",
               
               'H' : "Gold Horse",
               'h' : "Silver Horse",
            
               'D' : "Gold Dog",
               'd' : "Silver Dog",
               
               'C' : "Gold Cat",
               'c' : "Silver Cat",
     
               'R' : "Gold Rabbit",
               'r' : "Silver Rabbit"}  
            
     GOLD = 0x0
     def __init__(self):
         self.board = [[] for i in range(8)]
	 map(lambda xL : map(xL.append, itertools.repeat('.',8)), self.board)     # initialize empty board

	 ####### trap squares
	 self.board[2][2] = "X"
	 self.board[2][5] = "X"
	 self.board[5][2] = "X"
	 self.board[5][5] = "X"
         self.nextToMove = self.GOLD
	 self.totalMoves = 0
    

     def updateBoard(self, mv):
	 self.board[-1*int(mv[2])][self.cToNum[mv[1]]] = mv[0];  # mv[0] is the piece, mv[1] is its column, mv[2] is its row

     def printBoard(self):
	 for i in self.board:
	   for j in i:
             print j,
	   print
    
     def move(self, moveArg):
         mv = moveArg.split();
 	 mvNum = mv[0][0];
	 mvCol = mv[0][1];
	 mvList = mv[1:];
	 map(self.updateBoard, mvList);       # update board with element from list
	 self.printBoard();
	 print "Round: "+mvNum;
	 print "Turn: "+self.color[mvCol];
        
