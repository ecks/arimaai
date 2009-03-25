#Paul Abbazia
#3/12/09
#Negascout, evaluation function, and move generation
#Needs to be changed to make use of hash table of board states
#Needs 'smarter' move generation function
#Needs 'killer moves'
#Optimize evaluation function
#Needs Monte Carlo algorithm to store net results of moves to allow for a statistical measure of 'how good' in future games

import Queue
import Math


#AI parameters: lists storing weights for different behaviors (to be used in evaluation function):
#1st: preference to group pieces (create strong positions)
#2nd: preference to block incoming pieces (balanced positions)
#3rd: preference to advance quickly (low value means low emphasis on board positioning, focused on piece orientation)
#4th: preference to go after weak enemy positions (maximize positive difference between your position and nearby enemy position)
#5th: rabbit score multiplier with closeness to goal
flanking = [2., 1.5, 1., 1.7,5.] #try to create a strong position and push with it
divideAndConquer = [1., 2., 1.5, 1.7,5.] #Maintain board control
defensive = [1., 2., 0.3, 1.3,5.] #advance slowly and try to stonewall or capture enemy pieces
charger = [1.5, 1., 1.5, 2.,5.] #Try to find a weak spot in enemy line and capitalize on it

AI = flanking #what evaluation parameters to use


#Negascout is a variant of minimax with alpha-beta pruning
#Depth is how much deeper to go, alpha and beta are the cutoff parameters
#Board contains the state of the board at this level, and the moves made to get to that state
#Alpha and beta should initially be called with very large values


#boardState/board = 8x8 array containing the value of the piece in each position (negative for opponent's piece)
#alpha/beta = value
#depth = int
#turn = int, 1 = gold, -1 = silver
def negascout(depth, alpha, beta, board, turn):
    if (depth == 0):
        return evaluate(board, turn) #returns the strength value of the board

    turnList = generateMoves(board, turn) #moveList contains a set of turns (containing move sets)


    for moveList in turnList:
        newBoard = makeMove(board, moveList)
                
        val = -negascout(depth - 1, -beta, -alpha, newBoard, -turn) #descend one level and invert the function

        if (val >= beta):
            return beta
        if (val > alpha):
            alpha = val

    return alpha


#moves piece positions
#board = 8x8 array with piece values
#moveList = move piece in what position to what position = [move1,move2,move3,move4]
#move = [xinitial,yinitial,xfinal,yfinal], (if xfinal is 99, remove piece from game)
def makeMove(board, moveList):
    for move in moveList:
        if (xfinal != 99):
            board[xfinal,yfinal] = board[xinitial,yinitial]
        board[initial,yinitial] = 0
    return board
    
'''unfinished, needs to value rabbits getting to goal state among other additions to evaluation function'''
#evaluates the strength of the board
#returns a value and the moves to get to the board setup
def evaluate(board, turn):
    board = board * turn #invert piece values on silver's turn
    ai = getAI()
    groupedScore = 0 #power score of held board positions
    xPosScore = 0 #defensive line score
    yPosScore = 0 #closeness to goal score
    differenceScore = 0 #difference between enemy positions and this player's positions
    
    for x in range(0,7):
        for y in range(0,7):
            groupedScore = groupedScore + groupScore(board, x, y)

'''unfinished'''
def groupScore(board, x,y):
    count = 0
    score = 0
    for (x1 in range(-4,4)):
        if (board[x+x1,y] > 0 and x1 != 0 and x+x1 >-1 and x+x1 < 8):
            count = count + 1
            score = score + board[x1,y]/Math.abs(x-x1)
    for (y1 in range(-4,4)):
        if (board[x,y1] > 0 and y1 != 0 and y+y1 < 8 and y+y1 >-1):
            count = count + 1
            score = score + board[x,y1]/Math.abs(y-y1)
    for (x2 in range (-3,3)):
         for (y2 in range (-1,1)):
              pass
    
def defensiveScore(board):
    pass

def offensiveScore(board):
    pass

def matchedScore(board):
    pass

def rabbitScore(board):
    pass


def getAI():
    return AI

def setAI(ai):
    AI = ai


'''unfinished'''
#generate the child boards of the passed board
#should modify not to generate identical moves, null moves
#returns [[move01,move02,move03,move04],[move11,move12,move13,move14],....[moveN1,moveN2,moveN3,moveN4]
#move = [[xinitial,yinitial],[xfinal,yfinal]]
def generateMoves(board, turn):
    possibleMoves = Queue() #for each position, store possible moves
    board = board * turn #invert the piece values on silver's turn
    for moveNum in range(0,3) #loop for each move in the turn
        for x in range(0,7): #loop over full board
            for y in range(0,7):
                moves = []
                if isValid(board, x, y, x-1, y) == 0:
                    pass #unfinished
'''unfinished'''
#Checks if a move is legal
#Returns -1 if it's not, 0 if it is, 1 if it's a special case (push or pull)
#This and generateMoves need to be modified to accept the possibility of a pull
def isValid(board, x, y, x2, y2, turn):
    if (board[x,y] == 0): #check if a piece exists to move
        return -1
    elif (x2 < 0 or x2 > 7 or y2 < 0 or y2 > 7): #check if position is on board
        return -1
    elif (board[x2,y2] > 0): #make sure it's not trying to move into a position occupied by one of its own pieces
        return -1
    elif ((board[x,y] == 1) and y2 = y - turn): #make sure the computer isn't trying to move its rabbits (pawns) backwards
        return -1
    enemy = 0 #strength of most powerful adjacent enemy
    ally = 0  #strength of most powerful adjacent ally
    if (x-1 >= 0): #next several statements make sure piece is not frozen
        piece = board[x-1,y]
            enemy = piece
        elif (piece > ally):
            ally = piece
    if (x+1 < 8):
        piece = board[x+1,y]
        if (piece < enemy):
            enemy = piece
        elif (piece >ally):
            ally = piece
    if (y - 1 >= 0):
        piece = board[x,y-1]
        if (piece < enemy):
            enemy = piece
        elif (piece >ally):
            ally = piece
    if (y + 1 < 8):
        piece = board[x,y+1]
        if (piece < enemy):
            enemy = piece
        elif (piece >ally):
            ally = piece
    if (enemy > board[x,y] and ally < 1): #piece is frozen
        return -1
    if (board[x,y] + board[x2,y2] <= 0): #trying to move into the position of an enemy piece that's as strong or stronger
        return -1
    elif (board[x2,y2] != 0): #a push
        return 1 #return 1 on push or pull
    return 0
    
