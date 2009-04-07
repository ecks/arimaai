def displayBoard(board):
         print " ",
         for letter in range(97, 105):
             print chr(letter),
         print
 
         rowNum = 8
         for i in board:
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
         print
