#player has their hand values
class player:
    def __init__(self, numHands, numFingers):
        self.splitTimer = 0
        self.hands = []
        self.numHands = numHands
        self.numFingers = numFingers
        for i in range(numHands):
            self.hands.append(1)

    '''
    Player receives a move on their hand

    Parameters : self - The player receiving the move
                 hand - The hand being hit
                 number - The number of fingers the other player hit with
    '''
    def receiveMove(self, hand, number):
        if self.hands[hand] == 0:

            return

        # If the sum of the move being made is over numFingers then the player
        # takes the remainder of the move - numFingers
        newVal = (self.hands[hand] + number) % self.numFingers
        if(newVal >= self.numFingers):
            newVal = 0
        self.hands[hand] = newVal
