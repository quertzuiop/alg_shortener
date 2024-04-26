import json

from cube import Alg
from cube import default_state
from cube import movemap
from cube import move_invert_map
from cube import moveaxis

#test scramble: U' F U' R2 U F R2 U F'
#R' F' R  U  R' R  F  U  F' U' R' U' F  R  U' F  R2 F' U  R  U2 R' F'

print(0)
states = json.load(open("cube_states.json"))
print(1)
simple = {
    "R  R'": "",
    "R' R ": "",
    "U  U'": "",
    "U' U ": "",
    "U2 U2": "",
    "F  F'": "",
    "F' F ": "",
    "U  U ": "U2",
    "U  U2": "U'",
    "U' U'": "U2",
    "U' U2": "U ",
    "U2 U ": "U'",
    "U2 U'": "U ",
    "R  R ": "R2",
    "R  R2": "R'",
    "R' R'": "R2",
    "R' R2": "R ",
    "R2 R ": "R'",
    "R2 R'": "R ",
    "F  F ": "F2",
    "F  F2": "F'",
    "F' F'": "F2",
    "F' F2": "F ",
    "F2 F ": "F'",
    "F2 F'": "F ", 
}
algdict = {}
for long_state_len in reversed(states.keys()):
    for short_state_len in range(int(long_state_len)):
        print(short_state_len)
        for long_state, long_alg in states[long_state_len]:
            for short_state, short_alg in states[str(short_state_len)]:
                if long_state == short_state:
                    algdict[" ".join(long_alg)] = " ".join(short_alg)

with open("algdict.json", "w") as f:
    json.dump(algdict, f)