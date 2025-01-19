import random
import numpy as np
import pygame
import Move_Recommender as Move_Rec
from Permutation_Generator import generate_permutations
from shared_imports import Piece, I, T, shapes, convert_shape_format, xy_rel_to_blocks

"""
10 x 20 grid
play_height = 2 * play_width

tetriminos:
    0 - S - green
    1 - Z - red
    2 - I - cyan
    3 - O - yellow
    4 - J - blue
    5 - L - orange
    6 - T - purple
"""

pygame.font.init()

# global variables

col = 10  # 10 columns
row = 20  # 20 rows
s_width = 800  # window width
s_height = 750  # window height
play_width = 300  # play window width; 300/10 = 30 width per block
play_height = 600  # play window height; 600/20 = 20 height per block
block_size = 30  # size of block

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

filepath = './Resources/highscore.txt'
fontpath = 'Resources/Hubot_Sans/static/HubotSans-Medium.ttf'
# fontpath_mario = './Resources/mario.ttf'

# dummy values for now


def drop_shadow_text(screen, text, size, x, y, colour=(255, 255, 255), drop_colour=(128, 128, 128), font=None):
    # how much 'shadow distance' is best?
    dropshadow_offset = 1 + (size // 15)
    text_font = pygame.font.Font(font, size)
    # make the drop-shadow
    text_bitmap = text_font.render(text, True, drop_colour)
    screen.blit(text_bitmap, (x+dropshadow_offset, y+dropshadow_offset))
    # make the overlay text
    text_bitmap = text_font.render(text, True, colour)
    screen.blit(text_bitmap, (x, y))

# initialise the grid
def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(col)]
            for y in range(row)]  # grid represented rgb tuples

    # locked_positions dictionary
    # (x,y):(r,g,b)
    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                color = locked_pos[
                    (x, y)]  # get the value color (r,g,b) from the locked_positions dictionary using key (x,y)
                grid[y][x] = color  # set grid position to color

    return grid


# checks if current position of piece in grid is valid
def valid_space(piece, grid):
    # makes a 2D list of all the possible (x,y)
    accepted_pos = [[(x, y) for x in range(col) if grid[y]
                     [x] == (0, 0, 0)] for y in range(row)]
    # removes sub lists and puts (x,y) in one list; easier to search
    accepted_pos = [x for item in accepted_pos for x in item]

    formatted_shape = convert_shape_format(piece)
    
    for pos in formatted_shape:
        if pos not in accepted_pos:
            if pos[1] >= 0:
                return False
    return True


# check if piece is out of board
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# chooses a shape randomly from shapes list
def get_shape():
    return Piece(5, 0, random.choice(shapes))


# draws text in the middle
def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(fontpath, size)
    font.italic = True
    font.bold = False
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2),
                 top_left_y + play_height/2 - (label.get_height()/2)))


# draws the lines of the grid for the game
def draw_grid(surface):
    r = g = b = 0
    grid_color = (r, g, b)

    for i in range(row):
        # draw grey horizontal lines
        pygame.draw.line(surface, grid_color, (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))
        for j in range(col):
            # draw grey vertical lines
            pygame.draw.line(surface, grid_color, (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))


# clear a row when it is filled
def clear_rows(grid, locked):
    # need to check if row is clear then shift every other row above down one
    increment = 0
    for i in range(len(grid) - 1, -1, -1):      # start checking the grid backwards
        grid_row = grid[i]                      # get the last row
        if (0, 0, 0) not in grid_row:           # if there are no empty spaces (i.e. black blocks)
            increment += 1
            # add positions to remove from locked
            index = i                           # row index will be constant
            for j in range(len(grid_row)):
                try:
                    # delete every locked element in the bottom row
                    del locked[(j, i)]
                except ValueError:
                    continue

    # shift every row one step down
    # delete filled bottom row
    # add another empty row on the top
    # move down one step
    if increment > 0:
        # sort the locked list according to y value in (x,y) and then reverse
        # reversed because otherwise the ones on the top will overwrite the lower ones
        for key in sorted(list(locked), key=lambda a: a[1])[::-1]:
            x, y = key
            if y < index:                       # if the y value is above the removed index
                new_key = (x, y + increment)    # shift position to down
                locked[new_key] = locked.pop(key)

    return increment


# draws the upcoming piece
def draw_next_shape(piece, surface):
    font = pygame.font.Font(fontpath, 30)
    label = font.render('Next shape', 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                block_x = start_x + j * block_size
                block_y = start_y + i * block_size
                lighter_colour = tuple(min(x+25, 255) for x in piece.color)
                darker_colour = tuple(max(x-25, 0) for x in piece.color)
                dip = block_size//6

                pygame.draw.rect(surface, piece.color, (start_x + j*block_size,
                                 start_y + i*block_size, block_size, block_size), 0)

                pygame.draw.polygon(surface, lighter_colour, [
                    (block_x, block_y),
                    (block_x + block_size, block_y),
                    (block_x + block_size - dip, block_y + dip),
                    (block_x + dip, block_y + dip),
                    (block_x + dip, block_y + block_size - dip),
                    (block_x, block_y + block_size)
                ]),

                pygame.draw.polygon(surface, darker_colour, [
                    (block_x + block_size, block_y + block_size),
                    (block_x, block_y + block_size),
                    (block_x + dip, block_y + block_size - dip),
                    (block_x + block_size - dip, block_y + block_size - dip),
                    (block_x + block_size - dip, block_y + dip),
                    (block_x + block_size, block_y)
                ])


    surface.blit(label, (start_x, start_y - 30))

    # pygame.display.update()

# draws the content of the window
def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))  # fill the surface with black

    pygame.font.init()  # initialise font
    font = pygame.font.Font(fontpath, 65)
    font.bold = True
    # initialise 'Tetris' text with white (this is only used for the width of the text)
    label = font.render('TETRIS', 1, (255, 255, 255))

    # draw the text with drop shadow
    drop_shadow_text(surface, 'TETRIS', 65, (top_left_x +
                   play_width / 2) - (label.get_width() / 2), 20, (255, 255, 255), (128, 128, 128), fontpath)

    # current score
    font = pygame.font.Font(fontpath, 25)
    label = font.render('SCORE   ' + str(score), 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    surface.blit(label, (start_x, start_y + 200))

    # last score
    label_hi = font.render(
        'HIGHSCORE', 1, (255, 255, 255))
    label_hi_score = font.render(
        str(last_score), 1, (255, 255, 255))

    start_x_hi = top_left_x - 210
    start_y_hi = top_left_y + 400

    surface.blit(label_hi, (start_x_hi, start_y_hi))
    surface.blit(label_hi_score, (start_x_hi, start_y_hi + 30))

    # draw content of the grid
    for i in range(row):
        for j in range(col):
            # pygame.draw.rect()
            # draw a rectangle shape
            # rect(Surface, color, Rect, width=0) -> Rect
            block_x = top_left_x + j * block_size
            block_y = top_left_y + i * block_size
            dip = block_size//6
            colour = grid[i][j]
            lighter_colour = tuple(min(x+25, 255) for x in colour)
            darker_colour = tuple(max(x-25, 0) for x in colour)

            pygame.draw.rect(surface, colour,
                             (block_x, block_y, block_size, block_size), 0)

            if (colour != (0, 0, 0)):
                pygame.draw.polygon(surface, lighter_colour, [
                    (block_x, block_y),
                    (block_x + block_size, block_y),
                    (block_x + block_size - dip, block_y + dip),
                    (block_x + dip, block_y + dip),
                    (block_x + dip, block_y + block_size - dip),
                    (block_x, block_y + block_size)
                ]),

                pygame.draw.polygon(surface, darker_colour, [
                    (block_x + block_size, block_y + block_size),
                    (block_x, block_y + block_size),
                    (block_x + dip, block_y + block_size - dip),
                    (block_x + block_size - dip, block_y + block_size - dip),
                    (block_x + block_size - dip, block_y + dip),
                    (block_x + block_size, block_y)
                ])

    # draw vertical and horizontal grid lines
    draw_grid(surface)

    # draw rectangular border around play area
    border_color = (255, 255, 255)
    pygame.draw.rect(surface, border_color, (top_left_x,
                     top_left_y, play_width, play_height), 4)

    # pygame.display.update()


def draw_rec_numbers(surface, confidence, numbers):

    rankFont = pygame.font.Font(fontpath, 20)
    confFont = pygame.font.Font(fontpath, 12)

    for i in range(len(numbers)):
        rank = rankFont.render(str(i + 1), 1, (255, 255, 255))
        conf = confFont.render(str(confidence[i]), 1, (255, 255, 255))
        surface.blit(
            rank, ((top_left_x + numbers[i][0] * block_size) + 10, top_left_y + numbers[i][1] * block_size - 9))
        surface.blit(
            conf, ((top_left_x + numbers[i][0] * block_size) + 8, top_left_y + numbers[i][1] * block_size + 15))

# update the score txt file with high score
def update_score(new_score):
    score = get_max_score()

    with open(filepath, 'w') as file:
        if new_score > score:
            file.write(str(new_score))
        else:
            file.write(str(score))


# get the high score from the file
def get_max_score():
    with open(filepath, 'r') as file:
        lines = file.readlines()        # reads all the lines and puts in a list
        score = int(lines[0].strip())   # remove \n

    return score


def clean_grid_from_locked(locked_pos={}):
    grid = [[0 for x in range(col)]
            for y in range(row)]  # grid represented rgb tuples

    # locked_positions dictionary
    # (x,y):(r,g,b)
    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                grid[y][x] = 1

    return grid

def main(window):
    locked_positions = {}
    create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0
    last_score = get_max_score()

    recommended_moves = []

    while run:
        # need to constantly make new grid as locked positions always change
        grid = create_grid(locked_positions)

        # helps run the same on every computer
        # add time since last tick() to fall_time
        fall_time += clock.get_rawtime()  # returns in milliseconds
        level_time += clock.get_rawtime()

        clock.tick()  # updates clock

        if level_time/1000 > 5:    # make the difficulty harder every 10 seconds
            level_time = 0
            if fall_speed > 0.15:   # until fall speed is 0.15
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                # since only checking for down - either reached bottom or hit another piece
                # need to lock the piece position
                # need to generate new piece
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1  # move x position left
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1  # move x position right
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + \
                        1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - \
                            1 % len(current_piece.shape)
                        
                elif event.key == pygame.K_1 and len(recommended_moves) > 0:
                    current_piece.x = recommended_moves[0][1].x
                    current_piece.y = recommended_moves[0][1].y
                    current_piece.rotation = recommended_moves[0][1].rotation

                elif event.key == pygame.K_2 and len(recommended_moves) > 1:
                    current_piece.x = recommended_moves[1][1].x
                    current_piece.y = recommended_moves[1][1].y
                    current_piece.rotation = recommended_moves[1][1].rotation

                elif event.key == pygame.K_3 and len(recommended_moves) > 2:
                    current_piece.x = recommended_moves[2][1].x
                    current_piece.y = recommended_moves[2][1].y
                    current_piece.rotation = recommended_moves[1][1].rotation

        piece_pos = convert_shape_format(current_piece)

        # draw the piece on the grid by giving color in the piece locations
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color

        rec_nums = []

        for piece_and_conf in recommended_moves:
            (board, piece, confidence) = piece_and_conf

            rec_piece_pos = convert_shape_format(piece)
            rec_piece_pos = [(y, x) for x, y in rec_piece_pos]

            max_x = 0
            min_x = 10
            max_y = 0
            min_y = 20

            for i in range(len(rec_piece_pos)):
                x, y = rec_piece_pos[i]
                print(f"size of the grid: ({ len(grid) }, { len(grid[0]) }), x: { x }, y: { y }")
                if y >= 0:
                    grid[x][y] = (40, 40, 40)

                max_x = max(max_x, x)
                min_x = min(min_x, x)
                max_y = max(max_y, y)
                min_y = min(min_y, y)

            rec_nums.append((min_x + (max_x - min_x)/2,
                            min_y + (max_y - min_y)/2))

        if change_piece:  # if the piece is locked
            for pos in piece_pos:
                p = (pos[0], pos[1])
                # add the key and value in the dictionary
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # increment score by 10 for every row cleared
            score += clear_rows(grid, locked_positions) * 10
            update_score(score)

            if last_score < score:
                last_score = score

            # HERES WHERE THE BOARD STATE IS OUTPUTTED
            # Use clean_grid_from_locked(locked_positions) for the board
            # and next_piece for the next piece
            # print("\n".join(
            #     [" ".join([str(j) for j in i])
            #      for i in clean_grid_from_locked(locked_positions)]
            # ))

            recommended_moves = Move_Rec.Move_Recommender(
                clean_grid_from_locked(locked_positions), current_piece).recommend_move()
            
            # print(recommended_moves)

        draw_window(window, grid, score, last_score)
        draw_next_shape(next_piece, window)
        draw_rec_numbers(window, recommended_moves, rec_nums)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle('You Lost', 40, (255, 255, 255), window)
    pygame.display.update()
    pygame.time.delay(2000)  # wait for 2 seconds
    pygame.quit()


def main_menu(window):
    run = True
    while run:
        draw_text_middle('Press any key to begin', 50, (255, 255, 255), window)
        pygame.display.update()

        for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #     run = False
            # elif event.type == pygame.KEYDOWN:
                main(window)

    pygame.quit()


if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')

    main_menu(win)  # start game
