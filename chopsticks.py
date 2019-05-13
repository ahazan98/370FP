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

            if(state in allStates):
                states.remove(state)
            else:
                allStates.add(state)

        
        if len(states) == 0:
            return(state, state.evaluateScore(), allStates)
        bestState = states[0]
        if(state.turn == 0):
            bestVal = float("-inf")
            for Nstate in states:
                result = ABMove(Nstate, depth+1, alpha, beta, depthLimit, allStates)
                # print(str(result[1]) + ", " + str(bestVal))
                if(result[1] > bestVal):
                    bestVal = result[1]
                    bestState = Nstate
                if(bestVal > alpha):
                    alpha = bestVal
                if beta <= alpha:
                    break
                # # else:
                # allStates.add(Nstate)

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
                # print("beta: "+str(beta))
                if beta <= alpha:
                    # print("here")
                    break
                # else:
                # allStates.add(Nstate)

            # print(bestState)
            # print(bestVal)
            return (bestState, bestVal, allStates)

'''
Determine the best next move while implementing monte carlo tree search
'''
def mctsMove(root, maxStates):
    root.parent = None #need to set this so it doesn't recurse back farther than it needs?
    root.selected = 1
    count = 0
    start_time = time.time()
    root.states = [] #do we need to delete the states from the last player's turn?
    while resources_left(start_time, count, maxStates):
        leaf = traverse(root)
        simulation_result = rollout(leaf)
        count+= 1
        backpropogate(leaf,simulation_result)

    return best_child(root) #child with highest number of visits

def resources_left(start_time, count, maxStates):
    current_time = time.time()
    if current_time > start_time + 1 or count > maxStates: #idk how long to use
        return False
    return True

def best_child(root):
    bc = root.states[0]
    if bc.checkWin():

        p1sum = sum(bc.players[0].hands)
        p2sum = sum(bc.players[1].hands)
        if bc.turn == 0 and p1sum == 0:
            return bc
        elif bc.turn == 1 and p2sum == 0:
            return bc
    for state in root.states[1:]:
        if state.checkWin():
            p1sum = sum(state.players[0].hands)
            p2sum = sum(state.players[1].hands)
            
            if state.turn == 0 and p1sum == 0:
                return state
            elif state.turn == 1 and p2sum == 0:
                return state
        else:
            if state.uct > bc.uct:
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
        # print("here")
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
        if p1sum == 0:
            return 1
        else:
            return 0
    else:
        if p2sum == 0:
            return 1
        else:
            return 0

def backpropogate(node, result):
    while node.parent != None:
        if node.selected == 1:
            node.wins += result
            node.visits += 1
            node.uct = node.calcUct()
        node = node.parent
    '''
    RECURSION BACKPROPOGATE
    if node.parent == None:
        return
    node.wins += result
    node.visits += 1
    node.uct = node.calcUct()
    backpropogate(node.parent,result)
    '''
def playGame(currentRoot , gameNum):

    count = 0
    p1Visit = set()
    p2Visit = set()
    totalStates = 0
    maxStates = float("inf")

    currentRoot = randomMoves(currentRoot)
    # print(currentRoot)
    while(not currentRoot.checkWin()):
        if(currentRoot.turn == 0):

            p1Visit.add(currentRoot)
            (currentRoot,score,allStates) = ABMove(currentRoot, 1,float("-inf"),float("inf"), 6, p1Visit)
            print("MADE MOVE")
            print(currentRoot)
            p1Visit.update(allStates)
            maxStates = len(allStates)
            # print(maxStates)
            totalStates += len(allStates)
            # print("_____")

        else:
            p2Visit.add(currentRoot)
            # (currentRoot,score,allStates) = ABMove(currentRoot, 1,float("-inf"),float("inf"), 8, p2Visit)
            currentRoot = mctsMove(currentRoot, maxStates)

            print("MADE MOVE")
            print(currentRoot)
            # print(len(allStates))
            # p2Visit.update(allStates)
            # maxStates = len(allStates)
            # totalStates += len(allStates)
            # print(len(allStates))
            # print("______")



        count+= 1

        print(count)
        # print(gameNum)
        if(count > 10000):
            return 0,0
        # print()
    if(currentRoot.turn == 0):
        # print(currentRoot)
        print("Player 2 has won")
        # print(len(allStates))
        # print(totalStates / float(count))
        return 2,count
    else:
        # print(currentRoot)
        print("Player 1 has won")
        # print(len(allStates))
        # print(totalStates / float(count))
        return 1,count

def randomMoves(currentRoot):
    for i in range(4):
        states = currentRoot.expandStates()
        currentRoot = random.choice(tuple(states))
        if(len(currentRoot.expandStates()) == 0):
            currentRoot = random.choice(tuple(states))


    # return currentRoot

    return currentRoot

def main():
    # tree = gameTree(3,5)
    # root = tree.root
    # root.players[0].hands = [0,4,3]
    # root.players[1].hands = [0,1,0]
    # root.turn = 0
    # p1Visit = set()
    # root.states = root.expandStates()
    # for state in root.states:
    #     print(state)
    #     print(state.score)

    # (currentRoot,score,allStates) = ABMove(root, 1,float("-inf"),float("inf"),2 , p1Visit)
    # currentRoot = mctsMove(root, float("inf"))

    # print(currentRoot)
    # print(currentRoot.score)
    # print("MADE MOVE")


    ##### PLAY AB GAME #####
    
    # winners = {"p1" : 0, "p2":0}
    # loops = 0
    # count = 0
    # games = 0
    # while games <= 29:
    # # for i in range(30):
    #     print(games)
    #     gameT = gameTree(5,5)
    #     winner = playGame(gameT.root, games)

    #     print("Player " + str(winner) + " won")
    #     if(winner[0] == 1):
    #         winners["p1"] += 1
    #         count+= winner[1]
    #     elif(winner[0] == 2):
    #         winners["p2"] += 1
    #         count+= winner[1]
    #     else:
    #         print("Caught in loop")
    #         loops += 1
    #         games -= 1 
    #         pass
    #     print(winners["p2"] / float(winners["p1"] + winners["p2"]))
    #     # time.sleep(3)
    #     games += 1
    # print(winners["p1"])
    # print(winners["p2"])
    # print(winners["p2"] / float(winners["p1"] + winners["p2"]))
    # print(count / float(30))
    # print(loops)


    #### TEST EXPANDSTATES() #####
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

    
    
    ##### ONE GAME #####
    gameT = gameTree(3,5)
    randomMoves(gameT.root)
    r = playGame(gameT.root, 1)

    

    
    
if __name__ == "__main__":
    main()
