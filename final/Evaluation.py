import Common
import MoveGenerator
import math
import copy
import string

class Evaluation(object):

    hashkeys = []
    evaluations = []

    def __init__(self):
	pass

    #Paul Abbazia
    #boardState/board = 8x8 array containing the value of the piece in each position (negative for opponent's piece)
    #alpha/beta = value
    #depth = int
    #turn = char, 'w' = white, 'b' = black
    def negascout(self, depth, alpha, beta, board, color, steps, count, hash):
        if (depth == 0):
            return( (self.evaluate(board, color),steps))#returns the strength value of the board
        a = alpha
        b = beta
        m=""
	turnList = []
        bestPos = self.boardStrength(board)
	if color == 'w': #white's turn
            lowRow = bestPos[0][0]-2
            lowCol = bestPos[0][1]-2
            highRow = lowRow + 4
            highCol = lowCol + 4
            if lowRow < 0:
                lowRow = 0
            if lowCol < 0:
                lowCol = 0
            if highRow > 7:
                highRow = 7
            if highCol > 7:
                highCol = 7
	    moveGen = MoveGenerator.MoveGenerator(count, color, board, hash)
            moveGen.genMoves(steps,lowRow,lowCol,highRow,highCol) #moveList contains a set of turns (containing move sets)
	 #   moveGen.genMoves(steps)
	    turnList = moveGen.moveSteps
        elif color == 'b': #black's turn
            lowRow = bestPos[0][0]-2
            lowCol = bestPos[0][1]-2
            highRow = lowRow + 4
            highCol = highRow +4
            if lowRow < 0:
                lowRow = 0
            if lowCol < 0:
                lowCol = 0
            if highRow > 7:
                highRow = 7
            if highCol > 7:
                highCol = 7
            moveGen = MoveGenerator.MoveGenerator(count, color, board, hash)
            moveGen.genMoves(steps,lowRow,lowCol,highRow,highCol) #moveList contains a set of turns (containing move sets)
	    turnList = moveGen.moveSteps
        for turn in turnList:
            newBoardState = turn[0]
            stepPerBoard = turn[1]
           # index = Hash(newBoardState)
            nextColor = string.maketrans("wb", "bw")
            (val,m) = self.negascout(depth - 1, -beta, -alpha, newBoardState, string.translate(color, nextColor), stepPerBoard, count, hash) #descend one level and invert the function
            val = val * -1
	    if a > val and beta < val and turn != turnList[0]:
		    (alpha,n) = NegaScout(depth - 1, -beta, -val, newBoardState, string.translate(color, nextColor), stepPerBoard, count, hash)
		    alpha = alpha * -1
	    Common.displayBoard(newBoardState)
	    print(val)
	    if (alpha >= beta):
	    	return alpha;
	    beta = alpha + 1
            if (val >= beta):
                return (beta,m)
            if (val > alpha):
                alpha = val
        return (alpha,m)    

    #Paul Abbazia
    #Evaluates the given board based on set criteria
    #Board value is given by:
    #Player gains pieceValue*distance across board for all pieces except rabbits
    #Player gains pieceValue*distance^2 for rabbits
    #Player 'gains' sum of square of own pieces - sum of square enemy pieces
    #@board the board state to evaluate
    #@return the value of this board state
    def evaluate(self, board, color):
        value = 0
        if color == 'w':
            for col in range(0,8):
                for row in range(0,8):
                    piece = board[row][col]
                    if piece.isupper():
                        value += self.__pieceValue(piece)**2
                        if piece != 'R':
                            value += self.__pieceValue(piece) * (row+1)
                        elif piece == 'R':
                            value += self.__pieceValue(piece) * (row+1)**2

                    if piece.islower():
                        value -= self.__pieceValue(piece)**2
        elif color == 'b':
            for col in range(0,8):
                for row in range(0,8):
                    piece = board[row][col]
                    if piece.islower():
                        value += self.__pieceValue(piece)**2
                        if piece != 'r':
                            value += self.__pieceValue(piece) * (row+1)
                        elif piece == 'r':
                            value += self.__pieceValue(piece) * (row+1)**2

                    if piece.isupper():
                        value -= self.__pieceValue(piece)**2
        return value
            

    #Paul Abbazia
    #Computes a running average of piece values to narrow search space (a 4x4 grid is chosen to try to contain pieces that could potentially effect the area)
    #Returns the center of the strongest position for each player
    def boardStrength(self, board):
        white = copy.deepcopy(board)
        black = copy.deepcopy(board)
        bestWhite = 0
        bestBlack = 0
        bestWhitePos = [0,0]
	bestBlackPos = [0,0]
        for row in range(0,len(board[0])):
            for col in range(0,len(board[0])):
                indices = [] #the indices of the moves concerned
                for x in range(-2,3): #subscript a 5x5 moving grid
                    for y in range(-2,3):
                        newRow = abs(row+x)
			newCol = abs(col+y)
			if newRow > 7:
				newRow = newRow - 2
			if newCol > 7:
				newCol = newCol - 2
			indices.append([newRow, newCol])#take the absolute value to avoid going negative out of bounds
                white[row][col] = self.average(indices,25,board,1)
                if white[row][col] > bestWhite:
                    bestWhite = white[row][col]
                    bestWhitePos = [row,col]
                black[row][col] = self.average(indices,25,board,-1)
                if black[row][col] > bestBlack:
                    bestBlack = black[row][col]
                    bestBlackPos = [row,col]
        #return [white,black]
        return [bestWhitePos, bestBlackPos]

    #Paul Abbazia
    #Computes the average value of the given grid on the board
    #@indices the points to average
    #@gridSize the size of the grid being averaged
    #@board the board concerned
    #@player 1 for white, -1 for black
    #@return the averaged position state
    def average(self, indices,gridSize, board, player):
        total = 0
        for point in indices:
            piece  = board[point[0]][point[1]]
            if player == 1:
                if piece.isupper(): #white piece
                    total = total + self.__pieceValue(piece)
            elif player == -1:
                if piece.islower(): #black piece
                    total = total + self.__pieceValue(piece)
        return total/(gridSize*1.)

    ##
    # Returns the strength value of a given piece.
    # @param piece - the piece
    # @param strength - the piece's strength
    def __pieceValue(self, piece):
        piece = piece.lower()   # Make the piece lowercase.
        
        # Make the translation table for strengths
        transTable = string.maketrans("emhdcrx ", "65432100")  
        strength = string.translate(piece, transTable)  # Translate the piece
        return float(strength)
