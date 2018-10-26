# 86400 Daniel Fernandes | 86416 Francisco Sousa | Grupo 74

from search import *

class sol_state:
    __slots__ = ["board"]

    def __init__(self, board):
        self.board = board

    def __lt__(self, other):
        return count_content(self.board, c_empty()) < count_content(other.board, c_empty())

class solitaire(Problem):
    """Models a Solitaire problem as a satisfaction problem.
    A solution cannot have more than 1 peg left on the board."""

    def __init__(self, board):
        Problem.__init__(self, sol_state(board))

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        return board_moves(state.board)

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        if action in self.actions(state):
            return sol_state(board_perform_move(state.board, action))
        else:
            raise ValueError("Action not possible.")

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        return count_content(state.board, c_peg()) == 1

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def h(self, node):
        """Needed for informed search."""
        return 2 * count_content(node.state.board, c_peg()) - len(movable_pegs(node.state.board))
        
        
def movable_pegs(board):
    moves = board_moves(board)
    res = []
    for m in moves:
        if move_initial(m) not in res:
            res += [move_final(m)]
    return res


def isolated_pegs(board):
    moves = board_moves(board)
    res = []
    for m in moves:
        if move_final(m) not in res:
            res += [move_final(m)]
    return res


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
    if not is_peg(get_content(board, pos)):
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

def copy_board(board):
    boardcopy = []
    for l in board:
        boardcopy += [l.copy()]
    return boardcopy

def board_perform_move(board, move):
    newboard = copy_board(board)
    change_content(newboard, move_initial(move), c_empty())
    change_content(newboard, middle_pos(move), c_empty())
    change_content(newboard, move_final(move), c_peg())
    return newboard

def count_content(board, content):
    count = 0
    if is_board(board):
        for l in range(len(board)):
            for c in range(len(board[l])):
                if get_content(board, make_pos(l, c)) == content:
                    count += 1
    else:
        raise ValueError("Not a board.")
    return count


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