from time import perf_counter
import sys

filename = sys.argv[1]
with open(filename) as f: # read in boards
    line_list = []
    for line in f:
        line = line.strip()
        line_list.append(line)

def find_subblocks(size):
    for x in range(int(size/2)-1, 0, -1):
        if size%x==0:
            if int(size/x)>x:
                return((x, int(size/x)))
            return((int(size/x), x))

def display_board(board, size):
    display = "________________________________________________________________________"
    display = display[:size*2+2] + "\n"
    for x in range(size):
        display = display + "| " + " ".join(board[x*size:x*size+size]) + " |" + "\n"
    display = display + display[:size*2+2] + "\n"
    print(display)

def find_instances(board):
    instances = []
    for symbol in symbol_set:
        count = 0
        for x in range(len(board)):
            if board[x]==symbol:
                count +=1
        instances.append((symbol, count))
    return instances

def goal_test(state):
    for row in state:
        if len(row)>1:
            return False
    return True

def get_next_unassigned_var(state): # get most contrained var
    max = [100, 0]
    for x in range(len(state)):
        if len(state[x]) < max[0] and len(state[x])>1:
            max[0] = len(state[x])
            max[1] = x
    return max[1]

# def get_sorted_values(state, var, neighbor_sets):
#     poss = symbol_set.copy()
#     # returns list of possible symbols that could go in that space
#     for value in neighbor_sets[var]:
#         if state[value] in poss:
#             poss.remove(state[value])
#     return poss

def constraint_propagation(state):
    changes = []
    for constraint_set in constraintlist:
            for symbol in symbol_set:
                count = [0]
                for value in constraint_set:
                    if symbol in state[value]:
                        count[0] += 1
                        count.append((symbol, value))
                if count[0]==1:
                    if len(state[count[1][1]])!=1:
                        state[count[1][1]]=str(count[1][0])
                        changes.append(count[1][1])
                if count[0]==0:
                    return None
    if len(changes)!=0:
        return forward_looking(state, changes)
    return state

def forward_looking(state, solved):
    while solved: # loop over all indices in that index’s set of neighbors; remove value at solved index from each
        curr = solved.pop()
        for neighbor in neighbor_sets[curr]:
            if state[curr] in state[neighbor]:
                state[neighbor] = state[neighbor].replace(state[curr], "")
                if len(state[neighbor])==0: # index becomes empty, then a bad choice has been made
                    return None
                if len(state[neighbor])==1: # any of these becomes solved, add them to the list of solved indices.
                    solved.append(neighbor)
    # do constraint propagation
    result = constraint_propagation(state)
    return result

def backtracking(state, neighbor_sets):
    if goal_test(state): 
        return state
    var = get_next_unassigned_var(state) # pick first space
    for val in state[var]: # list of symbols that could go in space
        new_state = state.copy()
        new_state[var] = val
        checked_board = forward_looking(new_state, [var])
        if checked_board is not None:
            # checked_board = constraint_propagation(checked_board)
            # if checked_board is not None:
                result = backtracking(checked_board, neighbor_sets)
                if result is not None:
                    return result
    return None

characterposs = "123456789ABCDEFGHIJKLNMOPQRSTUVWXYZ"
start = perf_counter()
for line in line_list:
    neighbor_sets = []
    size, constraintlist, board = int(len(line)**0.5), [], []
    symbol_set = set(characterposs[:size])
    # make board
    for x in range(len(line)):
        vals = ""
        if line[x] == ".":
            for thing in symbol_set:
                vals = vals + thing
            board.append(vals)
        else:
            board.append(line[x])
    # find subblock width and height
    if int(int((size**0.5))**2) == size: 
        subblock_height, subblock_width = int(size**0.5), int(size**0.5)
    else:
        subblock_height, subblock_width = find_subblocks(size)
    # make list of constraint sets
    for x in range(size): # row
        currset = set(range(x*size, x*size+size))
        constraintlist.append(currset)
    for x in range(size): # column
        currset = set(x+y*size for y in range(size))
        constraintlist.append(currset)
    for row in range(subblock_width): # block
        for col in range(subblock_height):
            currset = set()
            for a in range(subblock_height):
                for b in range(row*size*subblock_height+(subblock_width*col), row*size*subblock_height+(subblock_width*col)+subblock_width):
                    currset.add(b+(a*size))
            constraintlist.append(currset)
    # make neighbor sets
    for index in range(size**2):
        neighborset = set()
        for x in constraintlist:
            if index in x:
                for v in x:
                    neighborset.add(v)
        neighborset.remove(index)
        neighbor_sets.append(neighborset)
    # make list of solved indices
    solved = []
    for index in range(len(board)):
        if len(board[index])==1:
            solved.append(index)
    solution = backtracking(forward_looking(board, solved), neighbor_sets)
    display_board(solution, size)
    print(str("".join(solution)))
end = perf_counter()
print("time: " + str(end-start))
# python sudoku_part_two.py puzzles_1_standard_easy.txt
# python sudoku_part_two.py puzzles_2_variety_easy.txt