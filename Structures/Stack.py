from Nodes.StackNode import StackNode
import os

class Stack:
    times = 0
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

    def graph(self):
        self.times += 1
        aux_head = self.top

        string = " |"

        if aux_head is not None:
            while aux_head is not None:
                if aux_head.down is None:
                    string += " ( {} , {} ) ".format(aux_head.position.x_position, aux_head.position.y_position)
                else:
                    string += " ( {} , {} ) |".format(aux_head.position.x_position, aux_head.position.y_position)
                aux_head = aux_head.down
        else:
            string = "Empty"


        file = open("stack-{}.dot".format(self.times), "w")
        file.write("digraph stack{\n")
        file.write("    rankdir = LR;\n")
        file.write("    subgraph cluster_stack{\n")
        file.write('        stack_node[ shape = record, label = " {} " ];\n'.format(string))
        file.write('        label = "Pila de Puntos {}" \n'.format(self.times))
        file.write("    }\n")
        file.write("}")
        file.close()

        os.system("dot -Tpng stack-{a}.dot -o stack-{a}.png".format(a=self.times))
        os.system("stack-{}.png".format(self.times))











