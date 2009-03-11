

moves
board_states

# true for gold, false for silver
turn = True

cToNum = dict(zip(map(chr,range(97,105)),range(0,8))) # easy way to go from char to int, so cToNum['a'] => 0 .. cToNum['h'] => 7


pieces = {'.' : 0,
               'E' : 6,
               'e' : 6,

               'M' : 5,
               'm' : 5,

               'H' : 4,
               'h' : 4,

               'D' : 3,
               'd' : 3,

               'C' : 2,
               'c' : 2,

               'R' : 1,
               'r' : 1
              }



def receiveInput (moveArg):

    mv = moveArg.split();
    mvNum = mv[0][0];
    mvColor = mv[0][1];



    mvList = mv[1:];

    for move in range(1:len(mvList)):
    if piece < 'A':
       push(mvList[move], mvList[move+1])
            

def push(mv1, mv2):
  if (mv1[0] < mv2[0]):
     if (mv2[3] == 'w'):
       if  

 
    if (turn):
      for move in range(1:len(mvList)):
        piece = mvList[move][0]
        col = cToNum[mvList[move][1]
        row = mvList[move][2]
        dir = mvList[move][3]


        if (move < len(mvList)):
          next_piece = mvList[move + 1][0]
          next_col = cToNum[mvList[move + 1][1]
          next_row = mvList[move + 1][2]
          next_dir = mvList[move + 1][3]
            
            
        


    turn = !turn
    
    


def setup():
    mv = moveArg.split();
    mvNum = mv[0][0];
    mvColor = mv[0][1];
    mvList = mv[1:];



def setup_board(moveList)   
    




