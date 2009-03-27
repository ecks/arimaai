import board
import genMove

aBoard = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', 'X', ' ', ' ', 'X', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', 'X', ' ', ' ', 'X', ' ', ' '], ['H', 'D', 'C', 'M', 'E', 'C', 'D', 'H'], ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R']]
numMoves = 1
turn = 'b'
myBoard = board.Board(aBoard,numMoves,turn)

genMove.generateMove(myBoard)
