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
         self.board = {}
	 self.board[0][2] = "X"
         self.nextToMove = self.GOLD
	 self.totalMoves = 0
    
         print "i";



board = Board()

