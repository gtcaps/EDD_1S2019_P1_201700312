from Nodes.StackNode import StackNode

class Stack:
    def __init__(self):
        self.top = None
        self.last = None
        self.size = 0

    def push(self, x, y):
        if self.top is None:
            self.top = self.last = StackNode(x, y)
            self.size += 1
        else:
            new_node = StackNode(x, y)
            new_node.down = self.top
            self.top = new_node
            self.size += 1

    def pop(self):
        if self.top is self.last:
            self.top = self.last = None
            self.size -= 1
        else:
            self.top = self.top.down
            self.size -= 1


    def view_stack(self):
        aux_top = self.top
        while aux_top is not None:
            print("[ " + str(aux_top.position.x_position) + " , " + str( aux_top.position.y_position ) + " ]" )
            aux_top = aux_top.down
