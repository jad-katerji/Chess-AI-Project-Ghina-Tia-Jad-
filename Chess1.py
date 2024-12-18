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
                
<<<<<<< HEAD
    def GetNextPossibleMoves(self,player):
=======
    def GetNextPossibleMoves(self, player):
>>>>>>> 5aa64d18c4fd666698e8b762ba6d2e9ec2b805b7
        possibleMoves = []
        
        for piece in self.AvailablePieces(player):
            possibleMoves = possibleMoves + self.generate_possible_moves(piece)
        
        return possibleMoves

    def Evaluate(self, player):
        # Piece values and piece-square tables
        piece_values = {'p': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 0}
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
            [-5, -4, -3, -3, -3, -3, -4, -5],
            [-4, -2, 0, 0, 0, 0, -2, -4],
            [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
            [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
            [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
            [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
            [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
            [-5, -4, -3, -3, -3, -3, -4, -5]
        ]

        # Player and opponent
        player_color = 'w' if player == self.MAX else 'b'
        opponent_color = 'b' if player == self.MAX else 'w'

        # Material and positional evaluation
        material_score = 0
        positional_score = 0
        for i in range(8):
            for j in range(8):
                piece = self.state[i][j]
                if piece == "--":
                    continue
                piece_type = piece[1]
                piece_color = piece[0]

                # Material score
                material_value = piece_values[piece_type]
                if piece_color == player_color:
                    material_score += material_value
                else:
                    material_score -= material_value

                # Positional score
                if piece_type == 'p':  # Pawns
                    table_score = pawn_table[i][j]
                elif piece_type == 'N':  # Knights
                    table_score = knight_table[i][j]
                else:
                    table_score = 0

                if piece_color == player_color:
                    positional_score += table_score
                else:
                    positional_score -= table_score

        # King safety evaluation
        player_king = 'wK' if player_color == 'w' else 'bK'
        opponent_king = 'bK' if player_color == 'w' else 'wK'
        
        player_king_position = self.find_piece(player_king)
        opponent_king_position = self.find_piece(opponent_king)
        king_safety_score = 0
        if player_king_position:
            king_safety_score += self.king_safety(player_king_position, player_color)
        if opponent_king_position:
            king_safety_score -= self.king_safety(opponent_king_position, opponent_color)

        # Pawn structure evaluation
        pawn_structure_score = self.evaluate_pawn_structure(player_color) - self.evaluate_pawn_structure(opponent_color)

        # Mobility evaluation
        mobility_score = len(self.GetNextPossibleMoves(player)) * 0.1

        # Game phase adjustment
        phase = self.game_phase()
        endgame_score = 0
        if phase == "endgame":
            endgame_score += self.evaluate_endgame(player_color, opponent_color)

        # Final evaluation
        total_score = material_score + positional_score + king_safety_score + pawn_structure_score + mobility_score + endgame_score
        return total_score


    def find_piece(self, piece):
        for i in range(8):
            for j in range(8):
                if self.state[i][j] == piece:
                    return (i, j)
        return None


    def king_safety(self, king_position, king_color):
        x, y = king_position
        safety_score = 0

        # Penalize kings on open files or without pawn shelter
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    piece = self.state[nx][ny]
                    if piece != "--" and piece[0] == king_color:
                        safety_score += 0.2

        return safety_score


    def evaluate_pawn_structure(self, player_color):
        pawns = [(i, j) for i in range(8) for j in range(8) if self.state[i][j] == f"{player_color}p"]
        score = 0
        for x, y in pawns:
            # Penalize isolated pawns
            is_isolated = all(
                not (0 <= nx < 8 and self.state[nx][y] == f"{player_color}p")
                for nx in [x - 1, x + 1]
            )
            if is_isolated:
                score -= 0.5

            # Penalize doubled pawns
            if sum(1 for i in range(8) if self.state[i][y] == f"{player_color}p") > 1:
                score -= 0.3

            # Reward passed pawns
            if all(
                not (0 <= nx < 8 and 0 <= ny < 8 and self.state[nx][ny][0] != player_color)
                for nx, ny in [(x + dx, y + dy) for dx in [-1, 1] for dy in [-1, 0, 1]]
            ):
                score += 0.5

        return score


    def game_phase(self):
        material_count = sum(
            1 for i in range(8) for j in range(8) if self.state[i][j][1] in ['R', 'N', 'B', 'Q']
        )
        if material_count > 12:
            return "opening"
        elif material_count > 6:
            return "middlegame"
        else:
            return "endgame"


    def evaluate_endgame(self, player_color, opponent_color):
        # Reward king activity and passed pawns in the endgame
        score = 0
        player_king = find_piece(state, 'wK' if player_color == 'w' else 'bK')
        if player_king:
            x, y = player_king
            score += (7 - x) * 0.1 if player_color == 'w' else x * 0.1

        # Check for passed pawns
        score += evaluate_pawn_structure(player_color)
        score -= evaluate_pawn_structure(opponent_color)
        return score
  

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
        if not self.GetNextPossibleMoves(self.MAX):
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


    def ExecuteMove(self, move):
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
                            moves.append((piece[1], (x,y))) 
                        elif "b" in self.state[x][y]: # capture
                            moves.append((x,y))
                
                else:  # pieces with iterative moves 
                    while True:
                        x -= dx
                        y -= dy
                        
                        if 0 <= x < 8 and 0 <= y < 8: #to stay within bounds
                            if self.state[x][y] == "--": #empty space
                                moves.append((piece[1], (x,y)))
                            elif "b" in self.state[x][y]: # capture
                                moves.append((x,y))
                            else: break # friendly piece
                        else: break
            return moves # move = ((oldx,oldy),(newx,newy))
            
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
                            moves.append((piece[1], (x,y)))
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
                                moves.append((piece[1], (x,y)))
                            else: break # friendly piece
                        else: break
            return moves # move = ((oldx,oldy),(newx,newy))
            
            

#-------------------------------MiniMax no improvement-------------
    def MiniMax(self,player,alpha,beta):
        self.nbExpandedNodes=self.nbExpandedNodes+1
        depth=3
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
            captured_piece = self.ExecuteMove(move)
            score=self.MiniMax(self.MIN,alpha,beta)
            v=max(v,score)
            if v >= beta:
                return v
            alpha= max(alpha, v)
            self.UndoMove((move[0], move[1], captured_piece))
        return v
    def MinValue(self,alpha,beta):
        v=+infinity
        for move in self.GetNextPossibleMoves(self.MIN):
            self.ExecuteMove(move)
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
            self.ExecuteMove(move)
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

<<<<<<< HEAD
    def basicEvaluate(self,player):
        piecePoints={'p':1,'R':5,'N':3,'B':3,'Q':9}
        score=0
        if player==self.MAX:
            opponent=self.MIN
        else:
            opponent=self.MAX

        for piece in self.AvailablePieces(player): 
            score+=piecePoints[piece[1]]
        for piece in self.AvailablePieces(opponent):
            score-=piecePoints[piece[1]]
        return score
=======
>>>>>>> 5aa64d18c4fd666698e8b762ba6d2e9ec2b805b7

    def kingPosition(self,player):
        color=player[0]
        king=color+'K'
        kingPosition=()
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j]==king:
                    kingPosition=(i,j)
                    return kingPosition
                
    
    def check(self,player):
        threats=[]
        if player==self.MAX:
            opponent=self.MIN
        else:
            opponent=self.MAX
        for piece in self.AvailablePieces(opponent):
            if self.validMove(piece,self.kingPosition(player)):
                threats.append(piece)
        if threats:
            return threats
        return False

    def validMove(self,piece,endPosition):
        for move in self.generate_possible_moves(piece):
            if move==endPosition:
                return True
        return False

    def checkMate(self,player):#if the king is checked and if king cant move and if none of the remaining player pieces can block the check
        color=player[0]
        king=color+'K'

        if self.check(player) and not self.generate_possible_moves((king,self.kingPosition(player))) and not self.canBlockCheck(player):
            return True
        return False
    
    def canBlockCheck(self,player):
        protected=True
        if self.check(player):
            for move in self.GetNextPossibleMoves(player):
                self.ExecuteMove(move)
                if self.check(player):
                    protected=False
                else:
                    protected=True
                self.UndoMove(move)

                if protected:
                    return True
            return False
        return True


    
    
        
    



game = Chess1()
game.DisplayBoard()
print(game.Evaluate("white"))

