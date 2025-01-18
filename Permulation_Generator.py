import numpy as np

class Permutation_Generator:
    def __init__(self, initial_board):
        self.initial_board = initial_board # 10 x 20 np array

    def generate(self, initial_board):
        perms = [0,0,0,0,0,0]
        return perms