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
    player receives a move on their hand
    '''
    def receiveMove(self, hand, number):
        if self.hands[hand] == 0:

            return

        # newVal = (self.hands[hand] + number)
        newVal = (self.hands[hand] + number) % self.numFingers #maybe include spillover?
        if(newVal >= self.numFingers):
            newVal = 0
        self.hands[hand] = newVal
