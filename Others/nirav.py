import math
import pprint
from pip import main
from read import readInput
from write import writeOutput
from host import GO

class MyPlayer():
    def __init__(self):
        self.type = 'random'
        self.main_i = -1
        self.main_j = -1
        self.MAX_DEPTH = 4

    def get_input(self, go, piece_type): 
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == 0:
                    possible_placements.append((i,j))

        pieces = {}
        pieces["my"] = piece_type
        pieces["opp"] = 1 if 1 != piece_type else 2
        died_pieces = {}
        died_pieces["my"] = 0
        died_pieces["opp"] = 0
        move1_check = 0
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] != 0:
                    move1_check = 1
        if move1_check == 0:
            return (2,2)
        _, self.main_i, self.main_j = self.max_value(go, possible_placements, -math.inf, math.inf, 4, pieces, -1, -1, died_pieces)
        if self.main_i == -1 and self.main_j == -1:
            return "PASS"
        return (self.main_i, self.main_j)

    def count_eyes(self, go, pieces):
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
                    
    # def total_liberty(self, go, pieces):
        
    #     board = go.board
    #     for i in range(go.size):
    #         for j in range(go.size): 
    #             if board[i][j] != 0:
    #                 neighbors = go.detect_neighbor(i, j)
    #                 for piece in neighbors:
    #                     if (board[piece[0]][piece[1]] == 0) and ((piece[0],piece[1]) not in checked_for_liberties[board[i][j]]):
    #                         liberties[board[i][j]] += 1
    #                         checked_for_liberties[board[i][j]].add((piece[0],piece[1]))

    #     return liberties
    
    def endangered_liberties(self, go, pieces):
        liberties = {}
        checked_for_liberties = {}
        liberties[pieces["my"]] = 0
        liberties[pieces["opp"]] = 0
        checked_for_liberties[pieces["my"]] = set()
        checked_for_liberties[pieces["opp"]] = set()
        endangered_liberties = {}
        endangered_liberties[pieces["my"]] = 0
        endangered_liberties[pieces["opp"]] = 0
        board = go.board
        endangered_groups = {}
        endangered_groups[pieces["my"]] = []
        endangered_groups[pieces["opp"]] = []
        checked = set()
        for i in range(go.size):
            for j in range(go.size): 
                temp = []
                lib_ct = 0
                if board[i][j] != 0 and (i,j) not in checked:
                    ally_members = go.ally_dfs(i, j)
                    for member in ally_members:
                        temp.append(member)
                        checked.add(member)
                        neighbors = go.detect_neighbor(member[0], member[1])
                        for piece in neighbors:
                            if board[piece[0]][piece[1]] == 0:
                                lib_ct += 1
                            if (board[piece[0]][piece[1]] == 0 and ((piece[0],piece[1]) not in checked_for_liberties[board[i][j]])):
                                liberties[board[i][j]] += 1
                                checked_for_liberties[board[i][j]].add((piece[0],piece[1]))
                    if lib_ct == 1:
                        # print(temp)
                        endangered_groups[board[i][j]].append(len(temp))
        endangered_liberties[pieces["my"]] = sum(endangered_groups[pieces["my"]])
        endangered_liberties[pieces["opp"]] = sum(endangered_groups[pieces["opp"]])
        return (liberties, endangered_liberties)

    def eval_values(self, go, pieces, died_pieces):
        # liberties = self.total_liberty(go, pieces)
        eyes = self.count_eyes(go, pieces)
        liberties, endangered_liberties = self.endangered_liberties(go, pieces)
        score_diff = 8*go.score(pieces["my"]) - 8*go.score(pieces["opp"])
        eyes_diff = 4*eyes[pieces["my"]] - 4*eyes[pieces["opp"]]
        liberties_diff = liberties[pieces["my"]] - 4*liberties[pieces["opp"]]
        died_diff = 4*died_pieces["my"] - 8*died_pieces["opp"]
        endangered_liberties_diff = 4*endangered_liberties[pieces["opp"]] - 8*endangered_liberties[pieces["my"]]
        komi = 8*math.ceil(go.komi)
        if pieces["my"] == 2:
            #print("liberties my = {}, liberties opp = {}, total my = {}, total opp = {}, eyes my = {}, eyes opp = {}, died my = {}, died opp = {}".format(liberties[pieces["my"]], liberties[pieces["opp"]], 8*go.score(pieces["my"]), 8*go.score(pieces["opp"]), 4*eyes[pieces["my"]], 4*eyes[pieces["opp"]], died_pieces["my"], died_pieces["opp"]))
            return score_diff + eyes_diff + liberties_diff + died_diff + endangered_liberties_diff + komi
        else:
            #print("liberties my = {}, liberties opp = {}, total my = {}, total opp = {}, eyes my = {}, eyes opp = {}, died my = {}, died opp = {}".format(liberties[pieces["my"]], liberties[pieces["opp"]], 8*go.score(pieces["my"]), 8*go.score(pieces["opp"]), 4*eyes[pieces["my"]], 4*eyes[pieces["opp"]], died_pieces["my"], died_pieces["opp"]))

            return score_diff + eyes_diff + liberties_diff + died_diff + endangered_liberties_diff - komi



    def max_value(self, go, possible_placements, alpha, beta, depth, pieces, main_i, main_j, died_pieces):
        if go.game_end(pieces["my"]) or depth == 0:
            score = self.eval_values(go,pieces, died_pieces)
            #print("Total score = ",score)
            return score, main_i, main_j
        total_placements = len(possible_placements)
        for i in range(total_placements):
            go_copy = go.copy_board()   
            #print(possible_placements)
            # print("Prev before placing")    
            # pprint.pprint(go_copy.previous_board)   
            # print("Curr before placing")                  
            # pprint.pprint(go_copy.board)                        
            if go_copy.place_chess(possible_placements[i][0], possible_placements[i][1], pieces["my"]):
                dead_pieces = go_copy.remove_died_pieces(pieces["opp"])
                dead_val = len(dead_pieces)*depth
                go_copy.set_board(pieces["opp"], go.board, go_copy.board)
                died_pieces["my"] += dead_val        
                # print("Prev after placing")    
                # pprint.pprint(go_copy.previous_board)  
                # print("Curr after placing")                                             
                # pprint.pprint(go_copy.board) 
                # print("="*10)  
                # ele = possible_placements.pop(0)                               
                #print('Befor MAX = ', possible_placements[i][0],possible_placements[i][1],'-', self.main_i, self.main_j)   
                a = self.min_value(go_copy, possible_placements + dead_pieces, alpha, beta, depth - 1, pieces, died_pieces)
                # possible_placements.append(ele)
                if alpha < a:
                    alpha = a
                    if depth == self.MAX_DEPTH:
                        main_i = possible_placements[i][0]
                        main_j = possible_placements[i][1]
                #print('MAX = ', possible_placements[i][0],possible_placements[i][1],'-', self.main_i, self.main_j, ' -- beta = ', beta, ' -- alpha = ',alpha)
                died_pieces["my"] -= dead_val
            
                if alpha >= beta:
                    return beta, main_i, main_j
        return alpha, main_i, main_j
  
          
    def min_value(self, go, possible_placements, alpha, beta, depth, pieces, died_pieces):
        flag = 0
        if go.game_end(pieces["my"]) or depth == 0:
            score = self.eval_values(go,pieces, died_pieces)
            #print("Total score = ",score)
            return score
        total_placements = len(possible_placements)
        for i in range(total_placements):
            #print(possible_placements)
            go_copy = go.copy_board()  
            # print("Prev before placing")    
            # pprint.pprint(go_copy.previous_board)   
            # print("Curr before placing")                  
            # pprint.pprint(go_copy.board) 
            if go_copy.place_chess(possible_placements[i][0], possible_placements[i][1], pieces["opp"]):
                flag = 1
                dead_pieces = go_copy.remove_died_pieces(pieces["my"])
                dead_val = len(dead_pieces)*(depth+1)
                go_copy.set_board(pieces["my"], go.board, go_copy.board)
                died_pieces["opp"] += dead_val   
                # print("Prev after placing")    
                # pprint.pprint(go_copy.previous_board)  
                # print("Curr after placing")                                             
                # pprint.pprint(go_copy.board)                           
                # ele = possible_placements.pop(0)       
                # print('Befor MIN = ', possible_placements[i][0],possible_placements[i][1],'-', self.main_i, self.main_j)        
                beta = min(beta, self.max_value(go_copy, possible_placements + dead_pieces,  alpha, beta, depth - 1, pieces, -1, -1, died_pieces)[0])
                # print('MIN = ', possible_placements[i][0],possible_placements[i][1],'-', self.main_i, self.main_j, ' -- beta = ', beta, ' -- alpha = ',alpha)                
                # possible_placements.append(ele)
                died_pieces["opp"] -= dead_val

                if beta <= alpha:
                    return alpha
        if flag == 0:
            go_copy = go.copy_board() 
            # print("Prev before Passing")    
            # pprint.pprint(go_copy.previous_board)   
            # print("Curr before Passing")                  
            # pprint.pprint(go_copy.board)  
            # print('Befor MIN = Pass -', self.main_i, self.main_j)                
            beta = min(beta, self.max_value(go_copy, possible_placements, alpha, beta, depth - 1, pieces, -1, -1, died_pieces)[0])
            # print("Opponent Passes")
            # print('MIN = PASS - ', self.main_i, self.main_j, ' -- beta = ', beta, ' -- alpha = ',alpha)                

            if beta <= alpha:
                return alpha

        return beta

    # def eval_position(self, go):

                 


if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = MyPlayer()
    action = player.get_input(go, piece_type)
    writeOutput(action)