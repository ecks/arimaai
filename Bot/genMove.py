# use stderr for output, stdout is taken!!!!!!!!!!!!!



import sys
from Position import * 
from board import *

moveBoardList = []

def printrowAnCol(row,col):
    print "row->"+str(row)
    print "col->"+str(col)

def printBoard(board):
    sys.stderr.write("board <<<<<<<<<<<<\n")
    for row in range(0,8):
      sys.stderr.write(str(board[row])+"\n")
    sys.stderr.write("board >>>>>>>>>>>>\n")
 
def otherTurn(turn):
    if turn is 'b':
	return 'w'
    else:
	return 'b'

# for board, return a list that contains a tuple of move and board for a particular board state 
def generateMove(board):
    aBoard = board.board
    printBoard(aBoard)
#    for moveNum in range(0,4): #loop for each move in the turn
    for row in range(0,8): #loop over full board
            for col in range(0,8):
              if aBoard[row][col].isupper() and aBoard[row][col] != 'X':
#		  if row != 7:
#		    oldPos = Position(board[row][col], row,col, '-')
#                    pos = Position(board[row][col] ,row+1, col, 's')
#                    if checkMove(board, pos):
#		      newBoard = updateBoard(board, oldPos, pos)
		   #   printBoard(newBoard)
#                      moveBoardList.append((pos, newBoard))
		  if row != 0:
		    oldPos = Position(aBoard[row][col], row,col, '-')
		    pos = Position(aBoard[row][col], row-1,col, 'n')
		    if checkMove(aBoard,pos):
   		      aNewBoard,newNumMoves = updateBoard(aBoard, oldPos, pos, board.numMoves)
		      newBoard = Board(aNewBoard,newNumMoves, otherTurn(board.turn))
		      printBoard(aNewBoard)
                      moveBoardList.append((pos, newBoard))
#    for l in moveBoardList:
#      printBoardAndTurn(l[1])
	            
                
def checkMove (board, pos):
    row = pos.row
    col = pos.col
    if row < 8 or row >= 0 or col >= 0 or col < 8:
      if board[row][col] == ' ' or board[row][col] == 'X':
        return True
    return False

def updateBoard(newBoard, oldPos, pos, numMoves):
  newBoard[pos.row][pos.col] = pos.piece
  newBoard[oldPos.row][oldPos.col] = ' '
  numMoves = numMoves - 1
  return (newBoard,numMoves)

# Translates the char to a number (strength).
def translatePiece(piece):
    
    transTable = string.maketrans("emhdcrEMHDCR", "654321654321")  # Make the translation table.
    piece = string.translate(piece, transTable)  # Translate the piece
    return piece


def isStronger(a, b):
    return True    
