#check for total liberty
#check for randomness in valid moves
#u may have to return board wihout died piece
#piplani
from copy import deepcopy

BLACK_PIECES=0
WHITE_PIECES=0
print("Piplani: ", "*"*30)

def read_input(path="input.txt"):
    with open(path, 'r') as f:
        lines = f.readlines()

        player = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:6]]
        current_board = [[int(x) for x in line.rstrip('\n')] for line in lines[6:11]]

        return player, previous_board, current_board


def write_output(result, path="output.txt"):
    res = ""
    if result == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)


def on_board(i, j):
    if i < 5 and j < 5 and i >= 0 and j >= 0:
        return True
    else:
        return False


def detect_neighbor(i, j):
    neighbors = []
    coordinates = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    for co in coordinates:
        new_x = i + co[0]
        new_y = j + co[1]
        if on_board(new_x, new_y):
            neighbors.append((new_x, new_y))
    return neighbors


def detect_neighbor_ally(i, j, board, player):
    neighbors = detect_neighbor(i, j)  # Detect neighbors
    group_allies = []
    for ne in neighbors:
        # the same color
        if board[ne[0]][ne[1]] == player:
            group_allies.append(ne)
    return group_allies


def all_ally_positions(i, j, board, player):
    # https://github.com/umbriel47/aigo/blob/master/board.py#L95

    if not on_board(i, j):
        return []

    all_allies = []
    neighbors = detect_neighbor_ally(i, j, board, player)
    all_allies.append((i, j))
    visited = {}
    visited[(i, j)] = True
    while True:
        temp_list = neighbors
        neighbors = []
        for x, y in temp_list:
            if (x, y) not in visited and board[x][y] == player:
                all_allies.append((x, y))
                visited[(x, y)] = True
                next_neighbor = detect_neighbor_ally(x, y, board, player)
                for ne in next_neighbor:
                    neighbors.append(ne)
        if len(neighbors) == 0:
            return []
    return all_allies


def all_positions(i, j, board, player):
    stack = [(i, j)]  # stack for DFS serach
    ally_members = []  # record allies positions during the search
    while stack:
        piece = stack.pop()
        ally_members.append(piece)
        neighbor_allies = detect_neighbor_ally(piece[0], piece[1], board, player)
        for ally in neighbor_allies:
            if ally not in stack and ally not in ally_members:
                stack.append(ally)
    return ally_members


def find_count_liberty(i, j, board, player):
    my_all_allies = all_positions(i, j, board, player)
    # print("hey in function fcl",my_all_allies)
    for ally in my_all_allies:
        neighbors = detect_neighbor(ally[0], ally[1])
        # print("kiii",neighbors)
        for piece in neighbors:
            # print("piece",piece)
            if board[piece[0]][piece[1]] == 0:
                
                return True
    return False


def find_died_pieces(player, board):
    died_pieces = []

    for i in range(0, 5):
        for j in range(0, 5):

            if board[i][j] == player:

                if not find_count_liberty(i, j, board, player):
                    died_pieces.append((i, j))
    return died_pieces


def remove_died_pieces(died_pieces, board):
    for piece in died_pieces:
        board[piece[0]][piece[1]] = 0
    return board


# check for capture liberty....
# check for self capture
def get_liberty_positions(i, j,board,player):
    liberties=set()
    allyMembers = all_positions(i, j,board,player)
    for member in allyMembers:
        neighbors = detect_neighbor(member[0], member[1])
        for piece in neighbors:
            if board[piece[0]][piece[1]] == 0:
                
                liberties=liberties|set([piece])
              
                
    #print(i,j)
    #print("lib",list(liberties))
    return list(liberties)


def get_neigh_liberty_positions(i,j,board,player):
    liberties = set()
    neighbors = detect_neighbor(i,j)
    for piece in neighbors:
        if board[piece[0]][piece[1]] == 0:
            liberties=liberties|set([piece])
    #print(i,j)
    #print("lib",list(liberties))
    return list(liberties)
    
def try_move(i, j, board, player):
    new_board = board

    new_board[i][j] = player
   # print("check in try",endangeredLiberties(new_board,player))
    died_pieces = find_died_pieces(3 - player, new_board)

    if len(died_pieces) == 0:
        return new_board,len(died_pieces),new_board
    else:
        next_board = remove_died_pieces(died_pieces, new_board)

        return next_board,len(died_pieces),new_board



def valid_moves(player, previous_board, new_board):
    moves = []
    imp_moves=[]
    counter = 1
    trial = 0
    self_end_1=[]
    safe_moves_important=[]
    self_end_2=set()
    oppo_end_2=set()
    
    all_liberties_vala_move=set()

    for i in range(0, 5):
        for j in range(0, 5):
            #print(player)
            if new_board[i][j]==player:    
                #print(i,j)
                self_end=get_liberty_positions(i,j,new_board,player)
                #print("yahi hai khatarnak",self_end)
                if len(self_end)==1:
                    all_liberties_vala_move=all_liberties_vala_move|set(self_end)
                    if i==0 or i==4 or j==0 or j==4:
                        safe_positions=get_neigh_liberty_positions(self_end[0][0],self_end[0][1],new_board,player)
                        if safe_positions:
                            all_liberties_vala_move=all_liberties_vala_move|set(safe_positions)
                        #all_liberties_vala_move.add(set(safe_positions))
                    #print("kaise",all_liberties_vala_move_1)
                    #return list(all_liberties_vala_move_1)
     
            elif new_board[i][j]==3-player:
                oppo_end=get_liberty_positions(i,j,new_board,3-player)
                #print("oopo",i,j,oppo_end)
                all_liberties_vala_move=all_liberties_vala_move|set(oppo_end)
   
   
    if len(list(all_liberties_vala_move)):
        #print("yaar")
        for x in list(all_liberties_vala_move):
            tri_board = deepcopy(new_board)
            board_after_move,died_pieces,_ = try_move(x[0],x[1], tri_board, player)
                #print(x[0],x[1],died_pieces)
                    #print("condition 4",find_count_liberty(i, j, board_after_move, player))
            if find_count_liberty(x[0], x[1], board_after_move, player)and board_after_move != new_board and board_after_move != previous_board:
                imp_moves.append((x[0], x[1],died_pieces)) 
        if len(imp_moves)!= 0:
            return sorted(imp_moves, key=lambda x: x[2],reverse=True)
        
        
    
        
    for i in range(0, 5):
        for j in range(0, 5):
          
            if  new_board[i][j] == 0:
              
                trial_board = deepcopy(new_board)
                board_after_move,died_pieces,_ = try_move(i, j, trial_board, player)
                    #print("condition 4",find_count_liberty(i, j, board_after_move, player))
                if find_count_liberty(i, j, board_after_move, player) and board_after_move != new_board and board_after_move != previous_board:
                        #print("check in vm",endangeredLiberties(board_after_move,player))
                       
                            #print("idhar")
                    moves.append((i, j,died_pieces))
                            


    return sorted(moves, key=lambda x: x[2],reverse=True)
        
    
  

    # improvise
def get_group_count_with_k_liberties(board,player,k):
    
    mine_grps_count = 0
    opponent_gps_count = 0
    
    for i in range(0,5):
        for j in range(0,5):
            if board[i][j] ==player:
                lib = get_liberty_positions(i,j,board,player)
                if len(set(lib)) <= k:
                    mine_grps_count=mine_grps_count+len(lib)
            if board[i][j] ==3-player:
                lib = get_liberty_positions(i,j,board,3-player)
                if len(set(lib)) <= k:
                    opponent_gps_count=opponent_gps_count+len(lib)
                
                    
    return mine_grps_count,opponent_gps_count

def evaluation_function(board, player,died_pieces_black,died_pieces_white):
    
    black_count = 0
    white_count = 0
    black_endangered_liberty=0
    white_endangered_liberty=0
    white_total_liberty=set()
    black_total_liberty=set()
    #self_groups,oppo_groups=get_group_count_with_k_liberties(board,player,2)
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == 1:
                lib=get_liberty_positions(i,j,board,1)
                #black_total_liberty=black_total_liberty | set(lib)
                if len(lib)<=1:#try 2
                    black_endangered_liberty=black_endangered_liberty+1
                black_count += 1
            elif board[i][j] == 2:
                lib=get_liberty_positions(i,j,board,2)
                #white_total_liberty=white_total_liberty | set(lib)
                if len(lib)<=1:
                    white_endangered_liberty=white_endangered_liberty+1
                white_count += 1
    white_count = white_count + 2.5
    if player==1:
        eval_value = black_count-white_count+white_endangered_liberty-black_endangered_liberty+died_pieces_white*10-died_pieces_black*16#try my total-uska total liberty
    else:
        eval_value = -black_count + white_count-white_endangered_liberty+black_endangered_liberty+died_pieces_black*10-died_pieces_white*16

    #eval_value=eval_value+oppo_groups-self_groups
    #print("player",player,eval_value)   
    return eval_value


def best_move(board,previous_board,player,depth):
    died_pieces_white=0
    score, actions = maximizer_value(board,previous_board,player,depth, float("-inf"), float("inf"),board)
    #print("yaar",score,actions)
    if len(actions) > 0:
        return actions[0]  
    else:
        return "PASS"


def maximizer_value(board,previous_board,player,depth, alpha, beta,new_board_without_died_pieces):
    global BLACK_PIECES
    global WHITE_PIECES
    if player==2:
        died_pieces_white=len(find_died_pieces(player,new_board_without_died_pieces))
        WHITE_PIECES=WHITE_PIECES+died_pieces_white
    if player==1:
        died_pieces_black=len(find_died_pieces(player,new_board_without_died_pieces))
        BLACK_PIECES=BLACK_PIECES+died_pieces_black
        
    
    
    
    if depth == 0:
        value = evaluation_function(board,player,BLACK_PIECES,WHITE_PIECES)
        if player==1:
            BLACK_PIECES=BLACK_PIECES-len(find_died_pieces(1,new_board_without_died_pieces))
        if player==2:
            WHITE_PIECES=WHITE_PIECES-len(find_died_pieces(2,new_board_without_died_pieces))
        return value,[]
        

    max_score = float("-inf")
    max_score_actions = []
    my_moves = valid_moves(player, previous_board, board)
    #print(type(my_moves))
    #print(len(my_moves))
    if len(my_moves)==25:
        return 100,[(2,2)]
    for move in my_moves:
        #print("idhar",move[0],move[1])
        trial_board = deepcopy(board)
        next_board,died_pieces,new_board_without_died_pieces = try_move(move[0], move[1], trial_board, player)
        #print("move max",move,died_pieces)
        score, actions = minimizer_value(next_board,board,3-player,depth-1, alpha, beta,new_board_without_died_pieces)
        
        
        if score > max_score:
            max_score = score
            max_score_actions = [move] + actions
            

        if max_score > beta:
            return max_score, max_score_actions

        if max_score > alpha:
            alpha = max_score

    return max_score, max_score_actions    
    
def minimizer_value(board,previous_board,player,depth, alpha, beta,new_board_without_died_pieces):
    global BLACK_PIECES
    global WHITE_PIECES
    if player==2:
        died_pieces_white=len(find_died_pieces(player,new_board_without_died_pieces))
        WHITE_PIECES=WHITE_PIECES+died_pieces_white
    if player==1:
        died_pieces_black=len(find_died_pieces(player,new_board_without_died_pieces))
        BLACK_PIECES=BLACK_PIECES+died_pieces_black
        
    if depth == 0:
        value = evaluation_function(board,player,BLACK_PIECES,WHITE_PIECES)
        if player==1:
            BLACK_PIECES=BLACK_PIECES-len(find_died_pieces(1,new_board_without_died_pieces))
        if player==2:
            WHITE_PIECES=WHITE_PIECES-len(find_died_pieces(2,new_board_without_died_pieces))
        return value,[]

    min_score = float("inf")
    min_score_actions = []
    my_moves = valid_moves(player, previous_board, board)
    
    for move in my_moves:
        trial_board = deepcopy(board)
        next_board,died_pieces,new_board_without_died_pieces = try_move(move[0], move[1], trial_board, player)
        #print("move min",move,died_pieces)
        score, actions = maximizer_value(next_board,board,3-player,depth-1, alpha, beta,new_board_without_died_pieces)
        #print("min",score,actions)
       
        if score < min_score:
            min_score = score
            min_score_actions = [move] + actions
            

        if min_score < alpha:
            return min_score, min_score_actions

        if min_score < beta:
            alpha = min_score

    return min_score, min_score_actions


def driver_function(player, previous_board, new_board):  
    depth=4
    #print(valid_moves(player, previous_board, new_board))
    #exit()
    good_move = best_move(new_board,previous_board,player,depth)
    #print(good_move)
    write_output(good_move)

player, previous_board, board = read_input()
driver_function(player, previous_board, board)