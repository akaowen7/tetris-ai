# shapes formats

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# index represents the shape
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(27, 224, 27), (237, 38, 38), (33, 217, 217),
                (230, 230, 37), (235, 186, 28), (34, 78, 224), (150, 14, 132)]

# class to represent each of the pieces
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        # choose color from the shape_color list
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # chooses the rotation according to index

    def __str__(self):
      return f"Piece at {self.x}, {self.y} with rotation {self.rotation} and shape {self.shape[self.rotation]} and color {self.color}"


def convert_shape_format(piece):
    positions = []
    # get the desired rotated shape from piece
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    '''
    e.g.
       ['.....',
        '.....',
        '..00.',
        '.00..',
        '.....']
    '''
    for i, line in enumerate(shape_format):  # i gives index; line gives string
        row = list(line)  # makes a list of char from string
        # j gives index of char; column gives char
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    #print(f"abs(?) Positions: { positions }, raw position: { piece.x, piece.y }, shape: { shape_format }")

    for i, pos in enumerate(positions):
        # offset according to the input given with dot and zero
        positions[i] = (pos[0] - 2, pos[1] - 4)

    #print(f"Final Positions: { positions }")

    return positions

def xy_rel_to_blocks(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(shape_format):  # i gives index; line gives string
        row = list(line)  # makes a list of char from string
        # j gives index of char; column gives char
        for j, column in enumerate(row):
            if column == '0':
                #positions.append((j - 2, i - 4))
                positions.append((2 - j, 4 - i))

    return positions