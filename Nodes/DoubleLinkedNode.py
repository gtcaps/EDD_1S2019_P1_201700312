from Classes.Position import Position

class DoubleLinkedNode:
    def __init__(self, x_position=None, y_position=None):
        self.position = Position(x_position, y_position)
        self.next = None
        self.behind = None