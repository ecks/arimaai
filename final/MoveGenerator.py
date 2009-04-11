'''
Filename: MoveGenerator.py
Description: Generates all the possible moves given a board state.
 
@author: et
'''
 
import string
import re
import bisect
import Step
import copy
import Hash
import random
import Board
import Step
import Piece
import Common

 
class MoveGenerator(object):
 
 
    # Most amount of steps we can make in a single turn.
    MAX_STEPS = 3
 
    ##
    # MoveGenerator constructor
    # @param turn - the turn number
    # @param color - whose turn is it (white or black)
    # @param board - the parsed board, 2 dimensional array.
    def __init__(self, turn, color, board, hash):
        self.turn = turn
        self.color = color
        self.board = board
 
        # An object of class Hash.
        self.hash = hash  

        # moveSteps is a list of tuples.
        # Each tuple contains a new board state and the steps that were
        # taken to get there from the original board state.
        self.moveStepHashes = []

        self.hashkeys = []
        
        # Going to need to hold onto the original board
        # state because we're going to making a lot of
        # new boards.
        self.original_board = copy.deepcopy(self.board)
        
    ##
    # Generates all possible moves in a given area.
    # @param steps_in - list of steps already taken (a move is a list of steps).
    # @param start_row - the starting row of the given area
    # @param start_col - the starting column of the given area
    # @param end_row - the ending row of the given area
    # @param end_col - the ending column of the given area
    # @return If we have no more valid moves for a given recursive call.
    def genMoves(self, steps_in, start_row = 0, start_col = 0, end_row = 7, end_col = 7):            
        steps = []
        moves = []
        
        self.__updateBoard(steps_in)

        # Construct Step objects out of all the previous steps
        # taken.
        for step_in in steps_in.split():
            step = Step.Step(step_in)
            steps.append(step)
        
        # Next steps are all the steps that are possible given the starting steps
        # from steps_in. The steps are sorted by which piece you attempt to move.
        next_steps = self.__genSteps(steps, start_row, start_col, end_row, end_col)
        
        prev_steps = "".join(steps_in) # if all items are strings
 
        # If genSteps gave us no more valid moves left, then we need to
        # escape this recursive call.
        if len(next_steps) <= 0:
            return
        else:
            for steps in next_steps:
                for step in steps:
                    
                    all_steps = prev_steps + " " + "".join(step)
                    
                    self.board = copy.deepcopy(self.original_board)
                    all_steps_with_traps = self.__updateBoard(all_steps)
                    
                    # If we're not currently in a push, we can print this step out.
                    if not self.__nextMoveTypeStr(all_steps_with_traps) == Step.Step.MUST_PUSH:
                        if not self.board == self.original_board:
                            hashkey = self.hash.getFinalHash()

                            # If item not found, tell us where to insert it,
                            # otherwise tell us that right in that index is the item
                            ins_pt = bisect.bisect_left(self.hashkeys,hashkey) 
                              
                            # short circuit for when we are appending to list
                            if len(self.hashkeys) == ins_pt or hashkey != self.hashkeys[ins_pt]:             
                             
                                 # This is definitely not a duplicate entry.
                                 self.hashkeys.insert(ins_pt, hashkey)
                                 self.moveStepHashes.append((self.board, all_steps_with_traps, hashkey))
                                 #print all_steps_with_traps, hashkey
				 #Common.displayBoard(self.board)
                    # Generate more moves with the updated board.
                    self.genMoves(all_steps, start_row, start_col, end_row, end_col)   
            
    ##
    # Update the board with a new move.
    # @param step - the step to change the board with
    # @return final_steps - the steps including trapped piece steps
    def __updateBoard(self, steps):
 
        # Needs to be called before using updateHashkey so that hashkey can reinitialize itself
        # Only needs to be reinitialized when not currently in a push
        if not self.__nextMoveTypeStr(steps) == Step.Step.MUST_PUSH:
           self.hash.initTempHashKey()
        
        
        # The steps with any traps done.
        final_steps = ""
        
        for step in steps.split():
            final_steps = final_steps + " " + step
            step = Step.Step(step)

            # The piece we are trying to move
            piece = self.board[step.start_row][step.start_col]

            # Update the hash for this position.
            self.hash.updateHashKey(step.start_row, step.start_col, piece, " ")

            # Delete the pieces starting position
            if (step.start_row == 2 and step.start_col == 2) or \
               (step.start_row == 2 and step.start_col == 5) or \
               (step.start_row == 5 and step.start_col == 2) or \
               (step.start_row == 5 and step.start_col == 5):
                self.board[step.start_row][step.start_col] = "X"
            else:   
                self.board[step.start_row][step.start_col] = " "
            
            # Put this piece in its new place
            self.board[step.end_row][step.end_col] = step.piece 
            
            trapped_piece = ""
            # Is the piece in a trap square?
            if not Board.isSafe(self.board, 2, 2):
               trapped_piece = self.board[2][2] + "c6x"
               self.board[2][2] = "X"
            elif not Board.isSafe(self.board, 2, 5):
               trapped_piece = self.board[2][5] + "f6x"
               self.board[2][5] = "X"
            elif not Board.isSafe(self.board, 5, 2):
               trapped_piece = self.board[5][2] + "c3x"
               self.board[5][2] = "X"
            elif not Board.isSafe(self.board, 5, 5):
               trapped_piece = self.board[5][5] + "f3x"
               self.board[5][5] = "X"
           
            piece = self.board[step.end_row][step.end_col] 
            self.hash.updateHashKey(step.end_row, step.end_col, " ", piece)    
            
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
    # Generates a list of steps given 0 or more previous steps.
    # @param steps - a list of steps to be processed before new ones can be generated.
    # @param start_row - the starting row of the given area
    # @param start_col - the starting column of the given area
    # @param end_row - the ending row of the given area
    # @param end_col - the ending column of the given area
    # @return moves - a list of moves (a list of steps) we can make at this position.
    def __genSteps(self, steps, start_row, start_col, end_row, end_col):
        moves = []
        steps_left = MoveGenerator.MAX_STEPS
        last_step = Step.Step("")
        push = ""
        
        # Go through all the previous steps.
        # Decrement number of steps left and determine what the last step was.
        # We need to know the last step for pushes and pulls.
        for step in steps:
            if step.dir != "x" or step.dir != "X":
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
            occ_adj_pos = Board.getAdjacentPositions(self.board, last_step.start_row, last_step.start_col, True)
            for pos in occ_adj_pos:
                row = pos[0]
                col = pos[1]
                piece = self.board[row][col]
                color = Piece.pieceColor(piece)
                if piece == " " or piece == "x" or piece == "X":
                    continue
                # A piece can't move into it's friendly space.
                elif color != last_step.color:
                    # See if this piece is stronger than the one that was just moved
                    if Piece.isStronger(piece, last_step.piece):
                        
                        # Can this piece even move? Or is it frozen.
                        if not Board.isFrozen(self.board, piece, row, col):
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
                                    
                    piece_color = Piece.pieceColor(piece)
                    
                    # Get all the unoccupied and occupied adjacent positions to this piece
                    unocc_adj_pos = Board.getAdjacentPositions(self.board, row, col, False)
                    occ_adj_pos = Board.getAdjacentPositions(self.board, row, col, True)
                    
                    # Only generate moves for the current player
                    if piece_color == self.color:
    
                        # Is the piece NOT frozen
                        if not Board.isFrozen(self.board, piece, row, col):
                            unocc_adj_pos = self.__adjustRabbitPositions(piece, row, col, unocc_adj_pos)
                            step = self.__makeStep(piece, row, col, unocc_adj_pos)
                            moves.append(step)
                            
                    # If we're here, then we found the opponent piece.
                    # Lets see if we can push or pull it.
                    else:
                        
                        # Try doing a pull if the last move we did can initialize a pull.
                        if (next_move_type == Step.Step.CAN_PULL):
                            
                            # Get all the occupied positions to the last step.
                            prev_adj_occ_pos = Board.getAdjacentPositions(self.board, last_step.start_row, last_step.start_col, True)
                            for prev_adj_pos in prev_adj_occ_pos:
                                if piece_color != self.color and \
                                   Piece.isStronger(last_step.piece, piece):
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
                                adj_color = Piece.pieceColor(adj_piece)
                                if adj_color == self.color and \
                                    Piece.isStronger(adj_piece, piece):
                                    if not Board.isFrozen(self.board, adj_piece, row, col):
                                        step = self.__makeStep(piece, row, col, unocc_adj_pos)
                                        moves.append(step)
                                
                
        return moves
        
    
    def __nextMoveTypeStr(self, stepsStr):
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
            if step.dir == "x" or step.dir == "X":
                steps.remove(step)
    
        
        last_step = steps[-1]
 
        
        # We may be in the process of doing a push
        # or just completing a pull.
        if last_step.color != self.color:
            
            # We just completed a pull
            if len(steps) >= 2:
                prev_step = steps[-2]
                if prev_step.start_row == last_step.end_row  and \
                   prev_step.start_col == last_step.end_col:
                    return Step.Step.REGULAR
                else:
                        return Step.Step.MUST_PUSH
            # Or we're in the middle of a push
            else:
                return Step.Step.MUST_PUSH
        else:
            # Get all the occupied adjacent positions to see if we can attempt a pull.
            adj_pos = Board.getAdjacentPositions(self.board, last_step.start_row, last_step.start_col, True)
            for pos in adj_pos:
                row = pos[0]
                col = pos[1]
                other_piece = self.board[row][col]
                # Ensure that the piece we are trying to pull is not our own.
                if Piece.pieceColor(other_piece) != self.color:
                    # Now are we actually stronger than that piece
                    if Piece.isStronger(last_step.piece, other_piece):
                        return Step.Step.CAN_PULL
        
        return Step.Step.REGULAR


    
    ##
    # If this is a rabbit, then remove the southern position
    # because rabbits can't move south on their own.
    # It's important to remember that our board's 0,0 position
    # starts in the top left corner. Also it should be noted
    # that a south move for black is different from a south move for white
    # since black is always at the top of the table and white is at the
    # bottom of the table.
    # @param piece - the piece in question
    # @param row - the piece's row
    # @param col - the piece's column
    # @param positions - list of positions generated from __getAdjacentPositions
    # @return positions - the same list of positions, or positions without a south direction.
    def __adjustRabbitPositions(self, piece, row, col, positions):
        if piece == "R":
            i = 0
            for position in positions:
                positionRow = position[0]
                if positionRow > row:
                    del positions[i]
                    break
      
            i = i + 1
        elif piece == "r":
            i = 0
            for position in positions:
                positionRow = position[0]
                if positionRow < row:
                    del positions[i]
                    break
          
            i = i + 1

        return positions
    
    
    

    
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
            piece_col_letter = string.translate(repr(piece_col), transTable) # Translate the column
            
            step = piece + piece_col_letter + repr(piece_row) + dir
            
            steps.append(step)
        
        return steps


    ##
    # Generates a random starting position based on whose turn it is.
    # These are predefined as good starting positions.
    # @param color - whose color it is.
    # @return setup - an optimal starting position.
    @staticmethod
    def randSetup(color):
        if color == 'w' or color == 'g':
            setup = ['Ee2 Md2 Ca1 Dc2 Hb2 Hg2 Ch1 Df2 Rb1 Rc1 Rd1 Re1 Rf1 Rg1 Ra2 Rh2',
                     'Ee2 Md2 Da1 Hb2 Dh1 Hg2 Cf1 Cc1 Rb1 Rd1 Re1 Rg1 Ra2 Rc2 Rf2 Rh2',
                     'Ee2 Md2 Hh2 Dg2 Db1 Ca2 He1 Cf1 Ra1 Rc1 Rd1 Rg1 Rh1 Rb2 Rc2 Rf2',
                     'Ee2 Md2 Ha2 Hh2 Db2 Dg2 Cc2 Cf2 Ra1 Rb1 Rc1 Rd1 Re1 Rf1 Rg1 Rh1']
        else:
            setup = ['ee7 md7 ha7 hh7 db7 dg7 cf8 cc8 rc7 rf7 ra8 rb8 rd8 re8 rg8 rh8',
                     'ha7 hh7 dg7 me7 ed7 cc8 cf8 da8 rb7 rc7 rf7 rb8 rd8 re8 rg8 rh8',
                     'ee7 md7 ha7 hh7 db7 dg7 cf8 cc8 rc7 rf7 ra8 rb8 rd8 re8 rg8 rh8',
                     'me7 ed7 ha7 hh7 db7 dg7 cc8 cf8 rc7 rf7 ra8 rb8 rd8 re8 rg8 rh8']
 
        return setup[random.randint(0,3)]
