import math
import time
import random
from gameTree import gameTree
from state import state
from player import player

'''
Expands the entire game tree.... not used in implementation of algorithms
'''
def expandTree(tree):
    root = tree.root
    allStates = tree.allStates
    stack = root.expandStates()
    while(len(stack) > 0):
        currentRoot = stack.pop()
        if(currentRoot not in allStates):
            allStates.add(currentRoot)
            stack.extend(currentRoot.expandStates())
    return allStates

# Algorithm that takes in a state and will perform minimax with Alpha-beta pruning on it,
# returning the ideal next state and the evaluated score of the state
def ABMove(state, depth, alpha, beta, depthLimit): 
    
    if(depth == depthLimit or state.checkWin()):
        return (state, state.evaluateScore())
        
    else:
        states = state.expandStates()
        # for state in states:
        #     if state.checkWin():
        #         return(state, state.evaluateScore())
        if len(states) == 0:
            x = 0       
        if(state.turn == 0):
            bestVal = float("-inf")
            for Nstate in states:
                
                value = ABMove(Nstate, depth+1, alpha, beta, depthLimit)[1]
                bestVal = max(value, bestVal)
                alpha = max(alpha, bestVal)
                if beta <= alpha:
                    break
            return (Nstate, bestVal)
        else:
            bestVal = float("inf")
            for Nstate in states:
                
                value = ABMove(Nstate, depth+1, alpha, beta, depthLimit)[1]
                bestVal = min(value, bestVal)
                beta = min(beta, bestVal)
                if beta >= alpha:
                    break
            return (Nstate, bestVal)


def playGame(currentRoot):

    count = 0
    while(not currentRoot.checkWin()):
        if(currentRoot.turn == 0):
            currentRoot = ABMove(currentRoot, 0,float("-inf"),float("inf"), 10)[0]
            print("MADE MOVE")
            print(currentRoot)
        else:
            currentRoot = ABMove(currentRoot, 0,float("-inf"),float("inf"), 1)[0]
            print("MADE MOVE")

            print(currentRoot)
            
       
        count+= 1

        print(count)
        print()
    if(currentRoot.turn == 0):
        print(currentRoot)
        print("Player 2 has won")
    else:
        print(currentRoot)
        print("Player 1 has won")



def main():
    gameT = gameTree(2, 5)

    # numStates = len(gameT.allStates)
    # copy = gameT.root.copyState()
    # copy.players[0].hands = [0,1,1]
    # copy.players[1].hands = [0,0,0]
    # copy.turn = 1
    # print(copy)
    # print(copy.checkWin())
    # s = copy.expandStates()
    # print(len(s))
    # for d in s: 
    #     print(s)  
    # print(copy.turn)

    ##### PLAY AB GAME #####
    playGame(gameT.root)

    ##### TEST EXPANDSTATES() #####
    # states = copy.expandStates()
    # for state in states:
    #     print(state)

    ##### COLLECTION OF AB MOVES ######
    # print("pre turn: " + str(copy.turn))
    # nextState = ABMove(copy, 0,float("-inf"),float("inf"), 5)[0]
    # print(nextState)
    # print("post turn: " + str(nextState.turn))

    # nextState = ABMove(nextState, 0,float("-inf"),float("inf"), 5)[0]
    # print
    # print(nextState)

    ##### TESTING MAKE MOVE ANYWAYS ###### (this works, but why doesn't it change with evaluate state?)
    # print(copy)
    # copy.makeTurn(0,0,False)
    # print(copy)

    
    
    # print(gameT.root)

    
    # gameT.allStates.add(gameT.root)
    # state = ABMove(gameT.root, 0, float("-inf"), float("inf"), 10)[0]
    # state = ABMove(state,0, float("-inf"), float("inf"), 10)[0]
    # print(state)

    # gameT.root.states = gameT.root.expandStates()

    # for state in gameT.root.states:
    #     print(state)
    #     print(state.score)
    
    
    #
    # print("_____")
    #
    #     if(state.checkWin()):
    #
    #         print("_______")
    #         print("Victory")
    #         print("_______")
    #
    #
    #
    #
    # print(len(gameT.allStates))
if __name__ == "__main__":
    main()
