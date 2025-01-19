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
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 0], 
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0], 
    [1, 0, 0, 1, 0, 1, 1, 1, 1, 0], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0]])

class Tracer_Object:
    # direction = (direction, check_location, next_direction, opposite_direction)
    directions = {
        "up": [(0, -1), "left", "down"],
        "down": [(0, 1), "right", "up"],
        "left": [(1, 0), "down", "right"],
        "right": [(-1, 0), "up", "left"]
    }

    previous_direction = directions["down"]

    def __init__(self, position: tuple):
        self.position = position

    def check_location(self):
        return self.previous_direction[0]
    
    def next_direction(self):
        self.previous_direction = self.directions[self.previous_direction[1]]

    def update_direction(self, new_direction: str):
        self.previous_direction = self.directions[new_direction]

    def update_position(self, new_position: tuple):
        self.position = new_position

class Edge_Tracer:
    """Returns tuple (position (x,y), has_block_below (bool))"""
    def __init__(self, board: np.array):
        self.board = board

    def find_start_point(self):
        currentPos = (0, 0)
        while self.board[currentPos[0] + 1, currentPos[1]] == 0:
            currentPos = (currentPos[0] + 1, currentPos[1])

        return currentPos
    
    def generate_path(self):
        tracer = Tracer_Object(self.find_start_point())
        path = {(tracer.position, True)}

        while tracer.position[1] + 1 != self.board.shape[1]:
            #print(f"Current position: { tracer.position }, Previous direction: { tracer.previous_direction }, check_location: { tracer.check_location() }")
            neighborPos = (tracer.position[0] + tracer.check_location()[0], tracer.position[1] + tracer.check_location()[1])
            neighbor = self.board[neighborPos[0], neighborPos[1]]

            if neighbor == 0:
                #print(f"Adding position to list: { neighborPos }")
                path.add((neighborPos, self.board[neighborPos[0] + 1, neighborPos[1]] == 1))

                if neighborPos[0] == tracer.position[0] + 1:
                    tracer.update_direction("up")
                elif neighborPos[0] == tracer.position[0] - 1:
                    tracer.update_direction("down")
                elif neighborPos[1] == tracer.position[1] + 1:
                    tracer.update_direction("left")
                else:
                    tracer.update_direction("right")
                
                tracer.update_position(neighborPos)
            else:
                tracer.next_direction()
        
        while self.board[tracer.position[0] + 1][tracer.position[1]] == 0:
            newPos = (tracer.position[0] + 1, tracer.position[1])
            path.add((newPos, self.board[newPos[0] + 1, newPos[1]] == 1))
            tracer.update_position(newPos)
        
        return path
    
# traceObj = Edge_Tracer(sample_board)

# edges = traceObj.generate_path()
# print(edges)

# zero_array = np.zeros(sample_board.shape)
# for edge in edges:
#     zero_array[edge[0][0], edge[0][1]] = 1
# print(zero_array)