"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    
    x=0
    o=0

    for i in range(3):
        for y in range(3):
            if board[i][y]==X:x+=1
            if board[i][y]==O:o+=1

    return X if x == o == 0 else O if x > o else X


def actions(board):
   
    L=[]

    for i in range(3):
        for y in range(3):

            if board[i][y] == EMPTY : 
                L.append((i,y))

    return L


def result(board, action):
    
    boardbis=copy.deepcopy(board) 
    i, y=action
    p=player(board)
    
    if not action in actions(board):
        raise IndexError("that's the wrong number")
    
    else:

        boardbis[i][y]=p
        return boardbis


def winner(board):
    
    potL=player(board)                                                                              #potential L

    potW= X if potL == O else O                                                                     #potential W
    W=[potW]*3                                                                   


    if W in board: return potW                                                                       # we test if the win is horizontal


    if W == [board[i][i] for i in range(3)] or W == [board[i-1][-i] for i in range(1,4)] : return potW    # we test if the win is diagonal


    for o in range(3):
        if W == [board[i][o] for i in range(3)] : return potW                                       # we test if the win is vertcal

        
    return None      


def terminal(board):

    return len(actions(board)) == 0  or winner(board) != None


def utility(board):
    
    return 1 if winner(board) == X else 0 if not winner(board) and terminal(board) else -1

def maxValue(board):

    v=-float("inf")

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = max(v,minValue(result(board, action)))

    return v

def minValue(board):

    v=float("inf")

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v,maxValue(result(board,action)))

    return v


def minimax(board):
    if terminal(board):
        return None
    
    elif board == initial_state():
        return random.choice(actions(board))

    
    else:
        p = player(board)
        acts=[]

        if p == X : 
            for elt in actions(board):
                boardbis=result(board, elt)
                acts.append(minValue(boardbis))

            if len(acts) != len(actions(board)):
                raise Exception ("il y a un prob sur les action")

            return actions(board)[acts.index(max(acts))]
        
        else:
            for elt in actions(board):
                boardbis=result(board, elt)
                acts.append(maxValue(boardbis))

            if len(acts) != len(actions(board)):
                raise Exception ("il y a un prob sur les action")

            return actions(board)[acts.index(min(acts))]

