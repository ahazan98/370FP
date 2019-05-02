import math
import time
import random
#Game Tree, each node is a state
class gameTree:
    def __init__(self,numHands, numFingers):
        self.numHands = numHands
        self.numFingers = numFingers
        self.root = state(player(numHands, numFingers), player(numHands, numFingers),0)
        self.root.score = 0
        self.allStates = set()
        self.allStates.add(self.root)

#State has two players
class state:
    def __init__(self, player1, player2, turn):
        self.players = [player1, player2]
        self.turn = turn
        self.states = []
        self.score = 0

    def __str__(self):
        return ("Player 1's state: " + str(self.players[0].hands) +
            "\nPlayer 2's state: " + str(self.players[1].hands) +
            "\nPlayer " + str(self.turn +1) + "'s turn")

    def __eq__(self, other):
        p1s1Hands = {}
        p2s1Hands = {}
        p1s2Hands = {}
        p2s2Hands = {}
        for hand in range(len(self.players[0].hands)):
            if(self.players[0].hands[hand] in p1s1Hands):
                p1s1Hands[self.players[0].hands[hand]] += 1
            else:
                p1s1Hands[self.players[0].hands[hand]] = 1
            if(self.players[1].hands[hand] in p2s1Hands):
                p2s1Hands[self.players[1].hands[hand]] += 1
            else:
                p2s1Hands[self.players[1].hands[hand]] = 1
            if(other.players[0].hands[hand] in p1s2Hands):
                p1s2Hands[other.players[0].hands[hand]] += 1
            else:
                p1s2Hands[other.players[0].hands[hand]] = 1
            if(other.players[1].hands[hand] in p2s2Hands):
                p2s2Hands[other.players[1].hands[hand]] += 1
            else:
                p2s2Hands[other.players[1].hands[hand]] = 1
        if(p1s1Hands == p1s2Hands and p2s1Hands == p2s2Hands):
            return True
        else:
            return False

    def __hash__(self):
        return hash(tuple(self.players[0].hands)) + hash(tuple(self.players[1].hands))
    
    '''
    return the copy of a state
    '''
    def copyState(self):
        newPlayer1 = player(self.players[0].numHands, self.players[0].numFingers)
        newPlayer2 = player(self.players[1].numHands, self.players[1].numFingers)
        newPlayer1.hands = self.players[0].hands[:]
        newPlayer2.hands = self.players[1].hands[:]


        return state(newPlayer1, newPlayer2, self.turn)


    '''
    score a state we need to revisit this...... I don't think we need the turn parameter
    '''
    def evaluateScore(self, turn):
        score = 0
        if(self.checkLose()):

            if(self.turn == 0):
                score = self.players[0].numHands * -10000

            else:

                score = self.players[1].numHands * 10000

        numDead = 0
        for i in self.players[0].hands:
            for j in self.players[1].hands:
                if(i+j >= self.players[0].numFingers):
                    numDead += 1
        if(turn == 0):
            score += 50 * numDead
        else:
            score -= 50 * numDead
        for i in self.players[0].hands:
            if(i == 0):
                score -= 100
            elif(float(i) >= .75 * self.players[0].numFingers):
                score -= 25

        for i in self.players[1].hands:
            if(i == 0):
                score += 100
            elif(float(i) >= .75 * self.players[1].numFingers):
                score += 25

        return score

    '''
    check if a player has lost the game
    '''
    def checkLose(self):
        if(self.turn == 0):
            if sum(self.players[0].hands) == 0:
                return True
            else:
                return False
        else:
            if sum(self.players[1].hands) == 0:
                return True
            else:
                return False

    '''
    looks into all the possible moves a player can take in a certain state
    '''
    def expandStates(self):
        possibleStates = set()
        playerMoves = set()
        # print("here")

        for i in range(len(self.players[self.turn].hands)):
            # if(0 < self.players[self.turn].hands[i]):
                for j in range(len(self.players[self.turn].hands)):
                    # if((self.players[self.turn].hands[i] not in playerMoves)):
                    oHand = self.players[self.turn].hands[i]
                    dHand = self.players[(self.turn + 1) % 2].hands[j]
                    tuple = (oHand, dHand)
                    if tuple not in playerMoves and oHand != 0 and dHand != 0:
                        playerMoves.add(tuple)
                        # playerMoves.add(self.players[self.turn].hands[i])
                        copy = self.copyState()
                        # print("turn before move " + str(copy.turn))
                        copy.makeTurn(i, j, False)
                        # print("turn after move "  + str(copy.turn))
                    
                        if(copy.turn == 0):
                            copy.score = copy.evaluateScore(1)
                        else:
                            copy.score = copy.evaluateScore(0)
                        if copy != self:
                            possibleStates.add(copy)
        copy = self.copyState()
        if(not copy.allSame()):
            # print("turn before split " + str(copy.turn))

            copy.makeTurn(0,0, True)
            # print("turn after split"  + str(copy.turn))

            if(copy.turn == 0):
                copy.evaluateScore(0) #changed from 1 to 0.... is this change for the next state?
                if copy != self:
                    possibleStates.add(copy)
            else:
                # print("changing turn")
                copy.evaluateScore(1) #changed from 0 to 1... is this chcange for the next state?
                if copy != self:
                    possibleStates.add(copy)

        return possibleStates

    '''
    Tests to see if all of a player's hands are the same
    '''
    def allSame(self):

        if self.turn == 0:
            prev = self.players[0].hands[0]
            for hand in self.players[0].hands:
                if(hand != prev):
                    return False
            return True
        else:
            prev = self.players[1].hands[0]
            for hand in self.players[1].hands:
                if(hand != prev):
                    return False
            return True



    '''
    Encodes making a turn, if they decide to split, distribute the number of fingers 
    evenly among the hands of the player. If they decide to make the move, the receiving
    player will take the move
    '''
    def makeTurn(self, handM, handR, split):
        if split:

            total = sum(self.players[self.turn].hands)
            value = int (total / self.players[self.turn].numHands)
            leftover = total % self.players[self.turn].numHands
            for i in range(len(self.players[self.turn].hands)):
                self.players[self.turn].hands[i] = value
            for j in range(leftover):
                self.players[self.turn].hands[j] += 1

        else:
            offense = self.players[self.turn]
            if self.turn == 1:
                receiving = self.players[0]
            else:
                receiving = self.players[1]
            receiving.receiveMove(handR, offense.hands[handM])
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0


#player has their hand values
class player:
    def __init__(self, numHands, numFingers):
        self.hands = []
        self.numHands = numHands
        self.numFingers = numFingers
        for i in range(numHands):
            self.hands.append(1)

    '''
    player receives a move on their hand
    '''
    def receiveMove(self, hand, number):
        if self.hands[hand] == 0:

            return

        newVal = (self.hands[hand] + number) 
        # newVal = (self.hands[hand] + number) % self.numFingers #maybe include spillover?
        if(newVal >= self.numFingers):
            newVal = 0
        self.hands[hand] = newVal

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
    
    if(depth == depthLimit or state.checkLose()):
        return (state, state.evaluateScore(state.turn))
    states = state.expandStates()
    # for state in states:
    #     print("state: ")
    #     print(state)
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
    while(not currentRoot.checkLose()):
        if(currentRoot.turn == 0):
            currentRoot = ABMove(currentRoot, 0,float("-inf"),float("inf"), 16)[0]
            print("MADE MOVE")
            print(currentRoot)
        else:
            currentRoot = ABMove(currentRoot, 0,float("-inf"),float("inf"), 9)[0]
            print("MADE MOVE")

            print(currentRoot)
            
        # states = currentRoot.expandStates()
        # for state in states:
        #     if(state == currentRoot):
        #         print("same")
        # time.sleep(2
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
    gameT = gameTree(3, 20)

    numStates = len(gameT.allStates)
    copy = gameT.root.copyState()
    # print(copy)
    # print(copy.turn)

    ##### PLAY AB GAME #####
    # playGame(gameT.root)

    ##### TEST EXPANDSTATES() #####
    # states = copy.expandStates()
    # for state in states:
    #     print(state)

    ##### COLLECTION OF AB MOVES ######
    print("pre turn: " + str(copy.turn))
    nextState = ABMove(copy, 0,float("-inf"),float("inf"), 5)[0]
    print(nextState)
    print("post turn: " + str(nextState.turn))

    nextState = ABMove(nextState, 0,float("-inf"),float("inf"), 5)[0]
    print
    print(nextState)

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
    #     if(state.checkLose()):
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
