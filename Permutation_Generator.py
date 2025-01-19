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
    print("Pre-moved piece: ", piece.x, piece.y)

    # surface_positions = [((2,3), True), (1,4, False), (7,8, True)]

    edges = Edge_Tracer.Edge_Tracer(board).generate_path()

    # Remove bools + edges not touching on bottom (We love one-liners!!!)
    potential_positions = [(edge[0][0], edge[0][1]) for edge in edges if edge[1]]

    valid_placements = [] # elements will be of form (board, piece)
    for test_pos in potential_positions: #try all resting potential_positions 
        for rotation in range(len(piece.shape)): #try all rotations of piece
            
            piece.rotation = rotation
            indiv_blocks = convert_shape_format(piece)
            indiv_blocks = [(i[1], i[0]) for i in indiv_blocks] # Convert to our x,y format

            for indiv_block_pos in indiv_blocks: #try putting each indiv_block_pos of the piece in the position
                # print(f"Testing cond: rotation = {rotation}, position = {test_pos}, indiv_block_pos = {indiv_block_pos}")
                origin = test_pos
                indiv_blocks_relative_pos = [(rev_block_pos[0] - indiv_block_pos[0], rev_block_pos[1] - indiv_block_pos[1]) for rev_block_pos in indiv_blocks] # relative position of each indiv_block_pos in piece
                indiv_blocks_abs_pos = [(origin[0] + rel_block_pos[0], origin[1] + rel_block_pos[1]) for rel_block_pos in indiv_blocks_relative_pos] # absolute position of each indiv_block_pos in board

                valid = False
                for block_pos in indiv_blocks_abs_pos: # checks that at least one block is touching on the bottom
                    if block_pos[0] == 19:
                        valid = True
                        break
                    elif block_pos[0] < 19 and board[block_pos[0] + 1][block_pos[1]] == 1:
                        valid = True
                        break

                for block_pos in indiv_blocks_abs_pos: #check that each other indiv_block_pos is in a valid position
                    #print("Block position:", block_pos)
                    if not ((0 <= block_pos[1] < 10) and (0 <= block_pos[0] < 20)): #out of bounds
                        #print("piece out of bounds")
                        valid = False
                        break
                    if board[block_pos[0]][block_pos[1]] == 1: #occupied
                        #print("space was occupied")
                        valid = False
                        break

                #print("indiv_block_pos is valid: ", valid)
                if valid:
                    print(blocks_absolute)
                    new_board = np.zeros(board.shape)
                    for test_pos in blocks_absolute:
                        new_board[test_pos[0]][test_pos[1]] = 1
                    # for i in range(20):
                    #     column = []
                    #     for j in range(10):
                    #         if board[i][j] == 1 or [i,j] in blocks_absolute:
                    #             column.append(1)
                    #         else:
                    #             column.append(0)
                    #     new_board.append(column)
                    valid_placements.append((new_board + board, Piece(x, y, piece.shape)))
    
    return valid_placements

# test_piece = Piece(0,0,T)

# perms = generate_permutations(test_piece, sample_board)

# print("perms length: ", len(perms))
# print(perms[0])
# print(perms[40])

