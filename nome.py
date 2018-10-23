#python3 -c 'from nome import *; print(oi())'

# TAI board
def is_board(board):
    if not isinstance(board, list):
        return False
    for l in board:
        if not isinstance(l, list):
            return False
        for e in l:
            if not (is_empty(e) or is_peg(e) or is_blocked(e)):
                return False
    return True

def get_pos(board, pos):
    return board[pos_l(pos)][pos_c(pos)]

def change_content(board, pos, content):
    board[pos_l(pos)][pos_c(pos)] = content


def get_content(board, pos):
    if not (0 <= pos_l(pos) < len(board) and 0 <= pos_c(pos) < len(board[pos_l(pos)])):
        raise ValueError("Position out of bounds.")
    return board[pos_l(pos)][pos_c(pos)]

def check_move(board, pos, func):
    try:
        if is_peg(get_content(board, func(pos))) and is_empty(get_content(board, func(func(pos)))):
            return make_move(pos, func(func(pos)))
        else:
            return []
    except ValueError:
        return []

def check_pos_moves(board, pos):
    moves = []
    if not is_peg(get_content(board, pos)): #falta um try aqui
        raise ValueError("not a peg")
    for f in [up_pos, down_pos, left_pos, right_pos]:
        m = check_move(board, pos, f)
        if m != []:
            moves.append(m)
    return moves

def board_moves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            try:
                moves += check_pos_moves(board, make_pos(i, j))
            except ValueError:
                continue
    return moves

def board_perform_move(board, move):
    newboard = board.copy()
    change_content(newboard, move_initial(move), c_empty())
    change_content(newboard, middle_pos(move), c_empty())
    change_content(newboard, move_final(move), c_peg())
    return newboard



# TAI content
def c_peg():
    return "O"

def c_empty():
    return "_"

def c_blocked():
    return "X"

def is_empty(e):
    return e == c_empty()

def is_peg(e):
    return e == c_peg()

def is_blocked(e):
    return e == c_blocked()

# TAI pos
# Tuplo (l, c)
def make_pos(l, c):
    return (l, c)

def pos_l(pos):
    return pos[0]

def pos_c(pos):
    return pos[1]

def up_pos(pos):
    return (pos_l(pos) - 1, pos_c(pos))

def down_pos(pos):
    return (pos_l(pos) + 1, pos_c(pos))

def left_pos(pos):
    return (pos_l(pos), pos_c(pos) - 1)

def right_pos(pos):
    return (pos_l(pos), pos_c(pos) + 1)

# TAI move
# Lista [p_initial, p_final]
def make_move(i, f):
    return [i, f]

def move_initial(move):
    return move[0]

def move_final(move):
    return move[1]

def middle_pos(move):
    if pos_l(move_initial(move)) == pos_l(move_final(move)):
        if pos_c(move_initial(move)) < pos_c(move_final(move)):
            return right_pos(move_initial(move))
        else:
            return left_pos(move_initial(move))
    else:
        if pos_l(move_initial(move)) < pos_l(move_final(move)):
            return down_pos(move_initial(move))
        else:
            return up_pos(move_initial(move))