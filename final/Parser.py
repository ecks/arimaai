'''
Filename: Parser.py
Description: Takes in a file. Parses the file and returns the
necessary output. Assumes the file is well formed to Arimaa
notation: http://arimaa.com/arimaa/learn/notation.html
 
@author: et
'''
 
import re

class Parser(object):
 
 
    ##
    # Parser construction
    # @param file - the position file, assumed to be well formed.
    def __init__(self, file):
        self.file = file
        
    ##
    # The parser method parses the file and returns the
    # necessary output.
    # @return turn - the turn number
    # @return color - whose turn is it (white or black)
    # @return steps - the steps taken so far
    # @return board - the parsed board, 2 dimensional array.
    def parse(self):
        board = [[' ' for col in range (8)] for row in range(8)]
 
        line = self.file.readline()

        expr = re.compile('\d+')
        turn = expr.match(line).group() # turn number
        
        # Sometimes the turn can come in as gold or silver.
        # We would like to change it to white or black.
        if turn == "g":
            turn = "w"
        elif turn == "s":
            turn = "b"

        expr = re.compile('\D')
        color = expr.search(line).group() # white or black
        steps = ""

        # if len(line) >= 4:
        #     steps = line[3:-1]

        lines = self.file.readlines() # the rest of the lines
        
        del lines[0:1] # get rid of the +----+
        lines.pop()
        lines.pop() # get rid of the bottom rows

        # By now, the board should like this:
        # 8|   r   r r   r   |
        # 7| m   h     e   c |
        # 6|   r x r r x r   |
        # 5| h   d     c   d |
        # 4| E   H         M |
        # 3|   R x R R H R   |
        # 2| D   C     C   D |
        # 1|   R   R R   R   |
 
        
        # We need to grab each char from the board
        # and construct a board state.
        # Row obviously starts at 0, col starts at 3 (don't forget
        # about the 0th position) because that's where chars start
        # in the above board.
        row = 0
        line_col = 3
        for line in lines:
            for col in range (8):
                char = line[line_col]
                board[row][col] = char
                line_col = line_col + 2
            row = row + 1
            line_col = 3
        
        return (turn, color, steps, board)
