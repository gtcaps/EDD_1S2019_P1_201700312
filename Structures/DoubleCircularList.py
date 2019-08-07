from Nodes.DoubleCircularNode import DoubleCircularNode

class DoubleCircularList:

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
