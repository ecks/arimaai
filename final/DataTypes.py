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

pieces = {' ' : EMPTY,
	  'x' : EMPTY,
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
