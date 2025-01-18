import Board_Evaluator as Board_Eval
import numpy as np
import Permutation_Generator as Perm_Gen

class Move_Recommender:
    def __init__(self, initial_board, next_piece):
        """
        initial_board (np.array): 10 x 20 array of the current board state
        next_piece (Piece): The next piece to be placed on the board
        """
        self.initial_board = initial_board # 20 x 10 np array
        self.next_piece = next_piece

        self.permGen = Perm_Gen.Permutation_Generator(self.initial_board, self.next_piece)
        self.boardEval = Board_Eval.Board_Evaluator(self.initial_board)

    def recommend_move(self):
        """
        Provides the best move to make given the current board state and the next piece
        
        Outputs:
        best_move (np.array[(np.array)]): List of the best moves to make"""

        perms = self.permGen.generate(self.initial_board, self.next_piece)

        calculated_values = []
        for board in perms:
            calculated_values.append((board[0], board[1], Board_Eval.Board_Evaluator(board).find_board_value()))

        calculated_values.sort(key=lambda x: x[2])

        outputted_moves = []
        for i in range(3):
            outputted_moves.append(calculated_values[i][0])
        
        return outputted_moves