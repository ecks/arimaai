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
        (count, color, steps, board) = parser.parse() # Parse the file.
        file.close()

        hash = Hash.Hash()  # Construct a new hash
        hash.calculateHashkey(board)  # Calculate the hash key for this given board.
    
	eval = Evaluation.Evaluation()
	print(eval.negascout(1,-999999, 999999, board, color,steps, count, hash))
        
        # Generate all the possible moves for this board.
#        generator = MoveGenerator.MoveGenerator(count, color, board, hash)
#        generator.genMoves(steps)
     
     
    else:
        print "File not found"
        
        
    sys.exit()
 
