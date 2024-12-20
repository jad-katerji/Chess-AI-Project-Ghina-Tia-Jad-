import secrets
import numpy as np
from math import inf as infinity
import time
from Chess1 import Chess1
from Chess2 import Chess2
import copy


agent1=Chess1()
agent2=Chess2()
GameState=np.array([["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
)
agent1Turn=True
staleMate=2
while (not agent1.GameOver()) or (not agent2.GameOver()):
    if agent1Turn:
        agent1.state=copy.deepcopy(GameState)
        print("\nAgent 1 turn...")
        bestMove,score=agent1.GetBestMove(agent1.MAX)
        if bestMove:
            print("Best Move: for ",agent1.MAX," ",bestMove," with score", score)
            GameState=agent1.ExecuteMove(bestMove)
        else:
            print("no moves available.")
            staleMate=staleMate-1
        agent1.DisplayBoard()
    else:		#human turn
        agent2.state=GameState
        print("\nAgent 2 turn...")
        bestMove,score=agent2.GetBestMove(agent2.MAX)
        if bestMove:
            print("Best Move: for ",agent2.MAX," ",bestMove," with score", score)
            GameState=agent1.ExecuteMove(bestMove,agent2.MAX)            
        else:
            print("no moves available.")
            staleMate=staleMate-1
        agent2.DisplayBoard()
    agent1Turn=not agent1Turn
    time.sleep(4)
    if staleMate==0:
        break
    
if agent2.IsGameWon(agent2.MAX):
    print("Agent 1 won")
elif agent2.IsGameWon(agent2.MAX):
    print("Agent 2 won")
else:
    print("Game Over, Draw")

