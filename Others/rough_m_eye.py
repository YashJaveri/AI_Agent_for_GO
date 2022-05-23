import math
from read import readInput
from write import writeOutput
from m_host import CustomGO

def print_eval(blacks, whites, black_non_deadly_libs, white_non_deadly_libs, num_dead_pieces_me, num_dead_pieces_enemy, deadly_libs_black, deadly_libs_white):
        print("Piece Type: ", piece_type, end=", ")
        print("Blacks: ", blacks, end=", ")
        print("Whites: ", whites, end=", ")
        print("Blacks Lib: ", black_non_deadly_libs, end=", ")
        print("White lib: ", white_non_deadly_libs, end=", ")
        if piece_type == 1:
            print("Black dead: ", num_dead_pieces_me, end=", ")
            print("White dead: ", num_dead_pieces_enemy, end=", ")
        elif piece_type == 2:
            print("Black dead: ", num_dead_pieces_enemy, end=", ")
            print("White dead: ", num_dead_pieces_me, end=", ")
        
        print("")
def count_eyes(go, pieces):
        eyes = {}
        eyes[pieces["my"]] = 0
        eyes[pieces["opp"]] = 0
        board = go.board
        for i in range(go.size):
            for j in range(go.size): 
                if board[i][j] == 0:
                    start_flag = 0
                    count_flag = 1
                    curr_piece = -1
                    neighbors = go.detect_neighbor(i, j)
                    # print("For i,j - {},{}".format(i,j))
                    for piece in neighbors:
                        if start_flag == 0:
                            curr_piece = board[piece[0]][piece[1]]
                            if curr_piece == 0:
                                count_flag = 0
                                break
                            start_flag = 1
                            continue
                        if (board[piece[0]][piece[1]] != curr_piece):
                            count_flag = 0
                            break
                    # print("Piece = ",curr_piece)
                    # print("Flag = ",count_flag)
                    if count_flag == 1:
                        go_copy = go.copy_board()      
                        go_copy.board[i][j] = pieces["my"] if curr_piece == pieces["opp"] else pieces["my"]
                        for piece in neighbors:
                            if not go_copy.find_liberty(piece[0], piece[1]):
                                count_flag = 2
                                break
                    if count_flag == 1:
                        eyes[curr_piece] += 1
                        # print(eyes)
        return eyes

def evaluator(go, num_dead_pieces_me, num_dead_pieces_enemy):
    eval = 0    
    # blacks, whites, black_libs, white_libs = go.get_analysis(board_size)
    # whites += 6
    # if piece_type == 1:
    #     eval = (blacks - whites) + (black_libs - white_libs) + (num_dead_pieces_enemy - num_dead_pieces_me)
    # else:
    #     eval = -((blacks - whites) + (black_libs - white_libs) + (num_dead_pieces_me - num_dead_pieces_enemy))    
    #blacks, whites, black_non_deadly_libs, white_non_deadly_libs, deadly_libs_black, deadly_libs_white = go.get_analysis(board_size)

    blacks, whites, black_libs, white_libs = go.get_analysis(board_size)
    whites += 2.5
 
    if piece_type == 1:
        eyes = count_eyes(go, {"my":1, "opp":2})
        eval = (go.score(1) - go.score(2))*8 + (num_dead_pieces_enemy*4 - num_dead_pieces_me*8) + (eyes[1] - eyes[2])*4 + (black_libs-white_libs)
    else:
        eyes = count_eyes(go, {"opp":1, "my":2})
        eval = (go.score(2) - go.score(1))*8 + (num_dead_pieces_enemy*4 - num_dead_pieces_me*8) + (eyes[2] - eyes[1])*4 + (white_libs-black_libs)
    return eval

def max_val(go, num_dead_pieces_me, num_dead_pieces_enemy, alpha, beta, depth):
    global best_i, best_j

    if depth == 0:
        return evaluator(go, num_dead_pieces_me, num_dead_pieces_enemy)

    for i in range(board_size):
        for j in range(board_size):
            go_clone = go.copy_board()
            if go_clone.place_chess(i, j, piece_type):
                dead_pieces_enemy = go_clone.remove_died_pieces(3-piece_type)
                val = (len(dead_pieces_enemy)*depth)
                num_dead_pieces_enemy += val
                x = min_val(go_clone, num_dead_pieces_me, num_dead_pieces_enemy, alpha, beta, depth-1)                
                num_dead_pieces_enemy -= val

                if x>alpha:
                    alpha = x
                    if depth == min_max_depth:
                        best_i = i
                        best_j = j

                if alpha>=beta:                    
                    return beta
    return alpha

def min_val(go, num_dead_pieces_me, num_dead_pieces_enemy, alpha, beta, depth):
    global black_dead, white_dead
    no_move_avail = True
    if depth == 0:        
        return evaluator(go, num_dead_pieces_me, num_dead_pieces_enemy)

    for i in range(board_size):
        for j in range(board_size):
            go_clone = go.copy_board()
            if go_clone.place_chess(i, j, 3-piece_type):
                no_move_avail = False
                dead_pieces_me = go_clone.remove_died_pieces(piece_type)
                val = (len(dead_pieces_me)*(depth+1))
                num_dead_pieces_me += val
                x = max_val(go_clone, num_dead_pieces_me, num_dead_pieces_enemy, alpha, beta, depth-1)
                num_dead_pieces_me -= val

                if x<beta:
                    beta = x           
                if alpha>=beta:
                    return alpha
    if no_move_avail == True:
        go_clone = go.copy_board()
        x = max_val(go_clone, num_dead_pieces_me, num_dead_pieces_enemy, alpha, beta, depth-1)
        if x<beta:
            beta = x
        if alpha>=beta:
            return alpha

    return beta

def get_best_move(): 
    max_val(go, 0, 0, alpha_initial, beta_initial, min_max_depth)
    return (best_i, best_j)

def play():
    go.set_board(piece_type, previous_board, curr_board)
    move = get_best_move()    
    if best_i == -1 or best_j == -1:
        writeOutput("PASS")
    else:
        writeOutput(move)

if __name__ == '__main__':
    alpha_initial = -math.inf
    beta_initial = math.inf
    best_i = -1
    best_j = -1        
    go = CustomGO(5)
    min_max_depth = 4
    board_size = 5
    piece_type, previous_board, curr_board = readInput(5)    
    play()