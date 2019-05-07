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
def ABMove(state, depth, alpha, beta, depthLimit, allStates):

    if(depth == depthLimit):
        return (state, state.evaluateScore(), allStates)
    else:
        states = state.expandStates()
        states = list(states)
        temp = states[:]

        for state in temp:

            if(state not in allStates):
                allStates.add(state)
            else:
                states.remove(state)


        allStates.update(states)
        if len(states) == 0:
            return(state, state.evaluateScore(), allStates)
        bestState = state
        if(state.turn == 0):
            bestVal = float("-inf")
            for Nstate in states:
                result = ABMove(Nstate, depth+1, alpha, beta, depthLimit, allStates)
                if(result[1] > bestVal):
                    bestVal = result[1]
                    bestState = Nstate
                if(bestVal > alpha):
                    alpha = bestVal
                if beta <= alpha:
                    break
            return (bestState, bestVal, allStates)
        else:
            bestVal = float("inf")

            for Nstate in states:
                # print("Nstate")
                # print(Nstate)
                result = ABMove(Nstate, depth+1, alpha, beta, depthLimit, allStates)
                # print("result:" + str(result[1]))
                if(result[1] < bestVal):
                    bestVal = result[1]
                    bestState = Nstate

                if(bestVal < beta):
                    beta = bestVal
                # print("beta: "+str(beta))
                if beta <= alpha:
                    # print("here")
                    break
            # print(bestState)
            # print(bestVal)
            return (bestState, bestVal, allStates)

'''
Determine the best next move while implementing monte carlo tree search
'''
def mctsMove(root):
    start_time = time.time()
    # root.states = [] #do we need to delete the states from the last player's turn?
    while resources_left(start_time):
        leaf = traverse(root)
        simulation_result = rollout(leaf)
        backpropogate(leaf,simulation_result)
    return best_child(root) #child with highest number of visits

def resources_left(start_time):
    current_time = time.time()
    # print(current_time)
    if current_time > start_time + .25: #idk how long to use
        return False
    return True

def best_child(root):
    bc = root.states[0]
    for state in root.states[1:]:
        if state.visits > bc.visits:
            bc = state
    return bc

def traverse(state):
    while isBoundary(state) == False: #need better criteria for deciding if
        selected_states = []
        for index in range(len(state.states)): #select all children that have been expanded upon
            if state.states[index].selected == 1:
                selected_states.append(index)
        best_state = state.states[0]
        for index in selected_states: #pick the bet utc of the selected states
            #pick maximum state
            if state.states[index].utc > best_state.utc:
                best_state = state.states[index]
        state = best_state

    if state.checkWin(): #return that state if it is a win
        return state
    else: #expand its children and then pick a random one to expand upon
        state.states = list(state.expandStates())
        rand_child = random.randint(0,len(state.states)-1)
        state.states[rand_child].selected = 1
        return state.states[rand_child]

def isBoundary(state):

    if state.selected == 1: #if part of frontier
        if state.states == []: #if its children have been not been explored, then we know its on an edge
            return True
        else: #it has children, but it is a boundary only if none of its children are selected
            for state in state.states:
                if state.selected == 1: #then one of its states is part of the frontier and will be expanded
                    return False
            return True
    else: #if it hasn't been selected, then something is messed up and should let us know
        return -1

def rollout(start):
    curr = start
    while not curr.checkWin():
        if curr.states == []:
            curr.states = list(curr.expandStates())
        rand_child = random.randint(0,len(curr.states)-1)
        curr = curr.states[rand_child]

    #at a end state, if the player opposite the turn has no fingers return a one, else return 0
    turn = curr.turn
    p1sum = sum(curr.players[0].hands)
    p2sum = sum(curr.players[1].hands)
    if turn == 0:
        if p2sum == 0:
            return 1
        else:
            return 0
    else:
        if p1sum == 0:
            return 1
        else:
            return 0

def backpropogate(node, result):
    if node.parent == None:
        return
    node.wins += result
    node.visits += 1
def playGame(currentRoot):

    count = 0
    p1Visit = set()
    p2Visit = set()
    # not currentRoot.checkWin()
    while(not currentRoot.checkWin()):
        if(currentRoot.turn == 0):
            p1Visit.add(currentRoot)
            (currentRoot,score,allStates) = ABMove(currentRoot, 0,float("-inf"),float("inf"), 10, p1Visit)
            print("MADE MOVE")
            print(currentRoot)
            p1Visit.update(allStates)
            print(len(allStates))
            print("_____")

        else:

            (currentRoot,score,allStates) = ABMove(currentRoot, 0,float("-inf"),float("inf"), 5, {currentRoot})
            # currentRoot = mctsMove(currentRoot)
            print("MADE MOVE")
            print(currentRoot)
            print(len(allStates))
            print("______")



        count+= 1

        print(count)
        print()
    if(currentRoot.turn == 0):
        print(currentRoot)
        print("Player 2 has won")
        print(len(allStates))
    else:
        print(currentRoot)
        print("Player 1 has won")
        print(len(allStates))



def main():
    gameT = gameTree(4, 5)


    # (currentRoot,score,allStates) = ABMove(gameT.root, 0,float("-inf"),float("inf"), 25, {gameT.root})
    # print(len(allStates))
    # print("__")
    # (currentRoot,score,allStates) = ABMove(currentRoot, 0,float("-inf"),float("inf"), 1, allStates)
    # print("__")
    # (currentRoot,score,allStates) = ABMove(currentRoot, 0,float("-inf"),float("inf"), 1, allStates)
    # print("__")


    # print(len(allStates))
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
