'''
Filename: Driver.py
Description: Driver class to run our bot.

@author: et
'''

import sys
import os.path
import Parser
import MoveGenerator


if __name__ == '__main__':
    
    # There were no command line arguments, ask for position file name.
    if len(sys.argv) < 2:
        print "Please enter the input position filename:"
        input = sys.stdin.readlines()
    # Take in from command line arguments
    else:
        input = sys.argv[1] # sys.argv[0] is this file's name (Driver.py)
    
    # Does this input exists and is input a file (not a directory).
    if os.path.exists(input) or os.path.isfile(input):
        print "Using file: " + input
        file = open(input, 'r')      # open file for reading
        parser = Parser.Parser(file) # construct new parser object.
        (count, color, steps, board) = parser.parse() # parse out the juicy stuff
        file.close()
        
        generator = MoveGenerator.MoveGenerator(count, color, steps, board)
        generator.genMoves()
    else:
        print "File not found"
        
        
    sys.exit()