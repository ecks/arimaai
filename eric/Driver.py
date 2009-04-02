'''
Filename: Driver.py
Description: Driver class to run our bot.

@author: et
'''

import sys
import os.path
import Parser
import MoveGenerator
import Step
import Hash
import copy
import bisect

def displayBoard(b):
         print " ",
         for letter in range(97, 105):
             print chr(letter),
         print

         rowNum = 8
         for i in b:
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
#
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
        
       	hash = Hash.Hash()
	hash.calculateHashkey(board)

	generator = MoveGenerator.MoveGenerator(count, color, board, hash)
        generator.genMoves(steps)
#	b = Board.Board(board, hash.get_hash_board())
#	b.calculateHashkey()
	# list of already determined hash keys for board states
#	hashkeys = []
	# list with moves that are not duplicates of each other
#	nonDupMoveStep = []
#	print "Before:"
	for moveStep in generator.moveSteps:
		(move,posSteps) = moveStep
		print posSteps
		displayBoard(move)
#		hashkey = b.computeHash(posSteps)
		# if item not found, tell us where to insert it, otherwise tell us 
		# that right in that index is the item
#		ins_pt = bisect.bisect_left(hashkeys,hashkey)
		# short circuit for when we are appending to list
#		if len(hashkeys) == ins_pt or hashkey != hashkeys[ins_pt]:
			# no duplicate entries
#			hashkeys.insert(ins_pt, hashkey)
#			nonDupMoveStep.append(moveStep)

#        print "After:"
#	for moveStep in nonDupMoveStep:
#	  print moveStep[1]
#	  b.displayBoard(moveStep[0])

			
#	b.updateHashKey(self.steps[0])
#	sys.stderr.write(str(generator.steps[0]))
#	sys.stderr.write(str(generator.moves[0]))
    else:
        print "File not found"
        
        
    sys.exit()
