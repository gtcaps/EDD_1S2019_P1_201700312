from Nodes.DoubleLinkedNode import DoubleLinkedNode
import os

class DoubleLinkedList:
    times = 0

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_in_front(self,x, y):
        if self.head is None:
            self.head = self.tail = DoubleLinkedNode(x,y)
            self.size += 1
        else:
            new_node = DoubleLinkedNode(x, y)
            new_node.next = self.head
            self.head.behind = new_node
            self.head = new_node
            self.size += 1

    def insert_in_back(self, x, y):
        if self.head is None:
            self.head = self.tail = DoubleLinkedNode(x, y)
            self.size += 1
        else:
            new_node = DoubleLinkedNode(x, y)
            new_node.behind = self.tail
            self.tail.next = new_node
            self.tail = new_node
            self.size += 1

    def delete_in_front(self):
        if self.head is self.tail:
            self.head = self.tail = None
            self.size -= 1
        else:
            self.head = self.head.next
            self.head.behind = None
            self.size -= 1

    def delete_in_back(self):
        if self.tail is self.head:
            self.tail = self.head = None
            self.size -= 1
        else:
            self.tail = self.tail.behind
            self.tail.next = None
            self.size -= 1

    def view_list(self):
        aux_head = self.head
        list = "None"
        while aux_head is not None:
            list += " ---> [{} , {}] ".format(aux_head.position.x_position, aux_head.position.y_position)
            aux_head = aux_head.next
        print(list)

        aux_tail = self.tail
        list2 = "None"
        while aux_tail is not None:
            list2 += " ---> [{} , {}] ".format(aux_tail.position.x_position, aux_tail.position.y_position)
            aux_tail = aux_tail.behind
        print(list2)

    def graph(self):
        aux_head = self.head
        self.times += 1
        cont = 1

        file = open("double-list-{}.dot".format(self.times), "w")
        file.write("digraph DoubleList{\n")
        file.write("    rankdir = LR;\n")
        file.write("    subgraph cluster_0 {\n")

        if aux_head is not None:
            string_next = '        snake0 -> snake1 [color="none"];\n        snake1 -> snake0;\n'
            file.write('        snake0[ shape = record, label = " { | NULL | } "];\n')
            file.write('        snake00[ shape = record, label = " { | NULL | } "];\n')

            while aux_head is not None:
                file.write('        snake{}[ shape = record, label = " {{ | ({},{}) | }} " ];\n'.format(cont,aux_head.position.x_position,aux_head.position.y_position))

                if cont + 1 > self.size:
                    string_next += '        snake{} -> snake00;\n'.format(cont)
                else:
                    string_next += '        snake{} -> snake{};\n'.format(cont, cont + 1)
                    string_next += '        snake{} -> snake{};\n'.format(cont + 1, cont)
                aux_head = aux_head.next
                cont += 1
            file.write(string_next)
        else:
            file.write('        snake0[ shape = record, label = " { | Empty | } "];\n')

        file.write('        label = "Lista Doble del Snake";\n')
        file.write("    }\n")
        file.write('    label = "Size of the snake = {} nodes"'.format(self.size))
        file.write("}")
        file.close()

        os.system("dot -Tpng double-list-{a}.dot -o double-list-{a}.png".format(a=self.times))
        os.system("double-list-{}.png".format(self.times))