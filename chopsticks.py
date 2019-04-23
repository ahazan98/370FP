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
    def copyState(self):
        newPlayer1 = player(self.players[0].numHands, self.players[0].numFingers)
        newPlayer2 = player(self.players[1].numHands, self.players[1].numFingers)
        newPlayer1.hands = self.players[0].hands[:]
        newPlayer2.hands = self.players[1].hands[:]


        return state(newPlayer1, newPlayer2, self.turn)

    def evaluateScore(self, turn):
        score = 0
        if(self.checkLose()):

            if(self.turn == 0):
                score = self.players[0].numHands * -10000

            else:

                score = self.players[1].numHands * 10000




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


    def expandStates(self):
        possibleStates = set()
        playerMoves = set()
        copy = self.copyState()
        if( not copy.allSame()):
            copy.makeTurn(0,0, True)
            if(copy.turn == 0):
                copy.turn = 1
                copy.evaluateScore(1)
            else:
                copy.turn = 0
                copy.evaluateScore(0)
                possibleStates.add(copy)
        for i in range(len(self.players[self.turn].hands)):
            for j in range(len(self.players[self.turn].hands)):
                if((self.players[self.turn].hands[i] not in playerMoves)):
                    playerMoves.add(self.players[self.turn].hands[i])
                    copy = self.copyState()

                    copy.makeTurn(i, j, False)
                    if(copy.turn == 0):
                        copy.turn = 1
                        copy.score = copy.evaluateScore(1)
                    else:
                        copy.turn = 0
                        copy.score = copy.evaluateScore(0)

                    possibleStates.add(copy)

        return possibleStates

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


#player has their hand values
class player:
    def __init__(self, numHands, numFingers):
        self.hands = []
        self.numHands = numHands
        self.numFingers = numFingers
        for i in range(numHands):
            self.hands.append(1)

    def receiveMove(self, hand, number):
        if self.hands[hand] == 0:

            return

        newVal = (self.hands[hand] + number) % self.numFingers
        self.hands[hand] = newVal

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


def ABMove(state, depth, alpha, beta, depthLimit):
    if(depth == depthLimit or state.checkLose()):
        return (state, state.evaluateScore(state.turn))
    states = state.expandStates()
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


    while(not currentRoot.checkLose()):
        if(currentRoot.turn == 0):
            currentRoot = ABMove(currentRoot, 0,float("-inf"),float("inf"), 10)[0]
            print(currentRoot)
        else:
            currentRoot = ABMove(currentRoot, 0,float("-inf"),float("inf"), 1)[0]
            print(currentRoot)
        # time.sleep(2)
    if(currentRoot.turn == 0):
        print(currentRoot)
        print("Player 1 has won")
    else:
        print(currentRoot)
        print("Player 2 has won")


def main():
    gameT = gameTree(4, 5)

    numStates = len(gameT.allStates)
    #print(numStates)
    copy = gameT.root.copyState()


    #print(copy.evaluateScore(copy.turn))
    #gameT.allStates = expandTree(gameT)
    gameT.allStates.add(gameT.root)
    state = ABMove(gameT.root, 0, float("-inf"), float("inf"), 10)[0]
    # print(state)
    # state = ABMove(state,0, float("-inf"), float("inf"), 10)[0]
    # print(state)

    playGame(gameT.root)
    #gameT.root.states = gameT.root.expandStates()

    #
    # print("_____")
    # for state in gameT.allStates:
    #     print(state)
    #     print(state.score)
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
