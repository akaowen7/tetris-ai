from shared_imports import Piece, convert_shape_format, T
import Edge_Tracer
import numpy as np

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

def generate_permutations(input_piece, board):
    piece = Piece(input_piece.x, input_piece.y, input_piece.shape) # don't mess with the actual game piece

    # surface_positions = [((2,3), True), (1,4, False), (7,8, True)]

    edges = Edge_Tracer.Edge_Tracer(board).generate_path()
    print(edges)




    positions = filter(lambda x : x[1], edges)

    valid_placements = [] # elements will be of form (board, piece)

    for rotation in range(3): #try all rotations of piece
        piece.rotation = rotation
        blocks = convert_shape_format(piece)
        for pos in positions: #try all resting positions
            for block in blocks: #try putting each block of the piece in the position
                valid = True
                x = pos[0][0] - block[0]
                y = pos[0][1] - block[1]
                blocks_absolute = map(lambda other_block: [x + other_block[0], y + other_block[1]], blocks) # absolute position of each block in board
                for other_block in blocks_absolute: #check that each other block is in a valid position
                    if not ((0 <= other_block[0] < 10) and (0 <= other_block[1] < 20)): #out of bounds
                        valid = False
                        break
                    if board[other_block[0]][other_block[1]] == 1: #occupied
                        valid = False
                        break
                print(valid)
                if valid:
                    new_board = np.zeros(board.shape)
                    for pos in blocks_absolute:
                        new_board[pos[0]][pos[1]] = 1

                    print(new_board)
                    # for i in range(20):
                    #     column = []
                    #     for j in range(10):
                    #         if board[i][j] == 1 or [i,j] in blocks_absolute:
                    #             column.append(1)
                    #         else:
                    #             column.append(0)
                    #     new_board.append(column)
                    valid_placements.append((board, Piece(x, y, piece.shape)))
    
    return valid_placements

test_piece = Piece(0,0,T)

perms = generate_permutations(test_piece, sample_board)

print("perms length: ", len(perms))
print(perms[0])
print(perms[1])

