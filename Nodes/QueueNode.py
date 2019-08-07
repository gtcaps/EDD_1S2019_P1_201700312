from Classes.Player import Player

class QueueNode:

    def __init__(self, name="", score=0):
        self.player = Player(name, score)
        self.next = None

