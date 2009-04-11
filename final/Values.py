'''
Created on Apr 9, 2009

@author: eric
'''

INF = 9999


elephant_pos_values = [[0,1,1,2,2,1,1,0],
                       [1,2,2,3,3,2,2,1], 
                       [2,4,-4,10,10,-4,4,2],
                       [3,8,12,12,12,12,8,3],
                       [3,8,10,10,10,10,8,3],
                       [2,4,-4,10,10,-4,4,2],
                       [1,2,2,3,3,2,2,1],
                       [0,1,1,2,2,1,1,0]]

camel_pos_values = [[-2,-1,0,1,1,0,-1,-2],
                    [-1,0,1,2,2,1,0,-1],
                    [0,1,2,3,3,2,1,0],
                    [1,2,3,4,4,3,2,1],
                    [2,3,4,5,5,4,3,2],
                    [1,2,3,4,4,3,2,1],
                    [0,1,2,3,3,2,1,0],
                    [-1,0,1,2,2,1,0,-1]]

horse_pos_values = [[-2,-1,0,1,1,0,-1,-2],
                    [-1,0,1,2,2,1,0,-1],
                    [0,1,-5,3,3,-5,1,0],
                    [1,2,3,4,4,3,2,1],
                    [2,3,4,5,5,4,3,2],
                    [1,4,2,3,3,2,4,1],
                    [0,1,2,3,3,2,1,0],
                    [-1,0,1,2,2,1,0,-1]]

dog_pos_values = [[-4,-6,-6,-6,-6,-6,-6,-4],
                  [-7,-8,-10,-9,-9,-10,-8,-7],
                  [-9,-10,-12,-11,-11,-12,-10,-9],
                  [-6,-8,-9,-9,-9,-9,-8,-6],
                  [-3,-5,-6,-6,-6,-6,-5,-3],
                  [-1,-1,-2,-3,-3,-2,-1,-1],
                  [1,2,4,2,2,4,2,1],
                  [0,1,1,1,1,1,1,0]]

cat_pos_values = [[-4,-6,-6,-6,-6,-6,-6,-4],
                  [-7,-8,-10,-9,-9,-10,-8,-7],
                  [-9,-10,-12,-11,-11,-12,-10,-9],
                  [-6,-8,-9,-9,-9,-9,-8,-6],
                  [-3,-5,-6,-6,-6,-6,-5,-3],
                  [-1,-2,-2,-3,-3,-2,-2,-1],
                  [1,2,4,2,2,4,2,1],
                  [0,1,1,1,1,1,1,0]]

rabbit_pos_values_normal = [[INF,INF,INF,INF,INF,INF,INF,INF],
                            [-14,-16,-8,-16,-16,-8,-16,-14],
                            [-16,-10,-16,-10,-10,-16,-10,-16],
                            [-8,-12,-12,-12,-12,-12,-12,-8],
                            [-5,-8,-8,-8,-8,-8,-8,-5],
                            [-3,-5,-6,-6,-6,-6,-5,-3],
                            [-1,-2,-1,-4,-4,-1,-2,-1],
                            [0,0,0,0,0,0,0,0]]

rabbit_pos_values_motivate = [[INF,INF,INF,INF,INF,INF,INF,INF],
                              [25,25,25,25,25,25,25,25],
                              [20,20,20,20,20,20,20,20],
                              [16,15,14,14,14,14,15,16],
                              [8,7,6,6,6,6,7,8],
                              [4,3,2,2,2,2,3,4],
                              [2,1,1,1,1,1,1,2],
                              [0,0,0,0,0,0,0,0]]


elephant_frozen_pos_values = [[0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0]]

camel_frozen_pos_values = [[-20,-24,-28,-26,-26,-28,-24,-20],
                           [-24,-30,-20,-32,-32,-20,-30,-24],
                           [-26,-20,0,-20,-20,0,-20,-26],
                           [-16,-12,-15,-10,-10,-15,-12,-16],
                           [-10,-7,-7,-7,-7,-7,-7,-10],
                           [-6,-2,0,-2,-2,0,-2,-6],
                           [-2,-2,-2,-2,-2,-2,-2,-2],
                           [-2,-2,-2,-2,-2,-2,-2,-2]]

horse_frozen_pos_values = [[-20,-24,-28,-26,-26,-28,-24,-20],
                           [-24,-30,-20,-32,-32,-20,-30,-24],
                           [-26,-20,0,-20,-20,0,-20,-26],
                           [-16,-12,-15,-10,-10,-15,-12,-16],
                           [-10,-7,-7,-7,-7,-7,-7,-10],
                           [-6,-2,0,-2,-2,0,-2,-6],
                           [-2,-2,-2,-2,-2,-2,-2,-2],
                           [-2,-2,-2,-2,-2,-2,-2,-2]]

dog_frozen_pos_values = [[-2,-2,-3,-2,-2,-3,-2,-2],
                         [-3,-10,-5,-8,-8,-5,-10,-3],
                         [-10,-5,0,-3,-3,0,-5,-10],
                         [-3,-3,-3,-3,-3,-3,-3,-3],
                         [-1,-1,-1,-1,-1,-1,-1,-1],
                         [-1,-1,0,-1,-1,0,-1,-1],
                         [-1,-1,-1,-1,-1,-1,-1,-1],
                         [-1,-1,-1,-1,-1,-1,-1,-1]]

cat_frozen_pos_values = [[-1,-1,-2,-1,-1,-2,-1,-1],
                         [-2,-9,-5,-7,-7,-5,-9,-2],
                         [-9,-5,0,-2,-2,0,-5,-9],
                         [-2,-2,-2,-2,-2,-2,-2,-2],
                         [-1,-1,-1,-1,-1,-1,-1,-1],
                         [-1,-1,0,-1,-1,0,-1,-1],
                         [-1,-1,-1,-1,-1,-1,-1,-1],
                         [-1,-1,-1,-1,-1,-1,-1,-1]]

rabbit_frozen_pos_values = [[0,0,0,0,0,0,0,0],
                            [-1,-1,-1,-1,-1,-1,-1,-1],
                            [-1,-1,0,-1,-1,0,-1,-1],
                            [-1,-1,-1,-1,-1,-1,-1,-1],
                            [0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0]]

