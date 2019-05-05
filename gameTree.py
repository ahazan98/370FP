from state import state
from player import player

#Game Tree, each node is a state
class gameTree:
    def __init__(self,numHands, numFingers):
        self.numHands = numHands
        self.numFingers = numFingers
        self.root = state(player(numHands, numFingers), player(numHands, numFingers),0)
        self.root.score = 0
        self.allStates = set()
        self.allStates.add(self.root)