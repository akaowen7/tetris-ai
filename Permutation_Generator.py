import numpy as np
import Tetris 
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
        perms (np.array): Array of board_state_with_piece"""
        
        perms = []
        
        tracedLocations = [(2,3), (1,4), (7,8)] # MAX AHHHHHH

        # makes a 2D list of all the possible (x,y)
        accepted_pos = [[(x, y) for x in range(20) if self.initial_board[y]
                        [x] == (0)] for y in range(10)]
        # removes sub lists and puts (x,y) in one list; easier to search
        accepted_pos = [x for item in accepted_pos for x in item]

        validLocations = [x for x in tracedLocations for x in accepted_pos]

        for loc in validLocations:
            # Set peice to a valid location
            self.next_piece.x = loc[0]
            self.next_piece.y = loc[1]

            for _ in range(3): # loop through all rotations

                formatted_shape = Tetris.convert_shape_format(self.next_piece)

                if Tetris.check_lost(formatted_shape): # If out of bounds rotate and go next
                    self.next_piece.rotation += 1
                    continue

                for pos in formatted_shape: # For each block check if its spot is open else rotate and go next
                    if pos not in accepted_pos:
                        if pos[1] >= 0:
                            self.next_piece.rotation += 1
                            continue
                # Add piece to board and add it to solution
                tempBoard = self.initial_board
                for pos in formatted_shape:
                    tempBoard[pos[0]] = 1
                    tempBoard[pos[1]] = 1
                if tempBoard not in perms:
                    perms.append(tempBoard)
                self.next_piece.rotation += 1
        
        return perms