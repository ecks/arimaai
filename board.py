# another comment
# eric2 test comment
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

