import numpy as np

class Board_Evaluator:
    def __init__(self, initial_board):
        self.initial_board = initial_board # 10 x 20 np array
    
    # Factor parameters
    holes_param = 1
    height_param = 1
    variance_param = 1
    lines_param = 1

    def find_next_move(self):
        # calc all permutations of next piece
        perms = [0,0,0,0,0,0]

        calculated_values = []
        for board in perms:
            calculated_values.append(board, self.find_board_value(board))

        calculated_values.sort(key=lambda x: x[1])

        # returns only the board NEED TO FIND THE MOVE
        return calculated_values[0][0]


    def find_board_value(self, board):
        return (self.holes(board) * self.holes_param) + (self.board_height(board) * self.height_param) + (self.surface_variance(board) * self.variance_param) +(self.complete_lines(board) * self.lines_param)

    def holes(_, board):
        return 1

    def board_height(_, board):
        return 1

    def surface_variance(_, board):
        return 1

    def complete_lines(_, board):
        return 1
    
test = Board_Evaluator(0)

print(test.find_board_value(test.initial_board))
