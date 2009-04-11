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
import MoveGenerator 
import Evaluation

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

           
            eval = Evaluation.Evaluation()
            (start_row, start_col, end_row, end_col) = eval.getStrongestGrid(board, color)
           
            mv = MoveGenerator.MoveGenerator(count, color, board, hash)
            mv.MAX_STEPS = 3
            mv.genMoves("", start_row, start_col, end_row, end_col)
            turns = mv.moveStepHashes

            bestMoveStrength = -sys.maxint -1
 
            for turn in turns:
                newBoard = turn[0]
                strength = eval.evaluateBoard(newBoard, color, True)
                if strength > bestMoveStrength:
                    bestStep = turn[1]
                    bestMoveStrength = strength

            print bestStep.strip()
              
     
    else:
        print "File not found"
        
        
    sys.exit()
 
