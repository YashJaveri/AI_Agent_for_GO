from host import GO

class CustomGO(GO):
    def get_analysis(self, size):
        board = self.board
        white_libs = set()
        black_libs = set()
        whites = 0
        blacks = 0

        for i in range(size):
            for j in range(size):
                if board[i][j] == 1:                                        
                    blacks += 1
                    neighbors = self.detect_neighbor(i, j)                    
                    for piece in neighbors:
                        if board[piece[0]][piece[1]] == 0:
                            black_libs.add((piece[0], piece[1]))
                elif board[i][j] == 2:
                    whites += 1
                    neighbors = self.detect_neighbor(i, j)                                        
                    for piece in neighbors:
                        if board[piece[0]][piece[1]] == 0:
                            white_libs.add((piece[0], piece[1]))

        return blacks, whites, len(black_libs), len(white_libs)

    visited = set()
    libs_white = set()
    libs_black = set()
    
    def get_liberties(self, i, j, board):
        liberties = set()        
        allies = self.ally_dfs(i, j)
        allies.append((i,j))
        for mem in allies:
            self.visited.add(mem)            
            neighbors = self.detect_neighbor(mem[0], mem[1])
            for piece in neighbors:
                if board[piece[0]][piece[1]] == 0:
                    if board[i][j] == 1:
                        self.libs_black.add(piece)
                    elif board[i][j] == 2:
                        self.libs_white.add(piece)
                    liberties.add(piece)        
        return liberties, len(allies)

    def get_analysis2(self, size):        
        board = self.board        
        deadly_nodes_white = 0        
        deadly_nodes_black = 0
        whites = 0
        blacks = 0        

        self.visited.clear()
        self.libs_black.clear()
        self.libs_white.clear()
        
        for i in range(size):       #Amortised complexity is O(n^2)
            for j in range(size):
                if board[i][j] == 1:
                    blacks+=1                    
                    if (i,j) not in self.visited:
                        liberties, nodes = self.get_liberties(i, j, board)                        
                        if len(liberties)==1:
                            deadly_nodes_black += nodes                            
                elif board[i][j] == 2:
                    whites+=1
                    if (i,j) not in self.visited:
                        liberties, nodes = self.get_liberties(i, j, board)                        
                        if len(liberties)==1:
                            deadly_nodes_white += nodes

        return blacks, whites, len(self.libs_black), len(self.libs_white), deadly_nodes_black, deadly_nodes_white