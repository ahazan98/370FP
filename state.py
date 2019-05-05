
import math
import time
import random
from player import player
#State has two players
class state:
    def __init__(self, player1, player2, turn, p=None): #need to add parent node to all states (ugh)
        self.players = [player1, player2]
        self.turn = turn
        self.states = []

        self.score = 0
        self.visits = 0
        self.selected = 0
        self.wins = 0
        self.parent = p
        self.utc = 0

    def __str__(self):
        return ("Player 1's state: " + str(self.players[0].hands) +
            "\nPlayer 2's state: " + str(self.players[1].hands) +
            "\nPlayer " + str(self.turn +1) + "'s turn")

    def __eq__(self, other):
        if other == None:
            return False
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

        newPlayer1.splitTimer = self.players[0].splitTimer
        newPlayer2.splitTimer = self.players[1].splitTimer

        newState = state(newPlayer1, newPlayer2, self.turn,self.parent) 
        newState.visits = 0 #self.visits #0
        #does selected need to get changed?
        newState.utc = newState.calcUtc() #do you need to do this? idk
        return newState
    
        
    '''
    score a state we need to revisit this...... I don't think we need the turn parameter
    '''
    def evaluateScore(self):
        score = 0
        if(self.checkWin()):

            if(self.turn == 0):
                score = self.players[0].numHands * -10000

            else:

                score = self.players[1].numHands * 10000

        canKill = 0
        knockoutMoves = set()
        for i in self.players[0].hands:
            for j in self.players[1].hands:
                tuple = (i,j)
                if(i+j >= self.players[0].numFingers and tuple not in knockoutMoves):
                    knockoutMoves.add(tuple)
                    canKill += 1
        if(self.turn == 0):
            score += 200 * canKill
        else:
            score -= 200 * canKill
        for i in self.players[0].hands:
            if(i == 0):
                score -= 100
            elif(float(i) >= .75 * self.players[0].numFingers or i ==0):
                score -= 25

        for i in self.players[1].hands:
            if(i == 0):
                score += 100
            elif(float(i) >= .75 * self.players[1].numFingers or i==0):
                score += 25

        return score

    '''
    check if a player has won the game
    '''
    def checkWin(self):
        p1sum = sum(self.players[0].hands)
        p2sum = sum(self.players[1].hands)
        if p1sum == 0 or p2sum == 0:
            return True
        else:
            return False
        # if(self.turn == 0):
        #     if sum(self.players[1].hands) == 0:
        #         return True
        #     else:
        #         return False
        # else:
        #     if sum(self.players[0].hands) == 0:
        #         return True
        #     else:
        #         return False

    '''
    looks into all the possible moves a player can take in a certain state
    '''
    def expandStates(self):
        possibleStates = set()
        playerMoves = set()
        # print("here")
        possibleStates.add(self)

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

                        if(self.players[self.turn].splitTimer > 0):
                            copy.players[self.turn].splitTimer -= 1
                        copy.score = copy.evaluateScore()

                        if copy != self:
                            copy.parent = self
                            copy.utc = copy.calcUtc()
                            possibleStates.add(copy)
        copy = self.copyState()
        if(not copy.allSame() and self.players[self.turn].splitTimer < 1): #maybe need to change so doesn't affect MCTS
            # print("turn before split " + str(copy.turn))

            copy.makeTurn(0,0, True)
            # print("turn after split"  + str(copy.turn))


            copy.evaluateScore() #changed from 1 to 0.... is this change for the next state?
            if copy != self:
                copy.parent = self
                copy.utc = copy.calcUtc()
                possibleStates.add(copy)

        possibleStates.remove(self)
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

            # liveHand = 0
            #
            # liveHand = liveHands(self.players[self.turn].hands)

            total = sum(self.players[self.turn].hands)
            
            # value = int (total / liveHand)
            value = int(total/ self.players[self.turn].numHands)
            # leftover = total % liveHand
            leftover = total % self.players[self.turn].numHands
            self.players[self.turn].splitTimer = self.players[self.turn].numHands*2
            for i in range(len(self.players[self.turn].hands)):
                # if self.players[self.turn].hands[i] != 0:
                #     self.players[self.turn].hands[i] = value
                self.players[self.turn].hands[i] = value
            j = 0
            while(leftover > 0):
                # if self.players[self.turn].hands[j] != 0:
                #     self.players[self.turn].hands[j] += 1
                #     leftover-= 1
                self.players[self.turn].hands[j] += 1
                leftover-= 1
                j+=1

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


    def liveHands(hands):
          count = 0
          for hand in hands:

              if hand != 0:
                  count+=1
          return count
    '''
    Evaluates the utc score of a given state
    '''
    def calcUtc(self):
        coeff = .6
        value = 0
        value_2 = 0
        #if a state doesn't have a parent, also uses it in ABmove
        if self.parent == None:
            return 0
        else:
            
            if self.visits == 0:
                value = 0
                value_2 = 0
            if self.parent.visits == 0:
                value_2 = 0
            else:
                value = self.wins /self.visits
                
                value_2 = math.sqrt(math.log10(self.parent.visits)/self.visits)
            score = value + coeff * value_2
            return score
