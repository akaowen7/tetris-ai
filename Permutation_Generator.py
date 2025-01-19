from shared_imports import Piece, convert_shape_format, T, xy_rel_to_blocks
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
    #print("Pre-moved piece: ", piece.x, piece.y)

    # surface_positions = [((2,3), True), (1,4, False), (7,8, True)]

    edges = Edge_Tracer.Edge_Tracer(board).generate_path()

    # Remove bools + edges not touching on bottom (We love one-liners!!!)
    potential_positions = [(edge[0][0], edge[0][1]) for edge in edges if edge[1]]

    valid_placements = [] # elements will be of form (board, piece)
    simple_valid_placements = [] # simpler data structure for checking duplicates, elements will be of form (x, y, rotation)

    for test_pos in potential_positions: #try all resting potential_positions 
        for rotation in range(len(piece.shape)): #try all rotations of piece
            
            piece.rotation = rotation
            xy_positions = xy_rel_to_blocks(piece) #all the xy positions corresponding to one of the blocks being in test_pos
            for xy in xy_positions: #try putting xy in each position
                piece.x = test_pos[1] + xy[0]
                piece.y = test_pos[0] + xy[1]
                if (piece.x, piece.y, rotation) in simple_valid_placements:
                    continue
                blocks_abs = convert_shape_format(piece) #computationally inefficient but more readable I hope
                blocks_abs = [(i[1], i[0]) for i in blocks_abs] # Convert to our x,y format

                #origin = test_pos
                #indiv_blocks_relative_pos = [(rev_block_pos[0] - indiv_block_pos[0], rev_block_pos[1] - indiv_block_pos[1]) for rev_block_pos in indiv_blocks] # relative position of each indiv_block_pos in piece
                #indiv_blocks_abs_pos = [(origin[0] + rel_block_pos[0], origin[1] + rel_block_pos[1]) for rel_block_pos in indiv_blocks_relative_pos] # absolute position of each indiv_block_pos in board

                valid = True
                # for block_pos in indiv_blocks_abs_pos: # checks that at least one block is touching on the bottom
                #     if block_pos[0] == 19:
                #         valid = True
                #         break
                #     elif block_pos[0] < 19 and board[block_pos[0] + 1][block_pos[1]] == 1:
                #         valid = True
                #         break

                for block_abs in blocks_abs: #check that each block is in a valid position
                    #print("Block position:", block_pos)
                    if not ((0 <= block_abs[1] < 10) and (0 <= block_abs[0] < 20)): #out of bounds
                        #print("piece out of bounds")
                        valid = False
                        break
                    if board[block_abs[0]][block_abs[1]] == 1: #occupied
                        #print("space was occupied")
                        valid = False
                        break

                #print("indiv_block_pos is valid: ", valid)
                if valid:
                    #print(blocks_abs)
                    new_board = np.zeros(board.shape)
                    display_board = np.zeros(board.shape)
                    for block_abs in blocks_abs:
                        new_board[block_abs[0]][block_abs[1]] = 1
                        display_board[block_abs[0]][block_abs[1]] = 2
                    # for i in range(20):
                    #     column = []
                    #     for j in range(10):
                    #         if board[i][j] == 1 or [i,j] in blocks_absolute:
                    #             column.append(1)
                    #         else:
                    #             column.append(0)
                    #     new_board.append(column)
                    rec_piece = Piece(piece.x, piece.y, piece.shape)
                    rec_piece.rotation = piece.rotation
                    
                    valid_placements.append((new_board + board, rec_piece))
                    simple_valid_placements.append((piece.x, piece.y, rotation))
    
    return valid_placements

