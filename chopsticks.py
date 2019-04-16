
#Game Tree, each node is a state
class gameTree:
    def __init__(self,numHands, numFingers):
        self.numHands = numHands
        self.numFingers = numFingers
        self.root = state(player(numHands, numFingers), player(numHands, numFingers),0)


#State has two players
class state:
    def __init__(self, player1, player2, turn):
        self.players = [player1, player2]
        self.turn = turn

    def __str__(self):
        return ("Player 1's state: " + str(self.players[0].hands) +
            "\nPlayer 2's state: " + str(self.players[1].hands) +
            "\nPlayer " + str(self.turn) + "'s turn")

    def copyState(self):
        newPlayer1 = player(self.players[0].numHands, self.players[0].numFingers)
        newPlayer2 = player(self.players[1].numHands, self.players[1].numFingers)
        newPlayer1.hands = self.players[0].hands[:]
        newPlayer2.hands = self.players[1].hands[:]


        return state(newPlayer1, newPlayer2, self.turn)


    def checkWin(self):
        if sum(self.players[self.turn].hands) == 0:
            if self.turn == 0:
                return ("Player 2 has won!!!")
            else:
                return "Player 1 has won!!!"
    def expandStates(self):
        possibleStates = []
        playerMoves = set()

        for i in range(len(self.players[self.turn].hands)):

            #if((self.players[self.turn].hands[i] not in playerMoves)):
                playerMoves.add(self.players[self.turn].hands[i])
                #print(self.players[self.turn].hands[i])
                for j in range(len(self.players[self.turn].hands)):


                    copy = self.copyState()

                    copy.makeTurn(i, j, False)
                    possibleStates.append(copy)
        copy = self.copyState()
        copy.makeTurn(0,0, True)
        possibleStates.append(copy)
        return possibleStates




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
            print("This hand is already out!")
            return

        newVal = (self.hands[hand] + number) % self.numFingers
        self.hands[hand] = newVal


def main():
    gameT = gameTree(2, 5)
    print(gameT.root)
    print("----")
    #gameT.root.makeTurn(gameT.root.turn,1,False)
    copy = gameT.root.copyState()
    gameT.root.players[0].hands[1] = 4
    states = gameT.root.expandStates()
    print("_____")
    for state in states:
        print(state)


if __name__ == "__main__":
    main()
