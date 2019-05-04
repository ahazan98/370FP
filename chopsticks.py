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

    if(depth == depthLimit):
        return (state, state.evaluateScore())

    else:
        states = state.expandStates()

        if len(states) == 0:
            return(state, state.evaluateScore())
        bestState = state
        if(state.turn == 0):
            bestVal = float("-inf")
            for Nstate in states:
                result = ABMove(Nstate, depth+1, alpha, beta, depthLimit)
                if(result[1] > bestVal):
                    bestVal = result[1]
                    bestState = Nstate
                if(bestVal > alpha):
                    alpha = bestVal
                if beta <= alpha:
                    break
            return (bestState, bestVal)
        else:
            bestVal = float("inf")

            for Nstate in states:
                # print("Nstate")
                # print(Nstate)
                result = ABMove(Nstate, depth+1, alpha, beta, depthLimit)
                # print("result:" + str(result[1]))
                if(result[1] < bestVal):
                    bestVal = result[1]
                    bestState = Nstate
                # print("bestVal: "+ str(bestVal))
                if(bestVal < beta):
                    beta = bestVal
                # print("beta: "+str(beta))
                if beta <= alpha:
                    # print("here")
                    break
            # print(bestState)
            # print(bestVal)
            return (bestState, bestVal)


def playGame(currentRoot):

    count = 0

    while(not currentRoot.checkWin()):
        if(currentRoot.turn == 0):
            currentRoot = ABMove(currentRoot, 0,float("-inf"),float("inf"), 4)[0]
            print("MADE MOVE")
            print(currentRoot)

        else:
            currentRoot = ABMove(currentRoot, 0,float("-inf"),float("inf"), 6)[0]
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
    gameT = gameTree(4, 5)

    # numStates = len(gameT.allStates)
    # copy = gameT.root.copyState()
    # copy.players[0].hands = [0,2,1,4]
    # copy.players[1].hands = [1,1,3,2]
    # copy.turn = 0
    # print("OG")
    # print(copy)
    # print(copy.evaluateScore())
    # copy.makeTurn(0,0, True)
    # print(copy)
    # print("states")
    # states = copy.expandStates()
    # # for state in states:
    # #     print(state)
    # #     print(state.evaluateScore())
    # state = ABMove(copy, 0,float("-inf"),float("inf"), 3)[0]
    # print("Choice")
    # print(state)

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
