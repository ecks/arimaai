import itertools

# another comment
# eric2 test comment

"""Paul Abbazia
3/10/09
added code to prevent rabbits from moving backwards
added code to allow for pushing and pulling, however our current model does
not allow for a robust implementation of all of arimaa's rules
I suggest a switch to a functional, state-based approach for the game. The AI can use whatever approach we deem necessary
TODO: Implement code to allow the passing of up to 3 of a person's 4 moves
Implement losing conditions
Implement code to only allow adding pieces in the first two rows during the setup phase
and pieces that have yet to be added (I suggest splitting up the setup portion to a different function)
Implement code to explicitly make player use or pass their 4 moves
"""

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

def init_a_board(limit, insideElement):
         board = [[] for i in range(limit)]
         map(lambda xL : map(xL.append, itertools.repeat(insideElement,limit)), board)     # initialize empty board
	 return board

# each piece corresponds to a unique value
GOLD = 0 
SILVER = 6
ELEPHANT = 6
CAMEL = 5
HORSE = 4
DOG = 3
CAT = 2
RABBIT = 1
EMPTY = 0
MAX_COMBOS = (SILVER + ELEPHANT) + 1
LIMIT_ON_BOARD = 8

class Board:
 
     cToNum = dict(zip(map(chr,range(97,105)),range(0,8))) # easy way to go from char to int, so cToNum['a'] => 0 .. cToNum['h'] => 7

     turn = "gold" #which player's turn is it?
    
     # convert from the string specification needed by PGNs to the ints required for hashing
     pieces = {'.' : EMPTY,
	       'X' : EMPTY,
               'E' : GOLD+ELEPHANT,
               'e' : SILVER+ELEPHANT,
               
               'M' : GOLD+CAMEL,
               'm' : SILVER+CAMEL,
               
               'H' : GOLD+HORSE,
               'h' : SILVER+HORSE,
            
               'D' : GOLD+DOG,
               'd' : SILVER+DOG,
               
               'C' : GOLD+CAT,
               'c' : SILVER+CAT,
     
               'R' : GOLD+RABBIT,
               'r' : SILVER+RABBIT
              } 


     color = {'g' : "Gold", 's' : "Silver"}

     # class constructor
     def __init__(self, hash_board):
	 # initialize our board with "."
         self.board = init_a_board(LIMIT_ON_BOARD, '.')
	 self.hash_board = hash_board
         self.hashkey = 0
         ####### trap squares
         self.board[2][2] = "X"
         self.board[2][5] = "X"
         self.board[5][2] = "X"
         self.board[5][5] = "X"
         self.nextToMove = GOLD
         self.totalMoves = 0
	 # calculate the initial hashkey - notice that this is most computationally intensive task,
	 # since we must recurse through the entire two-dimensional array. this is the only time we 
	 # will have to do this
	 self.calculateHashkey()
    
     # method called in the beginning when we are initially placing pieces only
     def initBoard(self, mv):
	 row = int(mv[2])
	 column = self.cToNum[mv[1]]
	 piece = mv[0]
	 oldPiece = self.board[row][column] # we need a reference to the old piece since we will XOR it from the current key in order to get rid of it
         self.board[row][column] = piece;  
         self.updateHashkey((row,column,oldPiece))

     # method called subsequently when a player actually needs to move a piece
     def updateBoard(self, mv):
         piece = mv[0];
         column = self.cToNum[mv[1]]
         row = int(mv[2])
         pos = (row, column)

         #Pieces can't move out of the board, and rabbits can't move backwards, and opponents pieces can only be moved by a push or pull

	 # We must recalculate the hash key two times, once for the new moved position, and once for the old position we moved from
         if mv[3] is "s":
           if self.isValidMove((row+1,column), pos, piece) == False or (piece == "R" and self.turn == "gold"):
             print "Cannot move south!"
           else:
	     oldPiece = self.board[row+1][column]
             self.board[row+1][column] = piece 
	     self.updateHashkey((row+1,column,oldPiece))
	     oldPiece = self.board[row][column]
             self.board[row][column] = "."
	     self.updateHashkey((row,column,oldPiece))
         elif mv[3] is "e":
           if self.isValidMove((row,column+1), pos, piece) == False:
             print "Cannot move east!"
           else:
	     oldPiece = self.board[row][column+1]
             self.board[row][column+1] = piece
	     self.updateHashkey((row,column+1,oldPiece))
             oldPiece = self.board[row][column]
             self.board[row][column] = "."
	     self.updateHashkey((row,column,oldPiece))
         elif mv[3] is "w":
           if self.isValidMove((row,column-1), pos, piece) == False:
             print "Cannot move west!"
           else:
	     oldPiece = self.board[row][column-1]
             self.board[row][column-1] = piece
	     self.updateHashkey((row,column-1,oldPiece))
	     oldPiece = self.board[row][column]
             self.board[row][column] = "."
	     self.updateHashkey((row,column,oldPiece))
         elif mv[3] is "n":
           if self.isValidMove((row-1,column), pos, piece) == False or (piece == "r" and self.turn == "silver"):
             print "Cannot move north!"
           else:
	     oldPiece = self.board[row-1][column]
             self.board[row-1][column] = piece
	     self.updateHashkey((row-1,column,oldPiece))
	     oldPiece = self.board[row][column]
             self.board[row][column] = "."
	     self.updateHashkey((row,column,oldPiece))
        
     def isValidMove(self, (r,c), (origr, origc), piece):
          valid = False #Boolean of whether this is a valid move. Start as false to prevent unplanned moves
          if (r < LIMIT_ON_BOARD) and (r >= 0) and (c < LIMIT_ON_BOARD) and (c >= 0): #is move within board?
           if self.board[r][c] == ".": #moving to a blank space?
             valid = True
           if self.board[origr][origc] != piece: #check if moving a real piece
               print("Piece does not exist in that position")
               valid = False
          #Ensure a player can only move opponent's pieces on the case of a push/pull
          #Does not ensure that the next move ensures the 2nd part of a push/pull, that the next move
          #has this player's adjacent piece fill the position, code probably needs a rewrite to account for this
          if self.turn == "gold" and piece >= "A":
               if self.board[origr+1][origc] == ("." or (origr+1 > 8 or origr+1 < 0)):
                 if self.board[origr-1][origc] == ("." or (origr-1 > 8 or origr-1 < 0)):
                      if self.board[origr][origc+1] == ("." or (origc+1 > 8 or orig+1 < 0)):
                           if self.board[origr][origc-1] == ("." or (origc-1 > 8 or orig-1 < 0)):
                                valid = False
          return valid
 
     def printBoard(self):
         print " ",
         for letter in range(97, 105):
             print chr(letter),
         print
        
         rowNum = 8
         for i in self.board:
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

     # helper
     def printHashKey(self):
	 print "Current hashkey: " + str(self.hashkey)


     # updates a hashkey, first XORing the old position, then XORing the new position
     # notice that the third parameter passed is the old piece, since we can get the new piece directly
     def updateHashkey(self, (i,j,oldPiece)):
         intValueOfOldPos = self.pieces[oldPiece]
	 intValueOfNewPos = self.pieces[self.board[i][j]]
	 self.hashkey ^= self.hash_board[i][j][intValueOfOldPos]
	 self.hashkey ^= self.hash_board[i][j][intValueOfNewPos]
	 self.printHashKey()

     # called in the beginning, initializes the hashkey
     def calculateHashkey(self):
         hashkey = 0
	 for i in range(LIMIT_ON_BOARD):
           for j in range(LIMIT_ON_BOARD):
	     stringOfPos = self.board[i][j]
	     intValueOfPos = self.pieces[stringOfPos] # get the integer value of the pos in order to refer to it
	     hashkey ^= self.hash_board[i][j][intValueOfPos] # get the actual hash code that we will use
         self.hashkey = hashkey
	 self.printHashKey()

     def getHashkey(self):
         return self.hashkey
     
     def getBoard(self):
	 return self.board

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
         if self.turn == "gold":
              self.turn == "silver"
         else:
              self.turn == "gold"

