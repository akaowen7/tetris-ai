import numpy as np
import Permutation_Generator as Perm_Gen

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
    
    # Factor parameters
    holes_param = 1 # a
    height_param = 1 # b
    variance_param = 1 # c
    lines_param = 1 # d

    def find_next_move(self):
        # calc all permutations of next piece
        perms = Perm

        calculated_values = []
        for board in perms:
            calculated_values.append(board, self.find_board_value(board))

        calculated_values.sort(key=lambda x: x[1])

        # returns only the board, WE NEED TO FIND THE MOVE
        return calculated_values[0][0]


    def find_board_value(self, board):
        return (self.holes(board) * self.holes_param) + (self.board_height(board) * self.height_param) + (self.surface_variance(board) * self.variance_param) +(self.complete_lines(board) * self.lines_param)

    def holes(_, board: np.array):
        return 1

    def board_height(_, board: np.array):
        max_height = 0

        for i in range(board.shape[1]):
            col = board[:, i] # Gets columns

            print(col)

            blocksInCol = np.where(col == 1)[0]
            if blocksInCol.size > 0 and (board.shape[0] - blocksInCol[0]) > max_height:
                max_height = board.shape[0] - blocksInCol[0]

        return max_height - 1 # Subtract 1 to make it 0-indexed
    

    def surface_variance(_, board):
        colHeights = []
        for i in range(board.shape[1]):
            col = board[:, i] # Gets columns

            blocksInCol = np.where(col == 1)[0]
            height = 0
            if blocksInCol.size > 0:
                height = board.shape[0] - blocksInCol[0]
            colHeights.append(height)

        print(colHeights)
        
        return sum(abs(colHeights[i] - colHeights[i + 1]) for i in range(len(colHeights) - 1))

    def complete_lines(_, board):
        completeLineCount = 0

        for row in board:
            if 0 not in row:
                completeLineCount += 1
        return completeLineCount
    
boardEvalObj = Board_Evaluator(sample_board)

print("Max height: ", boardEvalObj.board_height(sample_board))
print("Surface variance: ", boardEvalObj.surface_variance(sample_board))
print("Complete lines: ", boardEvalObj.complete_lines(sample_board))
