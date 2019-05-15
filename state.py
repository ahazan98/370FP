
import math
import time
import random
from player import player
#State has two players
class state:
    def __init__(self, player1, player2, turn, p=None): 
        self.players = [player1, player2]
        self.turn = turn
        self.states = []
        self.score = 0
        self.visits = 0
        self.selected = 0
        self.wins = 0
        self.parent = p
        self.uct = 0
        self.visited = set()
    def __str__(self):
        return ("Player 1's state: " + str(self.players[0].hands) +
            "\nPlayer 2's state: " + str(self.players[1].hands) +
            "\nPlayer " + str(self.turn +1) + "'s turn")

    def __eq__(self, other):
        if other == None:
            return False
        
        selfh1 = set(self.players[0].hands)
        selfh2 = set(self.players[1].hands)
        otherh1 = set(other.players[0].hands)
        otherh2 = set(other.players[1].hands)
        
        if (selfh1 - otherh1) == set() or (selfh2 - otherh2) == set():
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

        newState = state(newPlayer1, newPlayer2, self.turn,self.parent)
        newState.visits = 0 

      
        newState.uct = newState.calcUct()
        return newState


    '''
    score a state we need to revisit this...... I don't think we need the turn parameter
    '''
    def evaluateScore(self):
        score = 0
        if(self.checkWin()):
            p1sum = sum(self.players[0].hands)
            p2sum = sum(self.players[1].hands)

            if(self.turn == 0):
                if p1sum == 0:
                    score = self.players[0].numHands * -10000
                else:
                    score = self.players[0].numHands * 10000

            else:
                if p2sum == 0:
                     score = self.players[1].numHands * 10000
                else:
                    score = self.players[1].numHands * -10000

        
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
        

    '''
    looks into all the possible moves a player can take in a certain state
    '''
    def expandStates(self):
        possibleStates = set()
        playerMoves = set()
        possibleStates.add(self)

        for i in range(len(self.players[self.turn].hands)):
                for j in range(len(self.players[self.turn].hands)):
                    oHand = self.players[self.turn].hands[i]
                    dHand = self.players[(self.turn + 1) % 2].hands[j]
                    tuple = (oHand, dHand)
                    if tuple not in playerMoves and oHand != 0 and dHand != 0:
                        playerMoves.add(tuple)
                        copy = self.copyState()

                        copy.makeTurn(i, j, False)


                        copy.score = copy.evaluateScore()

                        if copy != self:
                            copy.parent = self
                            copy.uct = copy.calcUct()
                            possibleStates.add(copy)
        copy = self.copyState()
        if(not copy.allSame()): 
           

            copy.makeTurn(0,0, True)


            copy.evaluateScore() 
            if copy != self:
                copy.parent = self
                copy.uct = copy.calcUct()
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

            

            total = sum(self.players[self.turn].hands)

            value = int(total/ self.players[self.turn].numHands)
            leftover = total % self.players[self.turn].numHands

            for i in range(len(self.players[self.turn].hands)):
            
                self.players[self.turn].hands[i] = value
            j = 0
            while(leftover > 0):
                
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
    Evaluates the uct score of a given state
    '''
    def calcUct(self):
        coeff = .4
        value = 0
        value_2 = 0
        #if a state doesn't have a parent, also uses it in ABmove
        
        if self.parent == None:
            return 0
        else:
            if self.visits == 0 or self.wins == 0:
                value = 0
            else: 
                value = self.wins/self.visits
            if self.visits == 0 or self.parent.visits == 0:
                value_2 = 0
            else: 
                value_2 = math.sqrt(math.log(self.parent.visits)/self.visits)

                
            score = value + coeff * value_2
            return score

