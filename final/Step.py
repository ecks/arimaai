'''
Filename: Step.py
Description: Step object to hold a step and pertinent information about the step.
Steps come in the form of Ra2n, Dd2n, Rc3x, etc.

@author: et
'''

import string
import Piece

class Step(object):

    # Some pseudo enum types to be used for determining
    # what the next move can/must be.
    # See  __nextMoveType in MoveGenerator.py
    REGULAR = 0
    CAN_PULL = -1
    MUST_PUSH = 1
    CAPTURE = 2

    ##
    # Constructor for a Step object.
    # @param step - Arimaa step to be processed for our game. (something like Cc1n)
    def __init__(self, step):
        
        self.arimaa_step = step
        
        if (step == ""):
            return
        
        self.piece = step[0:1]                # C
        self.start_col = step[1:2]            # c
        self.start_row = step[2:3]            # 1
        self.dir = step[3:4]                  # n
        
        # Get the correct color.
        self.color = Piece.pieceColor(self.piece)
        
        # Make the translation table for columns
        transTable = string.maketrans("abcdefgh", "12345678")
        self.start_col = string.translate(self.start_col, transTable)  # Translate the column
        
        # Our notation is flipped from the Arimaa board.
        # Also we start at 0 not 1.
        self.start_row = 8 - int(self.start_row)
        self.start_col = int(self.start_col) - 1
        
        self.end_row = self.start_row
        self.end_col = self.start_col
        
        if self.dir == "n":
            self.end_row = self.end_row - 1
        elif self.dir == "s":
            self.end_row = self.end_row + 1
        elif self.dir == "w":
            self.end_col = self.end_col - 1
        elif self.dir == "e":
            self.end_col = self.end_col + 1
        elif self.dir == "x":                  # Removal of piece
            self.end_row = -1
            self.end_col = -1
        elif self.dir == "":                   # Initial placement of piece
            self.start_row = -1
            self.start_col = -1
        
        
        self.type = Step.REGULAR
        
   
    ##
    # A string representation of this step. 
    def __str__(self):
        return self.arimaa_step
