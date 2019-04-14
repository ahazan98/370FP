
#Game Tree, each node is a state
class gameTree:
    def __init__(self,numHands, numFingers):
        self.numHands = numHands
        self.numFingers = numFingers
        self.root = state(player(numHands, numFingers), player(numHands, numFingers),1)


#State has two players 
class state:
    def __init__(self, player1, player2, turn):
        self.players = [player1, player2]
        self.turn = turn
        # self.states = fillStates()
    def __str__(self):
        return ("Player 1's state: " + str(self.players[0].hands) + 
            "\nPlayer 2's state: " + str(self.players[1].hands) + 
            "\nPlayer " + str(self.turn) + "'s turn")
    
    def checkWin(self):
        if sum(self.players[self.turn].hands) == 0:
            if self.turn == 0:
                return ("Player 2 has won!!!")
            else:
                return "Player 1 has won!!!"

         
    
    def makeTurn(self, handM, handR, split):
        if split:
            #call split
            x = 5
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
        self.numFingers = numFingers
        for i in range(numHands):
            self.hands.append(1)
    
    def receiveMove(self, hand, number):
        newVal = (self.hands[hand] + number) % self.numFingers
        self.hands[hand] = newVal
    

def main():
    gameT = gameTree(9, 5)
    print(gameT.root)
    gameT.root.makeTurn(gameT.root.turn,1,False)
    print(gameT.root)

if __name__ == "__main__":
    main()