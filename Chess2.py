import secrets
import numpy as np
from math import inf as infinity
import time
import copy

class Chess2:
    

    def __init__(self):
        # Define players
        self.MAX = "white"
        self.MIN = "black"

        # Define initial empty state
        self.state = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        
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
        #code goes here

#-------------------------------MiniMax no improvement-------------
    def MiniMax(self,player):
        self.nbExpandedNodes=self.nbExpandedNodes+1        
        if self.GameOver():
            score = self.Evaluate()
            return score
        elif player==self.MAX:
            return self.MaxValue()
        else:
            return self.MinValue()
        
    def MaxValue(self):
        #code goes here
        return v

    def MinValue(self):
        #code goes here
        return v
    
    def GetBestMove(self,player):
        #code goes here
        bestMove=None
        bestScore=None
        return (bestMove,bestScore)
#-------------------------------End of MiniMax no improvement-------



