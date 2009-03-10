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




class Board:
 
     cToNum = dict(zip(map(chr,range(97,105)),range(0,8))) # easy way to go from char to int, so cToNum['a'] => 0 .. cToNum['h'] => 7

     turn = "gold" #which player's turn is it?
     
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
         pos = (row, column)

         #Pieces can't move out of the board, and rabbits can't move backwards, and opponents pieces can only be moved by a push or pull
         if mv[3] is "s":
           if self.isValidMove((row+1,column), pos, piece) == False or (piece == "R" and turn == "gold"):
             print "Cannot move south!"
           else:
             self.board[row+1][column] = piece 
             self.board[row][column] = "."
         elif mv[3] is "e":
           if self.isValidMove((row,column+1), pos, piece) == False:
             print "Cannot move east!"
           else:
             self.board[row][column+1] = piece
             self.board[row][column] = "."
         elif mv[3] is "w":
           if self.isValidMove((row,column-1), pos, piece) == False:
             print "Cannot move west!"
           else:
             self.board[row][column-1] = piece
             self.board[row][column] = "."
         elif mv[3] is "n":
           if self.isValidMove((row-1,column), pos, piece) == False or (piece == "r" and turn == "silver"):
             print "Cannot move north!"
           else:
             self.board[row-1][column] = piece
             self.board[row][column] = "."
        
     def isValidMove(self, (r,c), (origr, origc), piece):
          valid = False #Boolean of whether this is a valid move. Start as false to prevent unplanned moves
          if (r < self.limitOnBoard) and (r >= 0) and (c < self.limitOnBoard) and (c >= 0): #is move within board?
           if self.board[r][c] == ".": #moving to a blank space?
             valid = True
          if self.board[origr][origc] != piece: #check if moving a real piece
               print("Piece does not exist in that position")
               valid = False
          #Ensure a player can only move opponent's pieces on the case of a push/pull
          #Does not ensure that the next move ensures the 2nd part of a push/pull, that the next move
          #has this player's adjacent piece fill the position, code probably needs a rewrite to account for this
          if turn == "gold" and piece >= "A":
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
         if turn == "gold":
              turn == "silver"
         else:
              turn == "gold"

