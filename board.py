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

    
     pieces = {'.' : 0,
               'E' : 6,
               'e' : 6,
               
               'M' : 5,
               'm' : 5,
               
               'H' : 4,
               'h' : 4,
            
               'D' : 3,
               'd' : 3,
               
               'C' : 2,
               'c' : 2,
     
               'R' : 1,
               'r' : 1
              }    

     limitOnBoard = 8

     color = {'g' : "Gold", 's' : "Silver"}
     GOLD = 0x0
     def __init__(self):
         self.board = [[] for i in range(self.limitOnBoard)]
	 map(lambda xL : map(xL.append, itertools.repeat('.',self.limitOnBoard)), self.board)     # initialize empty board

	 ####### trap squares
	 self.board[2][2] = "X"
	 self.board[2][5] = "X"
	 self.board[5][2] = "X"
	 self.board[5][5] = "X"
         self.nextToMove = self.GOLD
	 self.totalMoves = 0
    

     def initBoard(self, mv):
	 self.board[int(mv[2])][self.cToNum[mv[1]]] = mv[0];  # mv[0] is the piece, mv[1] is its column, mv[2] is its row

     def updateBoard(self, mv):
         piece = mv[0];
         column = self.cToNum[mv[1]]
         row = int(mv[2])
         
         if mv[3] is "s":
           if self.isValidMove((row+1,column), piece) == False:
	     print "Cannot move south!"
           else:
             self.board[row+1][column] = piece 
	     self.board[row][column] = "."
         elif mv[3] is "e":
           if self.isValidMove((row,column+1), piece) == False:
	     print "Cannot move east!"
           else:
             self.board[row][column+1] = piece
	     self.board[row][column] = "."
         elif mv[3] is "w":
           if self.isValidMove((row,column-1), piece) == False:
	     print "Cannot move west!"
           else:
             self.board[row][column-1] = piece
	     self.board[row][column] = "."
         elif mv[3] is "n":
           if self.isValidMove((row-1,column), piece) == False:
	     print "Cannot move north!"
           else:
             self.board[row-1][column] = piece
	     self.board[row][column] = "."
        
     def isValidMove(self, (r,c), piece):
          if (r < self.limitOnBoard) and (r >= 0) and (c < self.limitOnBoard) and (c >= 0):
           if self.board[r][c] == ".":
	     return True
           else:
	     return False
          else:
           return False
 
     def printBoard(self):
	 for i in self.board:
	   for j in i:
             print j,
	   print
    
     def move(self, moveArg):
         mv = moveArg.split();
 	 mvNum = mv[0][0];
	 mvColor = mv[0][1];
	 mvList = mv[1:];

         mvList = map(lambda xL: xL[0:2] + str(int(xL[2])*(-1)+8) + xL[3:], mvList)  # convert from 8 -> 0, 7 -> 1 .. 1 -> 7, and assign back into mvList

         # Initial setup.
         if len(mvList[0]) == 3:
	   map(self.initBoard, mvList);       # update board with element from list
         
         # Regular move.
         elif len(mvList[0]) == 4:
           if len(mvList) <= 3:
	     map(self.updateBoard, mvList);
         # elif mvList[0] == "takeback":
             # to be implemented later
         elif mvList == "resigns":
           print "you lose"
         else:
           print "you passed an invalid string format"
	 self.printBoard();
	 print "Round: "+mvNum;
	 print "Turn: "+self.color[mvColor]; 
