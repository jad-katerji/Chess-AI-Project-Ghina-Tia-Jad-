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
                
    def GetNextPossibleMoves(self):
        possibleMoves = []
        #code goes here
        
        return possibleMoves

    def Evaluate(self):
        #code goes here
        return 0  

    def IsGameWon(self, player):
        #code goes here
        return False

    def IsDraw(self):
        #code goes here
        return False

    def GameOver(self):
        #code goes here
        return False


    def ExecuteMove(self,move,player):
        #code goes here
        return self.state
    
    def UndoMove(self,move):
        #code goes here
        return self.state

    def DisplayBoard(self):
        print("Expanded nodes:",self.nbExpandedNodes)
        print(game.state)
        
        
    
    
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
                    x += dx
                    y += dy
                    
                    if 0 <= x < 8 and 0 <= y < 8: #to stay within bounds
                        if self.state[x][y] == "--": #empty space
                            moves.append((x,y))
                        elif "b" in self.state[x][y]: # capture
                            moves.append((x,y))
                
                else:  # pieces with iterative moves 
                    while True:
                        x += dx
                        y += dy
                        
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
print(game.generate_possible_moves(("wN",(3,3))))

