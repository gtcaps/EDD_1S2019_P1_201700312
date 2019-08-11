from Nodes.DoubleCircularNode import DoubleCircularNode
import os

class DoubleCircularList:

    times = 0

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add(self, name):
        if self.head is None:
            self.head = DoubleCircularNode(name)
            self.head.next = self.head
            self.head.back = self.head
            self.tail = self.head
            self.size += 1
        else:
            new_node = DoubleCircularNode(name)
            self.tail.next = new_node
            new_node.back = self.tail
            new_node.next = self.head
            self.tail = new_node
            self.head.back = self.tail
            self.size += 1

    def view_list(self):
        aux_head = self.head
        cont = self.size + 1
        string = ""

        while cont > 0:
            string += " ----> " + str(aux_head.player.name)
            aux_head = aux_head.next
            cont -= 1

        print(string)

        aux_tail = self.head
        cont2 = self.size + 1
        string2 = ""

        while cont2 > 0:
            string2 += " ----> " + str(aux_tail.player.name)
            aux_tail = aux_tail.back
            cont2 -= 1

        print(string2)

    def graph(self):
        self.times += 1
        aux_head = self.head
        string_next = ""
        cont = 1

        file = open("circular-list-{}.dot".format(self.times), "w")
        file.write("digraph DoubleCircularList{\n")
        file.write("    rankdir = LR;\n")
        file.write("    subgraph cluster_0 {")
        file.write('        edge [color="black", minlen="3.0"];')

        while cont <= self.size :
            file.write('        player{}[ shape = record, label = " {{ | {} | }} " ];\n'.format(cont, aux_head.player.name))

            if cont + 1 > self.size:
                string_next += "        player{a} -> player{b};\n        player{b} -> player{a};\n".format(a=cont, b=1)
            else:
                string_next += "        player{a} -> player{b};\n        player{b} -> player{a};\n".format(a=cont, b=cont + 1)

            cont += 1
            aux_head = aux_head.next

        if self.head is None:
            file.write('        player[ shape = record, label = " { | Empty | } " ];\n')
        file.write(string_next)
        file.write('        label = "Lista Doblemente Enlazada de Jugadores";')
        file.write("    }")
        file.write("}")
        file.close()

        os.system("dot -Tpng circular-list-{a}.dot -o circular-list-{a}.png".format(a=self.times))
        os.system("circular-list-{}.png".format(self.times))



