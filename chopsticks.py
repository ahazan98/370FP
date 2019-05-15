import math
import time
import random
import time
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


"""
Runs the Minimax algorithm with Alpha-Beta pruning, or regular Minimax, with lines 55-58 and
74-78 commented out

Parameters : state - The current state of the game tree
             depth - The current depth level on the game tree
             alpha - The minimum score value a state needs to meet for the maximizing player to expand it
             beta - The maximum score value a state needs to meet for the minimizing player to expand it
             depthLimit - The depth limit Minimax is allowed to search to
             allStates - A set of states Minimax has expanded on this turn
Returns :    bestState - The state with the highest(or lowest depending on the turn) estimated value
             bestVal - The estimated value of bestVal
             allStates - A set of states Minimax has expanded on this turn
"""
def ABMove(state, depth, alpha, beta, depthLimit, allStates):

    if(depth == depthLimit):
        return (state, state.evaluateScore(), allStates)
    else:
        states = state.expandStates()
        states = list(states)
        temp = states[:]

        for state in temp:

            if(state in allStates):
                states.remove(state)
            else:
                allStates.add(state)


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

                result = ABMove(Nstate, depth+1, alpha, beta, depthLimit, allStates)

                if(result[1] < bestVal):
                    bestVal = result[1]
                    bestState = Nstate

                if(bestVal < beta):
                    beta = bestVal

                if beta <= alpha:
                    break

            return (bestState, bestVal, allStates)

'''
Determine the best next move while implementing monte carlo tree search
'''
def mctsMove(root, maxStates):
    count = 0
    start_time = time.time()
    root.states = []
    while resources_left(start_time, count, maxStates):
        leaf = traverse(root)
        simulation_result = rollout(leaf)
        count+= 1
        backpropogate(leaf,simulation_result)

    return best_child(root) #child with highest number of visits

def resources_left(start_time, count, maxStates):
    current_time = time.time()

    if current_time > start_time + 3 or count > maxStates:
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
        for index in selected_states: #pick the bet uct of the selected states
            #pick maximum state
            if state.states[index].uct > best_state.uct:
                best_state = state.states[index]
        state = best_state

    if state.checkWin(): #return that state if the game is over
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
    node.uct = node.calcUct()
    backpropogate(node.parent,result)

"""
Runs a game of chopsticks with either Alpha-Beta or MCTS playerMoves

Parameters : currentRoot - The initial root of the game tree, used to set hand and finger parameters
             gameNum - Number of the game in testing, intitially 0, used to keep track of testing

Returns : 1 if Red player has won, 2 if Blue player has won
          count - Number of turns it took for the game to finish
"""
def playGame(currentRoot , gameNum):

    count = 0
    p1Visit = set()
    p2Visit = set()
    totalStates = 0
    maxStates = float("inf")


    while(not currentRoot.checkWin()):
        if(currentRoot.turn == 0):

            p1Visit.add(currentRoot)
            (currentRoot,score,allStates) = ABMove(currentRoot, 1,float("-inf"),float("inf"), 6, p1Visit)
            print("MADE MOVE")
            print(currentRoot)
            p1Visit.update(allStates)
            maxStates = len(allStates)
            print(maxStates)
            totalStates += len(allStates)


        else:
            p2Visit.add(currentRoot)
            # (currentRoot,score,allStates) = ABMove(currentRoot, 1,float("-inf"),float("inf"), 2, p2Visit)

            currentRoot = mctsMove(currentRoot, maxStates)
            print("MADE MOVE")
            print(currentRoot)
            print(len(allStates))
            p2Visit.update(allStates)




        count+= 1

        print(count)

        if(count > 10000):
            return 0,0

    if(currentRoot.turn == 0):
        print(currentRoot)
        print("Player 2 has won")

        print(totalStates / float(count))
        return 2,count
    else:
        print(currentRoot)
        print("Player 1 has won")

        print(totalStates / float(count))
        return 1,count
"""
Has each player perfom 3 random moves in order to scramble the starting game state

Parameters : currentRoot - The starting state of the game

Returns : currentRoot - The new random state of the game
"""
def randomMoves(currentRoot):
    for i in range(5):
        states = currentRoot.expandStates()
        currentRoot = random.choice(tuple(states))
        if(len(currentRoot.expandStates()) == 0):
            currentRoot = random.choice(tuple(states))




    return currentRoot

    return currentRoot

def main():

    gameT = gameTree(5,5)


    ##### PLAY AB GAME #####
    # winner = playGame(gameT.root,0)
    #
    # print(winner[1])
    winners = {"p1" : 0, "p2":0}
    loops = 0
    count = 0
    for i in range(30):
        winner = playGame(gameT.root, i)

        print("Player " + str(winner) + " won")
        if(winner[0] == 1):
            winners["p1"] += 1
            count+= winner[1]
        elif(winner[0] == 2):
            winners["p2"] += 1
            count+= winner[1]
        else:
            print("Caught in loop")
            loops += 1
            pass
        print(winners["p1"] / float(winners["p1"] + winners["p2"]))
        time.sleep(3)
    # print(winners["p1"])
    # print(winners["p2"])
    # print(winners["p1"] / float(winners["p1"] + winners["p2"]))
    # print(count / float(30))
    # print(loops)



if __name__ == "__main__":
    main()
