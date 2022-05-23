import math
from read import readInput
from write import writeOutput
from m_host import CustomGO

def print_eval(blacks, whites, black_libs, white_libs, num_dead_pieces_me, num_dead_pieces_enemy, deadly_nodes_black, deadly_nodes_white):
        print("Piece Type: ", piece_type, end=", ")
        print("Blacks: ", blacks, end=", ")
        print("Whites: ", whites, end=", ")
        print("Blacks Lib: ", black_libs, end=", ")
        print("White lib: ", white_libs, end=", ")
        if piece_type == 1:
            print("Black dead: ", num_dead_pieces_me, end=", ")
            print("White dead: ", num_dead_pieces_enemy, end=", ")
        elif piece_type == 2:
            print("Black dead: ", num_dead_pieces_enemy, end=", ")
            print("White dead: ", num_dead_pieces_me, end=", ")
        print("Blacks Lib: ", deadly_nodes_black, end=", ")
        print("White lib: ", deadly_nodes_white, end=", ")
        print("")

def evaluator(go, num_dead_pieces_me, num_dead_pieces_enemy):
    eval = 0
    blacks, whites, black_non_deadly_libs, white_non_deadly_libs, deadly_nodes_black, deadly_nodes_white = go.get_analysis2(board_size)
    whites += 6
    if piece_type == 1:
        eval = (blacks*8 - whites*8) + (black_non_deadly_libs - 4*white_non_deadly_libs) + (num_dead_pieces_enemy*4 - 8*num_dead_pieces_me) + (deadly_nodes_white - deadly_nodes_black)
    else:
        eval = (whites*10 - blacks*10) + (white_non_deadly_libs- 4*black_non_deadly_libs) + (num_dead_pieces_enemy-num_dead_pieces_me) + (deadly_nodes_black - deadly_nodes_white)
    return eval

def max_value(go, possible_placements, num_dead_pieces_me, num_dead_pieces_enemy, alpha, beta, depth):
    global best_i, best_j
    if depth == 0:
        return evaluator(go, num_dead_pieces_me, num_dead_pieces_enemy)
    
    for move in possible_placements:
        go_clone = go.copy_board()
        if go_clone.place_chess(move[0], move[1], piece_type):
            dead_pieces_enemy = go_clone.remove_died_pieces(3-piece_type)
            go_clone.set_board(3-piece_type, go.board, go_clone.board)
            num_dead_pieces_enemy += len(dead_pieces_enemy)
            x = min_value(go_clone, possible_placements+dead_pieces_enemy, num_dead_pieces_me, num_dead_pieces_enemy, alpha, beta, depth)
            num_dead_pieces_enemy -= len(dead_pieces_enemy)
            if x>alpha:
                alpha = x
                if depth == min_max_depth:
                    best_i = move[0]
                    best_j = move[1]

            if alpha>=beta:
                return beta
    return alpha

def min_value(go, possible_placements, num_dead_pieces_me, num_dead_pieces_enemy, alpha, beta, depth):
    if depth == 0:        
        return evaluator(go, num_dead_pieces_me, num_dead_pieces_enemy)
    no_moves = True
    for move in possible_placements:
        go_clone = go.copy_board()
        if go_clone.place_chess(move[0], move[1], 3-piece_type):
            no_moves = False
            dead_pieces_me = go_clone.remove_died_pieces(piece_type)
            go_clone.set_board(piece_type, go.board, go_clone.board)
            num_dead_pieces_me += len(dead_pieces_me)
            x = max_value(go_clone, possible_placements+dead_pieces_me, num_dead_pieces_me, num_dead_pieces_enemy, alpha, beta, depth-1)
            num_dead_pieces_me -= len(dead_pieces_me)     
            if x<beta:
                beta = x
            if alpha>=beta:
                return alpha
    if no_moves==True:        
        go_clone = go.copy_board()
        x = max_value(go_clone, possible_placements, num_dead_pieces_me, num_dead_pieces_enemy, alpha, beta, depth-1)
        if x<beta:
            beta = x
        if alpha>=beta:
            return alpha

    return beta

def get_best_move(go):
    global best_i, best_j
    initial_move = True
    possible_placements = []

    for i in range(go.size):
        for j in range(go.size):
            if go.board[i][j] != 0:
                initial_move = False              
            else:
                possible_placements.append((i,j))

    if initial_move:
        best_i = 2
        best_j = 2
        return (best_i,best_i)
        
    _ = max_value(go, possible_placements, 0, 0, alpha_initial, beta_initial, min_max_depth)                    
    return (best_i, best_j)

def play():
    go = CustomGO(5)    
    go.set_board(piece_type, previous_board, curr_board)
    move = get_best_move(go)
    if best_i == -1 or best_j == -1:
        writeOutput("PASS")
    else:
        writeOutput(move)

if __name__ == '__main__':
    alpha_initial = -math.inf
    beta_initial = math.inf
    best_i = -1
    best_j = -1    
    min_max_depth = 2
    board_size = 5
    piece_type, previous_board, curr_board = readInput(5)
    play()