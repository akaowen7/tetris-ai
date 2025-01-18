import numpy as np
from Tetris import Piece

class Permutation_Generator:
    def __init__(self, initial_board: np.array, next_piece: Piece):
        """
        initial_board (np.array): 10 x 20 array of the current board state
        next_piece (Piece): The next piece to be placed on the board
        """
        self.initial_board = initial_board # 10 x 20 np array
        self.next_piece = next_piece

    def generate(self):
        """
        Generates all possible permutations of the board state
        
        Returns: 
        perms (np.array): Array of tuples of (board_state_with_piece, piece_by_itself_on_empty_board)"""
        
        perms = []
        
        # Def rotation-point of next_piece

        # Find "open air" spaces

        # For space in open_spaces:
            # For rotation in next_piece.rotations:

                # Check if placement is valid

                # If so: perms.append(board_state)

        return perms