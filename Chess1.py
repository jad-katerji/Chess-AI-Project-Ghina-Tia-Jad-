import secrets
import numpy as np
from math import inf as infinity
import time
import copy

class Chess1:
    

    def __init__(self):
        # Define players
        self.MAX = "white"
        self.MIN = "black"
        
        #define a dictionairy "Actions" to contain the actions of each piece
        self.Actions ={ "p" : [(1,0), (1,1), (1,-1)],
                        "R" : [(1,0), (-1,0), (0,1), (0,-1)],
                        "N" : [(2,1), (1,2), (-2,1), (1,-2), (2,-1), (-1,2), (-2,-1), (-1,-2)],
                        "B" : [(1,1),(-1,1),(1,-1), (-1,-1)],
                        "Q" : [(1,1),(-1,1),(1,-1), (-1,-1), (1,0), (-1,0), (0,1), (0,-1)],
                        "K" : [(1,1),(-1,1),(1,-1), (-1,-1), (1,0), (-1,0), (0,1), (0,-1)]
            }
        
        # Define initial empty state
        self.state = np.array([["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        )
        self.initState = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        
        self.nbExpandedNodes=0
        
    def Reset(self):
        self.state=copy.deepcopy(self.initState)
        self.nbExpandedNodes=0
                
    def GetNextPossibleMoves(self, player):
        possibleMoves = []
        
        for piece in self.AvailablePieces(player):
            possibleMoves = possibleMoves + self.generate_possible_moves(piece)
        
        return possibleMoves

    def Evaluate(self):
        # Piece values
        piece_values = {
            'wp': 1, 'wN': 3, 'wB': 3, 'wR': 5, 'wQ': 9, 'wK': 0,  # White pieces
            'bp': -1, 'bN': -3, 'bB': -3, 'bR': -5, 'bQ': -9, 'bK': 0  # Black pieces
        }
        
        # Positional scores (simplified for pawns and knights)
        pawn_table = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
            [0, 0, 0, 2, 2, 0, 0, 0],
            [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
            [0.5, 1, 1, -2, -2, 1, 1, 0.5],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        
        knight_table = [
            [-5,  -4,  -3,  -3,  -3,  -3,  -4, -5],
            [-4,  -2,   0,   0,   0,   0,  -2, -4],
            [-3,   0,   1, 1.5, 1.5,   1,   0, -3],
            [-3, 0.5, 1.5,   2,   2, 1.5, 0.5, -3],
            [-3,   0, 1.5,   2,   2, 1.5,   0, -3],
            [-3, 0.5,   1, 1.5, 1.5,   1, 0.5, -3],
            [-4,  -2,   0, 0.5, 0.5,   0,  -2, -4],
            [-5,  -4,  -3,  -3,  -3,  -3,  -4, -5]
        ]
        
        # Evaluate material
        material_score = 0
        positional_score = 0
        for row in range(len(self.state)):
            for cell in range(len(self.state[row])):
                if self.state[row][cell] != "--":
                    
                    #generating the piece
                    piece = (self.state[row][cell], (row,cell))
                    
                    # Material score
                    material_score += piece_values[piece[0]]
                    
                    # Positional score
                    if piece[0][1] == 'p':  # Pawns
                        positional_score += pawn_table[piece[1][0]][piece[1][1]] if "w" in piece[0] else -pawn_table[piece[1][0]][piece[1][1]]
                    elif piece[0][1] == 'N':  # Knights
                        positional_score += knight_table[piece[1][0]][piece[1][1]] if "w" in piece[0] else -knight_table[piece[1][0]][piece[1][1]]
            
        # Mobility
        available_moves = self.GetNextPossibleMoves(self.MAX)
        
        
            
        mobility_score = len(available_moves)
        
        # Combine scores
        evaluation = material_score + positional_score + 0.1 * mobility_score
        return evaluation
  

    def IsGameWon(self, player): 
        opponent = self.MIN if player == self.MAX else self.MAX
        opponent_king = "bK" if opponent == self.MIN else "wK"
        
        # Check if the opponent's king is still on the board
        for row in self.state:
            if opponent_king in row:
                return False
        return True
        
    def IsDraw(self):
        # Stalemate
        if not self.GetNextPossibleMoves():
            return True
    
        # Insufficient material
        pieces = "".join(["".join(row) for row in self.state])
        if all(p in "wbK--" for p in pieces):  # Only kings are left
            return True
        return False

    def GameOver(self):
        if self.IsGameWon(self.MAX) or self.IsGameWon(self.MIN) or self.IsDraw():
            return True
        return False


    def ExecuteMove(self, move, player):
        start, end = move
        captured_piece = self.state[end[0]][end[1]]  # Store end state in case there is a captured piece
        self.state[end[0]][end[1]] = self.state[start[0]][start[1]]  
        self.state[start[0]][start[1]] = "--"  
        return captured_piece  # Return captured piece for undo 


    def UndoMove(self, move):
        start, end, captured_piece = move
        self.state[start[0]][start[1]] = self.state[end[0]][end[1]]  # Move piece back
        self.state[end[0]][end[1]] = captured_piece  # Restore captured piece or empty square
        return self.state

    def DisplayBoard(self):
        print("Expanded nodes:",self.nbExpandedNodes)
        print(game.state)
        print("\n")
        
        
    
    
    def AvailablePieces(self, player): # returns [("piece name",(x,y))]
        Pieces = []
        if (player == self.MAX):
            for i in range(len(self.state)):
                for j in range(len(self.state[i])):
                    if 'w' in self.state[i][j]: Pieces.append((self.state[i][j], (i,j)))
        else:
            for i in range(len(self.state)):
                for j in range(len(self.state[i])):
                    if 'b' in self.state[i][j]: Pieces.append((self.state[i][j], (i,j)))
                    
        return Pieces
        
    def generate_possible_moves(self, piece): # piece = ("piece name", (x,y))
        moves = []
        
        
        if "w" in piece[0]:
            key = piece[0][1] #gets a key for self.Actions 
            for move in self.Actions[key]:
                dx,dy = move
                x,y = piece[1]
                
                if key == 'p' or key == 'N' or key == 'K': # pieces with non-iterative moves
                    x -= dx
                    y -= dy
                    
                    if 0 <= x < 8 and 0 <= y < 8: #to stay within bounds
                        if self.state[x][y] == "--": #empty space
                            moves.append((piece[0], (x,y)))
                        elif "b" in self.state[x][y]: # capture
                            moves.append((x,y))
                
                else:  # pieces with iterative moves 
                    while True:
                        x -= dx
                        y -= dy
                        
                        if 0 <= x < 8 and 0 <= y < 8: #to stay within bounds
                            if self.state[x][y] == "--": #empty space
                                moves.append((x,y))
                            elif "b" in self.state[x][y]: # capture
                                moves.append((x,y))
                            else: break # friendly piece
                        else: break
            return moves
            
        if "b" in piece[0]:
            key = piece[0][1] #gets a key for self.Actions 
            for move in self.Actions[key]:
                dx,dy = move
                x,y = piece[1]
                
                if key == 'p' or key == 'N' or key == 'K': # pieces with non-iterative moves
                    x += dx
                    y += dy
                    
                    if 0 <= x < 8 and 0 <= y < 8: #to stay within bounds
                        if self.state[x][y] == "--": #empty space
                            moves.append((x,y))
                        elif "w" in self.state[x][y]: # capture
                            moves.append((x,y))
                
                else:  # pieces with iterative moves 
                    while True:
                        x += dx
                        y += dy
                        
                        if 0 <= x < 8 and 0 <= y < 8: #to stay within bounds
                            if self.state[x][y] == "--": #empty space
                                moves.append((x,y))
                            elif "w" in self.state[x][y]: # capture
                                moves.append((x,y))
                            else: break # friendly piece
                        else: break
            return moves
            
            

#-------------------------------MiniMax no improvement-------------
    def MiniMax(self,player,alpha,beta):
        self.nbExpandedNodes=self.nbExpandedNodes+1
        depth=5
        if self.GameOver() or self.nbExpandedNodes==depth:
            score = self.Evaluate()
            self.nbExpandedNodes=0
            return score
        elif player==self.MAX:
            return self.MaxValue(alpha,beta)
        else:
            return self.MinValue(alpha,beta)
        
    def MaxValue(self,alpha,beta):
        v=-infinity
        for move in self.GetNextPossibleMoves(self.MAX):
            self.ExecuteMove(move,self.MAX)
            score=self.MiniMax(self.MIN,alpha,beta)
            v=max(v,score)
            if v >= beta:
                return v
            alpha= max(alpha, v)
            self.UndoMove(self,move)
        return v
    def MinValue(self,alpha,beta):
        v=+infinity
        for move in self.GetNextPossibleMoves(self.MIN):
            self.ExecuteMove(move,self.MIN)
            score=self.MiniMax(self.MAX,alpha,beta)
            v=min(v,score)
            if v<=alpha:
                return v
            beta =min(beta,v)
            self.UndoMove(self,move)
        return v
    
    def GetBestMove(self,player):
        bestMove=None
        if player==self.MAX:
            nextPlayer=self.MIN
            bestScore=-infinity
        if player==self.MIN:
            nextPlayer=self.MAX
            bestScore=+infinity
        alpha=-infinity
        beta=+infinity
        for move in self.GetNextPossibleMoves(player):
            self.ExecuteMove(move,player)
            moveScore=self.MiniMax(nextPlayer,alpha,beta)
            self.UndoMove(self,move)
            if player==self.MAX:
                if moveScore>bestScore:
                    bestMove=move
                    bestScore=moveScore
            elif player==self.MAX:
                if moveScore<bestScore:
                    bestMove=move
                    bestScore=moveScore
                    
        return (bestMove,bestScore)
#-------------------------------End of MiniMax no improvement-------

    def basicEvaluate(self,player):
        piecePoints={'p':1,'R':5,'N':3,'B':3,'Q':9}
        score=0
        playerColor=self.MAX[0]
        opponentColor=self.MIN[0]

        for piece in self.AvailablePieces(player):
            if piece[0]==playerColor:
                score+=piecePoints[piece[1]]
            elif piece[0]==opponentColor:
                score-=piecePoints[piece[1]]
        return score


game = Chess1()
game.DisplayBoard()
print(game.Evaluate())

