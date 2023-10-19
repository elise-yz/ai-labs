import sys
def game_over(board):
    wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    if board.count(".") == 0:
        return (True, 0)
    for x in range(len(wins)):
        count = 0
        for space in wins[x]:
            if board[space]=="X":
                count +=1
            if board[space]=="O":
                count += -1
        if count==3:
            return (True, 1)
        if count==-3:
            return (True, 2)
    return (False, 0)

def display_board(board):
    return board[:3] + "\n" + board[3:6] + "\n" + board[6:]

def possible_next_boards(board, player):
    poss = []
    for x in range(len(board)):
        if board[x]==".":
            poss.append(board[:x]+player+board[x+1:])
    return poss

def possible_next_spaces(board, player):
    poss = []
    for x in range(len(board)):
        if board[x]==".":
            poss.append((x, board[:x]+player+board[x+1:]))
    return poss

def min_step(board):
    end, score = game_over(board)
    if end == True:
        if score==2:
            return -1
        elif score==1:
            return 1
        return 0
    results = []
    for next_board in possible_next_boards(board, "O"):
        results.append(max_step(next_board))
    return min(results)

def max_step(board):
    end, score = game_over(board)
    if end == True:
        if score==2:
            return -1
        elif score==1:
            return 1
        return 0
    results = []
    for next_board in possible_next_boards(board, "X"):
        results.append(min_step(next_board))
    return max(results)

def human_move(board, symbol, ai_symbol):
    end, score = game_over(board)
    if end == True:
        print("\n" + display_board(board))
        if score==1:
            if symbol=="O":
                print("AI WINS")
            else:
                print("HUMAN WINS")
        elif score==2:
            if symbol=="X":
                print("AI WINS")
            else:
                print("HUMAN WINS")
        else:
            print("DRAW")
        return board
    print("\n" + "your turn, board: " + "\n" + display_board(board))
    possible_moves = []
    for x in range(len(board)):
        if board[x]==".":
            possible_moves.append(x)
    print("possible moves: " + str(possible_moves))
    move = int(input("what is your move? "))
    board = board[:move] + symbol + board[move+1:]
    ai_move(board, ai_symbol, symbol)

def ai_move(board, symbol, human_symbol):
    end, score = game_over(board)
    if end == True:
        display_board("\n" + board)
        if score==1:
            if symbol=="X":
                print("AI WINS")
            else:
                print("HUMAN WINS")
        elif score==2:
            if symbol=="O":
                print("AI WINS")
            else:
                print("HUMAN WINS")
        else:
            print("DRAW")
        return board
    print("\n" + "ai's turn, board: " + "\n" + display_board(board))
    scores, possible_next = [], possible_next_spaces(board, symbol)
    print("possible ai moves: ")
    for poss in possible_next:
        if symbol=="X":
            scores.append(min_step(poss[1]))
            if scores[-1]==1:
                print("moving at " + str(poss[0]) + " results in a " + "W")
            elif scores[-1]==-1:
                print("moving at " + str(poss[0]) + " results in a " + "L")
            else:
                print("moving at " + str(poss[0]) + " results in a " + "T")
        else:
            scores.append(max_step(poss[1]))
            if scores[-1]==1:
                print("moving at " + str(poss[0]) + " results in a " + "L")
            elif scores[-1]==-1:
                print("moving at " + str(poss[0]) + " results in a " + "W")
            else:
                print("moving at " + str(poss[0]) + " results in a " + "T")
    if symbol=="X":
        if 1 in scores:
            human_move(possible_next[scores.index(1)][1], human_symbol, symbol)
        elif 0 in scores:
            human_move(possible_next[scores.index(0)][1], human_symbol, symbol)
        else:
            human_move(possible_next[scores.index(-1)][1], human_symbol, symbol)
    if symbol=="O":
        if -1 in scores:
            human_move(possible_next[scores.index(-1)][1], human_symbol, symbol)
        elif 0 in scores:
            human_move(possible_next[scores.index(0)][1], human_symbol, symbol)
        else:
            human_move(possible_next[scores.index(1)][1], human_symbol, symbol)

board = sys.argv[1]
if board.count("X")==0 and board.count("O")==0:
    human = input("Will you play X or O? ")
    if human=="X":
        human_move(board, "X", "O")
    else:
        ai_move(board, "X", "O")
elif board.count("X")==board.count("O"):
    ai_move(board, "X", "O")
else:
    ai_move(board, "O", "X")
# python tictactoe.py .........