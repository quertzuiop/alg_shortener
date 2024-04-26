import json

long_solution = "R' F' R  U  R' R  F  U  F' U' R' U' F  R  U' F  R2 F' U  R  U2 R' F' "
print(len(long_solution)//3, long_solution)

algdict = json.load(open("algdict.json"))

def sort_improvements(possible_improvements):
    return sorted(possible_improvements, key=lambda x: len(x[1])-len(x[0]))
while True:
    possible_improvements = []
    for start in range(0, len(long_solution), 3):
        for end in range(start+3, min(len(long_solution), start+21), 3):
            #print(long_solution[start:end-1][-1], long_solution[start:end-1])
            try:
                print(f"[{long_solution[start:end-1]}], {algdict[long_solution[start:end-1]]}")
                if algdict[long_solution[start:end-1]]:
                    solution = algdict[long_solution[start:end-1]]
                    solution+=" "
                    if solution == " ": solution = ""
                    possible_improvements.append([long_solution[start:end-1]+" ", solution])
            except:
                pass

    
    possible_improvements = sort_improvements(possible_improvements)

    try: long_solution = long_solution.replace(possible_improvements[0][0], possible_improvements[0][1])
    except: break
    print(len(long_solution)//3, long_solution)
