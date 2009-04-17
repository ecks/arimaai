'''
Filename: Driver.py
Description: Driver class to run our bot.
 
@author: et
'''
 
import sys
import os.path
import Parser
import Hash 
import random
import string
import Negascout
import MoveGenerator
import Common
import Minimax
 
if __name__ == '__main__':
   
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "Could not import psyco"
    
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


        if count == "1":
            print MoveGenerator.MoveGenerator.randSetup(color)
        else:           
            hash = Hash.Hash()  # Construct a new hash
            hash.calculateHashkey(board)  # Calculate the hash key for this given board.

            mini = Minimax.Minimax(board, color)
            res = mini.minimax(2, board, color, "", count, hash)
	    move = res[1].split('|')
	    print move[1].strip()
           
     
     
    else:
        print "File not found"
        
        
    sys.exit()
 
