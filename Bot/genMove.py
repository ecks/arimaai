from Position import * 

moveBoardList = []

# for board, return a list that contains a tuple of move and board for a particular board state 
def generateMove(board, turn):
    
    for moveNum in range(0,4): #loop for each move in the turn
        for row in range(0,8): #loop over full board
            for col in range(0,8):
                if board[row][col].isupper():

                  position = Position(board[row][col] ,row+1, col, 'n')
                  if checkMove(board, position):
		     newBoard = updateBoard(board, position)
                     moveBoardList.add((position, newBoard))
                   
                
def checkMove (board, position):
    row = position.row
    col = position.col
    if row < 8 or row >= 0 or col >= 0 or col < 8:
      if board[row][col] == ' ' or board[row][col] == 'x':
        return True
    return False

def updateBoard(board, position):
  newBoard = board[position.row][position.col] = position.piece
  return newBoard

# Translates the char to a number (strength).
def translatePiece(piece):
    
    transTable = string.maketrans("emhdcrEMHDCR", "654321654321")  # Make the translation table.
    piece = string.translate(piece, transTable)  # Translate the piece
    return piece


def isStronger(a, b):
    return True    
