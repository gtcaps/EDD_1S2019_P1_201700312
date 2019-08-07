from Classes.Player import Player

class DoubleCircularNode:
    def __init__(self, name=""):
        self.player = Player(name)
        self.next = None
        self.back = None