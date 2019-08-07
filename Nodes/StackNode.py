from Classes.Position import Position

class StackNode:
    def __init__(self, x=None, y=None):
        self.position = Position(x, y)
        self.down = None
