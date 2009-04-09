'''
Filename: Piece.py
Description: Static methods that pertain to piece functions.
It's better to have these as static methods so they can be used
without instantiating an unnecessary object.

@author: eric
'''

class Piece(object):

    ##
    # Piece info returns the piece and it's color (white or black)
    # based on whether it's upper case or lower case.
    # If it's a blank space, color is returned as nothing.
    # @param piece - the piece
    # @return color - the piece's color 
    @staticmethod           
    def pieceColor(piece):
        if piece == " ":
            color = " "
        elif piece.isupper():
            color = "w"
        else:
            color = "b"
        
        return color
    
    ##
    # Returns the strength value of a given piece.
    # @param piece - the piece
    # @param strength - the piece's strength
    @staticmethod
    def pieceValue(piece):
        piece = piece.lower() # Make the piece lowercase.
        
        # Make the translation table for strengths
        transTable = string.maketrans("emhdcrx ", "65432100")
        strength = string.translate(piece, transTable) # Translate the piece
        return int(strength)
    
    ##
    # Returns whether or not the first piece
    # is stronger than the second piece.
    # @param a - the first piece
    # @param b - the second piece
    # @return True if the a is stronger than b, False otherwise
    @staticmethod
    def isStronger(a, b):
        a = Piece.pieceValue (a)
        b = Piece.pieceValue (b)
        return (a > b)
    
    ##
    # Determines if two pieces are on the same team.
    # @param pieceA - the first piece
    # @param pieceB - the second piece
    # @return True if they are friends, False if they are enemies
    def areFriends(pieceA, pieceB):
        if (pieceA.isupper() and pieceB.isupper) or (pieceA.islower() and pieceB.islower()):
            return True
        else:
            return False