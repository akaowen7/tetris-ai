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
    height_param = -0.35 # b
    variance_param = -0.18 # c
    lines_param = 0.76 # d
    
    def find_board_heights(self, board):
        heights = []
        for i in range(board.shape[1]):
            col = board[:, i] # Gets columns
            filledCells = np.where(col != 0)[0]
            if len(filledCells) == 0:
                heights.append(0)
            else:
                heights.append(filledCells[0])
        print(heights)
        return heights

    def find_board_value(self, board):
        return ((self.holes(board) * self.holes_param) + (self.board_height() * self.height_param) + (self.surface_variance() * self.variance_param) + (self.complete_lines(board) * self.lines_param))

    def holes(self, board: np.array):
        edges = Edge_Tracer.Edge_Tracer(board).generate_path()
        holes = 0

        for i in range(board.shape[1]):
            col = board[:, i]
            lowestEdge = max([edge for edge in edges if edge[1] == i], key=lambda x: x[0])[0]
            holes += np.where(col[lowestEdge + 1::] == 0)[0].shape[0]

        return holes

    def board_height(self):
        max_height = 0

        for height in self.heightsOfCols:
            if height > max_height:
                max_height = height

        return max_height - 1 # Subtract 1 to make it 0-indexed
    

    def surface_variance(self):        
        return sum(abs(self.heightsOfCols[i] - self.heightsOfCols[i + 1]) for i in range(len(self.heightsOfCols) - 1))

    def complete_lines(_, board):
        completeLineCount = 0

        for row in board:
            if 0 not in row:
                completeLineCount += 1
        return completeLineCount
    
boardEvalObj = Board_Evaluator(sample_board)

print("Max height: ", boardEvalObj.board_height())
print("Surface variance: ", boardEvalObj.surface_variance())
print("Complete lines: ", boardEvalObj.complete_lines(sample_board))
print("Holes: ", boardEvalObj.holes(sample_board))
