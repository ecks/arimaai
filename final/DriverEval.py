'''
Filename: Driver.py
Description: Driver class to run our bot.
 
@author: et
'''
 
import sys
import os.path
import Parser
import Evaluation
import Hash 
import random
import Common
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
        file = open(input, 'r') # open file for reading
        parser = Parser.Parser(file) # construct new parser object.
        (turn, color, steps, board) = parser.parse() # Parse the file.
        file.close()

        eval = Evaluation.Evaluation(board)
        print eval.evaluateBoard(color)

     
    else:
        print "File not found"
        
        
    sys.exit()
 
