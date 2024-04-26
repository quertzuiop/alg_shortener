import numpy as np
import timeit
import cProfile
import json
"""
Cube state format:
[
    [[0, 0], [1, 0]],
    [[2, 0], [3, 0]],
],
[
    [[4, 0], [5, 0]],
    [[6, 0], [7, 0]],
],
z: 0
y: 1
x: 2
first is cubie index, second is rotation
"""
moveaxis = {
    "U": 0,
    "F": 1,
    "R": 2,
}
movemap = {
    "R ": (2, 1),
    "R'": (2, -1),
    "R2": (2, 2),
    "U ": (0, 1),
    "U'": (0, -1),
    "U2": (0, 2),
    "F ": (1, -1),
    "F'": (1, 1),
    "F2": (1, 2),
}
move_invert_map = {
    " ": "'",
    "'": " ",
    "2": "2",
}
default_state = np.array([
    [
        [[0, 0], [1, 0]],
        [[3, 0], [2, 0]],
    ],[
        [[4, 0], [5, 0]],
        [[7, 0], [6, 0]],
    ]
])

class Alg:
    def __init__(self, moves=None, randomize=False, l=None):
        if randomize:
            moves = np.array([["R", "U", "F"][np.random.randint(0, 3)] + np.random.choice([" ", "'", "2"]) for _ in range(l)])
        self.moves = moves
        
    def invert(self):
        inverted = [move_invert_map[move[1]] for move in self.moves[::-1]]
        self.moves = inverted
        return inverted


class Cube_2x2:
    def __init__(self, inital_state=default_state):
        self.state = inital_state.copy()

    def reset(self):
        self.state = default_state.copy()
    
    def set_state(self, state):
        self.state = state.copy()

    def rotate(self, axis, amount):
        stationary_half, moving_half = np.split(self.state, 2, axis)
        perpendicular_axes = [0, 1, 2]
        perpendicular_axes.pop(axis)
        if axis != 0:
            moving_half[0][0][0][1] = (moving_half[0][0][0][1] + (3-axis)) % 3
            moving_half[0][axis-1][2-axis][1]   = (moving_half[0][axis-1][2-axis][1] + axis) % 3
            moving_half[1][0][0][1]             = (moving_half[1][0][0][1] + axis) % 3
            moving_half[1][axis-1][2-axis][1]   = (moving_half[1][axis - 1][2 - axis][1] + (3 - axis)) % 3
        moving_half = np.rot90(moving_half, -amount, perpendicular_axes)
        self.state = np.concatenate((stationary_half, moving_half), axis)
        #print(self.state)
    
    def notation_rotate(self, move):
        axis, amount = movemap[move]
        self.rotate(axis, amount)

class Base9Num:
    def __init__(self, num):
        self.num = num
        self.digits = []
        self.__update(num)
    
    def __str__(self):
        return "".join([str(digit) for digit in self.digits])
    
    def __int__(self):
        return self.num
    
    def __update(self, num):
        self.digits = []
        while num > 0:
            self.digits.append(num % 9)
            num //= 9
    
    def increment(self):
        self.num += 1
        self.__update(self.num)

if __name__ == "__main__":
    cube = Cube_2x2()
    cube_states = {"0": [[default_state.tolist(), []]]}
    moves = movemap.keys()
    current_moves = Base9Num(0)
    for alglen in range(1, 8):
        states = []
        for state, alg in cube_states[str(alglen-1)]:
            for move in moves:
                try:
                    if move[0] != alg[-1][0]:
                        cube.set_state(np.array(state))
                        cube.notation_rotate(move)
                        states.append([cube.state.tolist(), alg+[move]])
                except:
                    cube.set_state(np.array(state)) 
                    cube.notation_rotate(move)
                    states.append([cube.state.tolist(), alg+[move]])
        cube_states[str(alglen)] = states
    with open("cube_states.json", "w") as f:
        json.dump(cube_states, f)
    
    #print(timeit.timeit(lambda: cube.rotate(0, 1), number=1000000))
    #def test():
    #    for i in range(4):
    #        cube.rotate(2, 1)
    #        #alg1.inverted()
    #test()
    #cProfile.run("test()", sort="cumtime")