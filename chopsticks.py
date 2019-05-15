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
def ABMove(state, depth, alpha, beta, depthLimit, allStates,visited):

    if(depth == depthLimit):
        return (state, state.evaluateScore(), visited)
    else:
        state.states = state.expandStates()
        nStates = list(state.states)
        temp = nStates[:]

        for state in temp:

            if(state in allStates):
                nStates.remove(state)
            else:
                allStates.add(state)
                visited.add(state)

        
        if len(nStates) == 0:
            return(state, state.evaluateScore(), visited)
        bestState = nStates[0]
        if(state.turn == 1):
            bestVal = float("-inf")
            for Nstate in nStates:
                result = ABMove(Nstate, depth+1, alpha, beta, depthLimit, allStates,visited)
                if(result[1] > bestVal):
                    bestVal = result[1]
                    bestState = Nstate
                if(bestVal > alpha):
                    alpha = bestVal
                if beta <= alpha:
                    break
                

            return (bestState, bestVal, visited)
        else:
            bestVal = float("inf")

            for Nstate in nStates:
                
                result = ABMove(Nstate, depth+1, alpha, beta, depthLimit, allStates,visited)

                if(result[1] < bestVal):
                    bestVal = result[1]
                    bestState = Nstate

                if(bestVal < beta):
                    beta = bestVal
                if beta <= alpha:
                    break
            return (bestState, bestVal, visited)

'''
Determine the best next move while implementing monte carlo tree search
'''
def mctsMove(root, maxStates):
    root.parent = None 
    root.selected = 1
    count = 0
    start_time = time.time()
    root.states = [] 
    while resources_left(start_time, count, maxStates):
        leaf = traverse(root)
        simulation_result = rollout(leaf)
        count+= 1
        backpropogate(leaf,simulation_result)

    return best_child(root) 

def resources_left(start_time, count, maxStates):
    current_time = time.time()
    if count > maxStates: #could add a time here if you want
        
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
    while isBoundary(state) == False: 
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
    else: 
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
        node.wins += result
        node.visits += 1
        oldUct = node.uct
        node.uct = node.calcUct()
        node = node.parent
    
def playGame(currentRoot , gameNum):

    count = 0
    p1Visit = set()
    p2Visit = set()
    totalStates = 0
    maxStates = float("inf")

    currentRoot = randomMoves(currentRoot)
    while(not currentRoot.checkWin()):
        if(currentRoot.turn == 0):
            visited = set()
            p1Visit.add(currentRoot)
            # currentRoot = mctsMove(currentRoot, maxStates)
            (currentRoot,score,allStates) = ABMove(currentRoot, 1,float("-inf"),float("inf"), 6, p1Visit, visited)
            p1Visit.update(allStates)
            if len(allStates) != 0:
                maxStates = len(allStates)
            totalStates += len(allStates)
            # print("MADE MOVE")
            # print(currentRoot)
            
        else:
            p2Visit.add(currentRoot)
            # (currentRoot,score,allStates) = ABMove(currentRoot, 1,float("-inf"),float("inf"), 8, p2Visit)
            # p2Visit.update(allStates)
            # if len(allStates) != 0:
            #     maxStates = len(allStates)
            # totalStates += len(allStates)
            currentRoot = mctsMove(currentRoot, maxStates)

            # print("MADE MOVE")
            # print(currentRoot)
            


        count+= 1

        # print(count)
        # print(gameNum)
        if(count > 10000):
            return 0,0
        # print()
    if(currentRoot.turn == 0):
        # print("Player 2 has won")
        return 2,count
    else:
        # print("Player 1 has won")
        return 1,count

def randomMoves(currentRoot):
    for i in range(4):
        states = currentRoot.expandStates()
        currentRoot = random.choice(tuple(states))
        if(len(currentRoot.expandStates()) == 0):
            currentRoot = random.choice(tuple(states))



    return currentRoot

def main():

    ##### ONE GAME #####
    # gameT = gameTree(3,5)
    # randomMoves(gameT.root)
    # r = playGame(gameT.root, 1)

    ##### Bulk testing function #####
    results = open("results.txt","w")
    params = [3,4,5,6,7]
    for fingers in params:
        header = "Playing with " + str(fingers) + " hands\n"
        results.write(header)
        winners = {"p1" : 0, "p2":0}
        loops = 0
        count = 0
        games = 0
        while games <= 29:
            gameT = gameTree(2,4)
            winner = playGame(gameT.root, games)
            if(winner[0] == 1):
                winners["p1"] += 1
                count+= winner[1]
            elif(winner[0] == 2):
                winners["p2"] += 1
                count+= winner[1]
            else:
                print("Caught in loop")
                loops += 1
                games -= 1 
                pass
            
            games += 1
        results.write("AB won "+str(winners["p1"]) + " times\n")
        results.write("MCTS won "+str(winners["p2"]) + " times\n")
        results.write("MCTS won " + str(winners["p2"] / float(winners["p1"] + winners["p2"])) + " percent of the time\n\n")
        
        print(winners["p2"] / float(winners["p1"] + winners["p2"]))
        print("_______")
    results.close()

    
    

    

    
    
if __name__ == "__main__":
    main()
