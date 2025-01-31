import numpy as np
import Edge_Tracer as Edge_Tracer

sample_board = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0], 
    [1, 1, 1, 0, 0, 0, 1, 1, 1, 0], 
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0], 
    [1, 0, 0, 1, 0, 1, 1, 1, 1, 0], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0]])

class Board_Evaluator:
    def __init__(self, initial_board):
        self.initial_board = initial_board # 20 x 10 np array
        self.heightsOfCols = self.find_board_heights(initial_board)
    
    # Factor parameters
    holes_param = -0.51 # a
    height_param = -0.28 # b
    variance_param = -0.15 # c
    lines_param = 0.76 # d
    overhang_param = -0.41 # e
    
    def find_board_heights(self, board):
        heights = []
        for i in range(board.shape[1]):
            col = board[:, i] # Gets columns
            filledCells = np.where(col != 0)[0]
            if len(filledCells) == 0:
                heights.append(0)
            else:
                heights.append(20 - filledCells[0])
        return heights

    def find_board_value(self):
        return ((self.overhangs(self.initial_board) * self.overhang_param) + (self.holes(self.initial_board) * self.holes_param) + (self.board_height() * self.height_param) + (self.surface_variance() * self.variance_param) + (self.complete_lines(self.initial_board) * self.lines_param))

    def overhangs(self, board: np.array):
        overhangs = 0
        for i in range(board.shape[1]):
            col = board[:, i]
            count = False
            for j in range(len(col)):
                if count:
                    if col[j] == 0:
                        overhangs += 1
                else:
                    count = (col[j] == 1)
        return overhangs
    
    def holes(self, board: np.array):
        edges = [(edge[0][0], edge[0][1]) for edge in Edge_Tracer.Edge_Tracer(board).generate_path()]

        holes = 0

        for i in range(board.shape[1]):
            col = board[:, i]
            lowestEdge = max([edge for edge in edges if edge[1] == i], key=lambda x: x[0])[0]
            # print(lowestEdge)
            holes += np.where(col[lowestEdge + 1::] == 0)[0].shape[0]

        return holes

    def board_height(self):
        return sum(self.heightsOfCols)/len(self.heightsOfCols)

    def surface_variance(self):        
        return sum(abs(self.heightsOfCols[i] - self.heightsOfCols[i + 1]) for i in range(len(self.heightsOfCols) - 1))

    def complete_lines(_, board):
        completeLineCount = 0

        for row in board:
            if 0 not in row:
                completeLineCount += 1
        return completeLineCount
    
# boardEvalObj = Board_Evaluator(sample_board)

# print("Max height: ", boardEvalObj.board_height())
# print("Surface variance: ", boardEvalObj.surface_variance())
# print("Complete lines: ", boardEvalObj.complete_lines(sample_board))
# print("Holes: ", boardEvalObj.holes(sample_board))
