import math

class evaluation(Object):
    self.hashkeys = []
    self.evaluations = []

    #Paul Abbazia
    #boardState/board = 8x8 array containing the value of the piece in each position (negative for opponent's piece)
    #alpha/beta = value
    #depth = int
    #turn = int, 1 = white, -1 = black
    def negascout(self, depth, alpha, beta, board, turn):
        if (depth == 0):
            val = self.evaluate(board, turn) #returns the strength value of the board

        bestPos = self.boardStrength()
        if turn == 1: #white's turn
            lowRow = bestPos[0][0]-4
            lowCol = bestPos[0][1]-4
            highRow = lowRow + 8
            highCol = highRow + 8
            if lowRow < 0:
                lowRow = 0
            if lowCol < 0:
                lowCol = 0
            if highRow > 7:
                highRow = 7
            if highCol > 7:
                highCol = 7
            turnList = self.genMoves(self,[],lowRow,lowCol,highRow,highCol) #moveList contains a set of turns (containing move sets)
        elif turn == -1: #black's turn
            lowRow = bestPos[0][0]-4
            lowCol = bestPos[0][1]-4
            highRow = lowRow + 8
            highCol = highRow + 8
            if lowRow < 0:
                lowRow = 0
            if lowCol < 0:
                lowCol = 0
            if highRow > 7:
                highRow = 7
            if highCol > 7:
                highCol = 7
            turnList = self.genMoves(self,[],lowRow,lowCol,highRow,highCol) #moveList contains a set of turns (containing move sets)

        for move in turnList:
            newBoardState = makeMovePseudoCode()################################
            index = Hash(newBoardState)
            
            val = -negascout(depth - 1, -beta, -alpha, newBoard, -turn) #descend one level and invert the function

            if (val >= beta):
                return beta
            if (val > alpha):
                alpha = val

        return alpha    

    #Paul Abbazia
    #Evaluates the given board based on set criteria
    #Board value is given by:
    #Player gains pieceValue*distance across board for all pieces except rabbits
    #Player gains pieceValue*distance^2 for rabbits
    #Player 'gains' sum of square of own pieces - sum of square enemy pieces
    #@board the board state to evaluate
    #@return the value of this board state
    def evaluate(self, board):
        value = 0
        if self.color == 'white':
            for col in range(0,8):
                for row in range(0,8):
                    piece = board[row,col]
                    if piece >= 'A':
                        value += self.__pieceValue(piece)**2
                        if piece != 'R':
                            value += self.__pieceValue(piece) * (row+1)
                        elif piece == 'R':
                            value += self.__pieceValue(piece) * (row+1)**2

                    if piece < 'A':
                        value -= self.__pieceValue(piece)**2
        elif self.color == 'black':
            for col in range(0,8):
                for row in range(0,8):
                    piece = board[row,col]
                    if piece < 'A':
                        value += self.__pieceValue(piece)**2
                        if piece != 'r':
                            value += self.__pieceValue(piece) * (row+1)
                        elif piece == 'r':
                            value += self.__pieceValue(piece) * (row+1)**2

                    if piece >= 'A':
                        value -= self.__pieceValue(piece)**2
        return value
            

    #Paul Abbazia
    #Computes a running average of piece values to narrow search space (a 4x4 grid is chosen to try to contain pieces that could potentially effect the area)
    #Returns the center of the strongest position for each player
    def boardStrength(self):
        white = copy.deepcopy(self.board)
        black = copy.deepcopy(self.board)
        bestWhite = 0
        bestBlack = 0
        for row in range(0,8):
            for col in range(0,8):
                indices = [] #the indices of the moves concerned
                for x in range(-4,4): #subscript a 4x4 moving grid
                    for y in range(-4,4):
                        indices.append([math.abs(row + x), math.abs(col+y)])#take the absolute value to avoid going out of bounds
                white[row,col] = average(indices,16,white,1)
                if white[row,col] > bestWhite:
                    bestWhite = white[row,col]
                    bestWhitePos = [row,col]
                black[row,col] = average(indices,16,white,-1)
                if black[row,col] > bestBlack:
                    bestBlack = black[row,col]
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
        for point in array2D:
            piece  = board[point[0],point[1]]
            if player == 1:
                if piece >= A: #white piece
                    total += self.__pieceValue(piece)
            elif player == -1:
                if piece < A: #black piece
                    total += self.__pieceValue(piece)
        return total/gridSize

    ##
    # Returns the strength value of a given piece.
    # @param piece - the piece
    # @param strength - the piece's strength
    def __pieceValue(self, piece):
        piece = piece.lower()   # Make the piece lowercase.
        
        # Make the translation table for strengths
        transTable = string.maketrans("emhdcrx", "6543210")  
        strength = string.translate(piece, transTable)  # Translate the piece
        return strength
