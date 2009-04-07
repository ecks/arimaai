'''
Filename: MoveGenerator.py
Description: Generates all the possible moves given a board state.

@author: et
'''

import string
import re
import Step
import copy
import bisect
import math

class MoveGenerator(object):


    # Currently setting max steps to 2 so we can actually see the results finish.
    MAX_STEPS = 4

    ##
    # MoveGenerator constructor
    # @param count - the turn number
    # @param color - whose turn is it (white or black)
    # @param board - the parsed board, 2 dimensional array.
    # @param hashkey - hashkey of the initial board state
    def __init__(self, count, color, board):
        self.count = count
        self.color = color
        self.board = board
        self.moveSteps = []

        
        # Going to need to hold onto the original board
        # state because we're going to making a lot of
        # new boards.
        self.original_board = copy.deepcopy(self.board)

    #Paul Abbazia
    #boardState/board = 8x8 array containing the value of the piece in each position (negative for opponent's piece)
    #alpha/beta = value
    #depth = int
    #turn = int, 1 = white, -1 = black
    def negascout(self, depth, alpha, beta, board, turn):
        if (depth == 0):
            return self.evaluate(board, turn) #returns the strength value of the board

        averages = self.boardStrength()
        if turn == 1: #white's turn
            pass
        turnList = self.genMoves(self,[],0,0,7,7) #moveList contains a set of turns (containing move sets)


        for moveList in turnList:
            newBoard = makeMove(board, moveList)
                    
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
    #Player 'gains' sum of own pieces - sum of enemy pieces
    #@board the board state to evaluate
    #@return the value of this board state
    def evaluate(self, board):
        value = 0
        if self.color == 'white':
            for col in range(0,8):
                for row in range(0,8):
                    piece = board[row,col]
                    if piece >= 'A':
                        value += self.__pieceValue(piece)
                        if piece != 'R':
                            value += self.__pieceValue(piece) * (row+1)
                        elif piece == 'R':
                            value += self.__pieceValue(piece) * (row+1)**2

                    if piece < 'A':
                        value -= self.__pieceValue(piece)
        elif self.color == 'black':
            for col in range(0,8):
                for row in range(0,8):
                    piece = board[row,col]
                    if piece < 'A':
                        value += self.__pieceValue(piece)
                        if piece != 'r':
                            value += self.__pieceValue(piece) * (row+1)
                        elif piece == 'r':
                            value += self.__pieceValue(piece) * (row+1)**2

                    if piece >= 'A':
                        value -= self.__pieceValue(piece)
        return value
            

    #Paul Abbazia
    #Computes a running average of piece values to narrow search space (a 4x4 grid is chosen to try to contain pieces that could potentially effect the area)
    #Returns a list of two board states, one containing the strength of the white player, the other the black
    def boardStrength(self):
        white = copy.deepcopy(self.board)
        black = copy.deepcopy(self.board)

        for row in range(0,8):
            for col in range(0,8):
                indices = [] #the indices of the moves concerned
                for x in range(-4,4): #subscript a 4x4 moving grid
                    for y in range(-4,4):
                        indices.append([math.abs(row + x), math.abs(col+y)])#take the absolute value to avoid going out of bounds
                white[row,col] = average(indices,16,white,1)
                black[row,col] = average(indices,16,white,-1)
        return [white,black]

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
    # Generates all possible moves in a given area.
    # @param steps_in - list of steps already taken (a move is a list of steps).
    # @param start_row - the starting row of the given area
    # @param start_col - the starting column of the given area
    # @param end_row - the ending row of the given area
    # @param end_col - the ending column of the given area
    # @return moves - a list of moves (a move is a list of steps)
    def genMoves(self, steps_in, start_row = 0, start_col = 0, end_row = 7, end_col = 7):
                
        steps = []
        moves = []
        
        # Construct Step objects out of all the previous steps
        # taken.
        for step_in in steps_in.split():
            step = Step.Step(step_in)
            steps.append(step)
        
        # Next steps are all the steps that are possible given the starting steps 
        # from steps_in. The steps are sorted by which piece you attempt to move.
        next_steps = self.__genSteps(steps, start_row, start_col, end_row, end_col)
        
        prev_steps =  "".join(steps_in) # if all items are strings

        if len(next_steps) <= 0:
            return 
        else:
            for steps in next_steps:
                for step in steps:
                    
                    all_steps = prev_steps + " " + "".join(step)
                    
                    self.board = copy.deepcopy(self.original_board)
                    all_steps_with_traps = self.__updateBoard(all_steps)
                    
                    # If we're not currently in a push, we can print this step out.
                    if not self.__nextMoveTypeStr(all_steps) == Step.Step.MUST_PUSH:
                        # Make this move actually changes the board state.
                        if not self.board == self.original_board:
                             print all_steps_with_traps
                             self.__displayBoard()
                    else:
                        pass

                    
                    self.genMoves(all_steps, start_row, start_col, end_row, end_col)
                    

    # global displaying
    def displayBoard(self, aBoard):
         print " ",
         for letter in range(97, 105):
             print chr(letter),
         print

         rowNum = 8
         for i in aBoard:
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
  
            
    ##
    # Update the board with a new move.
    # @param step - the step to change the board with
    # @return final_steps - the steps including trapped piece steps
    def __updateBoard(self, steps):
        final_steps = ""
        for step in steps.split():
            final_steps = final_steps + " " + step 
            step = Step.Step(step)
        
            piece = self.board[step.start_row][step.start_col]

            self.board[step.start_row][step.start_col] = " "
            
            trapped_piece = ""
            
            # Is the piece in a trap square?
            if step.end_row == 2 and step.end_col == 2:
                if not self.__isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "c6x"
            elif step.end_row == 2 and step.end_col == 5:
                if not self.__isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "f6x"
            elif step.end_row == 5 and step.end_col == 2:
                if not self.__isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "c3x"
            elif step.end_row == 5 and step.end_col == 5:
                if not self.__isSafe(step.end_row, step.end_col):
                    trapped_piece = piece + "f3x"
            else:
                self.board[step.end_row][step.end_col] = step.piece
    
            
            if trapped_piece != "":
                final_steps = final_steps + " " + trapped_piece
        
        
        return final_steps
    
    def __displayBoard(self):
         print " ",
         for letter in range(97, 105):
             print chr(letter),
         print

         rowNum = 8
         for i in self.board:
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
    
    ##
    # Simply returns whether or not a piece has a friendly
    # piece next to it in an adjacent square. Used to check
    # trap squares.
    # @param row - the row
    # @param col - the column
    # @return True if it's safe, False otherwise.
    def __isSafe(self, row, col):
        adj_occ_pos = self.__getAdjacentPositions(row, col, True)
        for pos in adj_occ_pos:
            adj_row = pos[0]
            adj_col = pos[1]
            adj_piece = self.board[adj_row][adj_col]
            piece = self.board[adj_row][adj_col]
            if self.__areFriends(adj_piece, piece):
                return True
        
        return False
            
    
    ##      
    # Determines if two pieces are on the same team.
    # @param pieceA - the first piece
    # @param pieceB - the second piece
    # @return True if they are friends, False if they are enemies
    def __areFriends(self, pieceA, pieceB):
        if pieceA.isupper() and pieceB.isupper or pieceA.islower() and pieceB.islower():
            return True
        else:
            return False
            
    
                
    
    ##
    # Generates a list of steps given 0 or more previous steps.
    # @param steps - a list of steps to be processed before new ones can be generated.
    # @param start_row - the starting row of the given area
    # @param start_col - the starting column of the given area
    # @param end_row - the ending row of the given area
    # @param end_col - the ending column of the given area
    # @return moves - a list of moves (a list of steps) we can make at this position.
    # @return push - indicated with a dash (-) that we are in the process of doing a push
    #               and we must finish it.
    def __genSteps(self, steps, start_row, start_col, end_row, end_col):
        moves = []
        steps_left = MoveGenerator.MAX_STEPS
        last_step = Step.Step("")
        push = ""
        
        # Go through all the previous steps.
        # Decrement number of steps left and determine what the last step was.
        # We need to know the last step for pushes and pulls.
        for step in steps:
            if step.dir != "x":
                steps_left = steps_left - 1
                last_step = step
        
        if steps_left <= 0:
            return moves
        
        # Next move type gives information about what the next step can/must be
        next_move_type = self.__nextMoveType(steps)
        
        # If we're in the process of making a push, we have to complete the push.
        # Multiple pieces could move into that position, just as long as their
        # stronger and aren't on the same team.
        if next_move_type == Step.Step.MUST_PUSH:
            occ_adj_pos = self.__getAdjacentPositions(last_step.start_row, last_step.start_col, True)
            for pos in occ_adj_pos:
                row = pos[0]
                col = pos[1]
                piece = self.board[row][col]
                color = Step.Step.pieceColor(piece)
                if piece == " ":
                    continue
                # A piece can't move into it's friendly space.
                elif color != last_step.color:
                    # See if this piece is stronger than the one that was just moved
                    if self.__isStronger(piece, last_step.piece):
                        
                        # Can this piece even move? Or is it frozen.
                        piece_occ_adj_pos = self.__getAdjacentPositions(row, col, True)
                        if not self.__isFrozen(piece, piece_occ_adj_pos):
                            step = self.__makeStep(piece, row, col, [[last_step.start_row, last_step.start_col]])
                            moves.append(step)
                            
        # Were not completing a push, we are free to do what we want
        else:
            for row in range(start_row, end_row + 1):
                for col in range(start_col, end_col + 1):
                    piece = self.board[row][col]
    
                    # Don't care for blank spaces or trap squares
                    if piece == " " or re.match("x", piece, re.IGNORECASE):
                        continue
                                    
                    piece_color = Step.Step.pieceColor(piece)
                    
                    # Get all the unoccupied and occupied adjacent positions to this piece
                    unocc_adj_pos = self.__getAdjacentPositions(row, col, False)
                    occ_adj_pos = self.__getAdjacentPositions(row, col, True)
                    
                    # Only generate moves for the current player
                    if piece_color == self.color:
    
                        # Is the piece NOT frozen
                        if not self.__isFrozen(piece, occ_adj_pos):
                            unocc_adj_pos = self.__adjustRabbitPositions(piece, unocc_adj_pos)
                            step = self.__makeStep(piece, row, col, unocc_adj_pos)
                            moves.append(step)
                            
                    # If we're here, then we found the opponent piece.
                    # Lets see if we can push or pull it.
                    else:
                        
                        # Try doing a pull if the last move we did can initialize a pull.
                        if (next_move_type == Step.Step.CAN_PULL):
                            
                            # Get all the occupied positions to the last step.
                            prev_adj_occ_pos = self.__getAdjacentPositions(last_step.start_row, last_step.start_col, True)
                            for prev_adj_pos in prev_adj_occ_pos:
                                if piece_color != self.color:
                                    if self.__isStronger(last_step.piece, piece):
                                        prev_adj_row = prev_adj_pos[0]
                                        prev_adj_col = prev_adj_pos[1]
                                        if row == prev_adj_row and col == prev_adj_col:
                                            step = self.__makeStep(piece, row, col, [[last_step.start_row, last_step.start_col]])
                                            moves.append(step)
                                            
                                        
                        
                        # Try performing a push on this piece.
                        if (steps_left >= 2):
                            for pos in occ_adj_pos:
                                adj_row = pos[0]
                                adj_col = pos[1]
                                adj_piece = self.board[adj_row][adj_col]
                                adj_color = Step.Step.pieceColor(adj_piece)
                                if adj_color == self.color:
                                    if self.__isStronger(adj_piece, piece):
                                        adj_piece_occ_pos = self.__getAdjacentPositions(adj_row, adj_col, True)
                                        if not self.__isFrozen(adj_piece, adj_piece_occ_pos):
                                            step = self.__makeStep(piece, row, col, unocc_adj_pos)
                                            moves.append(step)
                                
                
        return moves
        
    
    def __nextMoveTypeStr(self, stepsStr):
        stepsStr = stepsStr.strip()
        steps = []
        for step in stepsStr.split():
            step = Step.Step(step)
            steps.append(step)
        
        return self.__nextMoveType(steps)
    
    ##
    # Determines what the next move type can/must be.
    # This is based off the last one or two steps taken.
    # For example, if the last step taken was
    # rb3e and it's white's turn, then we're in the process of
    # doing a push. We have to push on the next turn.
    # If the last step taken was something that could
    # result in a pull on the next turn we should note that too.
    # @param steps - the list of steps taken.
    # @return REGULAR, PUSH, PULL
    def __nextMoveType(self, steps):
        
        if len(steps) <= 0:
            return Step.Step.REGULAR
        
        # Get rid of traps, not necessary for this
        for step in steps:
            if step.dir == "x":
                steps.remove(step)
    
        
        last_step = steps[-1]

        
        # We may be in the process of doing a push
        # or just completing a pull.
        if last_step.color != self.color:
            
            # We just completed a pull or are in the middle of a push
            if len(steps) >= 2:
                prev_step = steps[-2]
                if prev_step.start_row == last_step.end_row:
                    if prev_step.start_col == last_step.end_col:
                        return Step.Step.REGULAR
                    else:
                        return Step.Step.MUST_PUSH
                else:
                    return Step.Step.MUST_PUSH
            else:
                return Step.Step.MUST_PUSH
        else:
            # Get all the occupied adjacent positions to see if we can attempt a pull.
            adj_pos = self.__getAdjacentPositions(last_step.start_row, last_step.start_col, True)
            for pos in adj_pos:
                row = pos[0]
                col = pos[1]
                other_piece = self.board[row][col]
                # Ensure that the piece we are trying to pull is not our own.
                if Step.Step.pieceColor(other_piece) != self.color:
                    # Now are we actually stronger than that piece
                    if self.__isStronger(last_step.piece, other_piece):
                        return Step.Step.CAN_PULL
        
        return Step.Step.REGULAR
            
    
    ##
    # Returns whether this piece is frozen.
    # @param piece - the piece
    # @param adj_pos - the adjacent positions to this piece
    # @return True if the piece is frozen, False otherwise
    def __isFrozen(self, piece, adj_pos):
        for pos in adj_pos:
            adj_row = pos[0]
            adj_col = pos[1]
            adj_piece = self.board[adj_row][adj_col]
            
            if adj_piece == " ":
                continue
            elif adj_piece.isupper() and piece.isupper():
                continue
            elif adj_piece.islower() and piece.islower():
                continue
            elif self.__isStronger(adj_piece, piece):
                return True
        
        return False
        
    ##
    # Returns all the adjacent positions (north, south, east, west),
    # that are on the board, to this piece.
    # @param row - the piece's row
    # @param col - the pieces's column
    # @param occupied - True to return only occupied space, False to return empty spaces.
    # @return pieces - the positions adjacent to this piece
    def __getAdjacentPositions(self, row, col, occupied):
        
        positions = []
        
        if occupied:
            expr = "[^ x]"
        else:
            expr = "( |x)"
            
        
        # North
        if row - 1 >= 0 and re.match(expr, self.board[row-1][col], re.IGNORECASE):
            positions.append([row - 1, col])
        
        # South
        if row + 1 <= 7 and re.match(expr, self.board[row+1][col], re.IGNORECASE):
            positions.append([row + 1, col])
        
        # West
        if col - 1 >= 0 and re.match(expr, self.board[row][col-1], re.IGNORECASE):
            positions.append([row, col - 1])
        
        # East
        if col + 1 <= 7 and re.match(expr, self.board[row][col+1], re.IGNORECASE):
            positions.append([row, col + 1])
        
        return positions
    
    ##
    # If this is a rabbit, then remove the southern position
    # because rabbits can't move south on their own.
    # @param piece - the piece in question
    # @param positions - list of positions generated from __getAdjacentPositions
    # @return positions - the same list of positions, or positions without a south direction.
    def __adjustRabbitPositions(self, piece, positions):
        if piece == "R" or piece == "r":
            del positions[1]
            
        return positions
    
    
    ##
    # Returns whether or not the first piece
    # is stronger than the second piece.
    # @param a - the first piece
    # @param b - the second piece
    # @return True if the a is stronger than b, False otherwise
    def __isStronger(self, a, b):
        a = self.__pieceValue (a)
        b = self.__pieceValue (b)
        return (a > b) 
        pass
    
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
    
    ##
    # Constructs a step in proper notation
    # given a list of positions a piece can move into.
    # @param piece - the piece to move
    # @param row - the piece's current row
    # @param col - the piece's current column
    # @param adj_pos - the list of adjacent positions to move into.
    def __makeStep(self, piece, row, col, adj_pos):
        
        steps = []
        
        for pos in adj_pos:
            
            piece_row = row
            piece_col = col
            
            adj_row = pos[0]
            adj_col = pos[1]
            
            # Moving north
            if adj_row < piece_row:
                dir = "n"
            
            # Moving south
            elif adj_row > piece_row:
                dir = "s"
            
            # Moving west
            elif adj_col < piece_col:
                dir = "w"
            
            # Moving east
            elif adj_col > piece_col:
                dir = "e"
            
            
            # Arimaa notation starts at 1, not 0
            piece_row = piece_row + 1
            piece_col = piece_col + 1
            
            # Arimaa notation for rows is flipped upside down.
            piece_row = 9 - piece_row
            
                
            # Make the translation table for columns
            transTable = string.maketrans("12345678", "abcdefgh")
            piece_col_letter = string.translate(repr(piece_col), transTable)  # Translate the column
            
            step = piece + piece_col_letter + repr(piece_row) + dir
            
            steps.append(step)
        
        return steps
