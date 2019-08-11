from Nodes.QueueNode import QueueNode
from Classes.Player import Player
import os


class Queue:
    times = 0

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, name, score=0):
        if self.head is None:
            self.head = self.tail = QueueNode(name, score)
            self.size += 1
        else:
            new_node = QueueNode(name, score)
            self.tail.next = new_node
            self.tail = new_node
            self.size += 1

    def dequeue(self):
        if self.head is self.tail:
            self.head = self.tail = None
        else:
            aux_head = self.head
            while aux_head.next is not self.tail:
                aux_head = aux_head.next

            aux_head.next = None
            self.tail = aux_head


    def view(self):
        if self.head is not None:
            aux_head = self.head
            while aux_head is not None:
                print("Name = ",aux_head.player.name, "Score = ", aux_head.player.score)
                aux_head = aux_head.next
        else:
            print("Empty")

    def graph(self):
        self.times += 1
        aux_head = self.head
        cont = 1
        string = ""

        file = open("queue-{}.dot".format(self.times), "w")
        file.write("digraph queue{\n")
        file.write("    rankdir = LR;\n")
        file.write("    subgraph cluster_queue{\n")

        while aux_head is not None:

            if aux_head.next is None:
                file.write('        queue_node{}[  shape = record, label = " {{  ({} , {}) |  }}  " ];\n'.format(cont,aux_head.player.name,aux_head.player.score))
                file.write('        queue_node{}[  shape = record, label = " {{  Null  }}  " ];\n'.format(cont + 1))
            else:
                file.write('        queue_node{}[  shape = record, label = " {{  ({} , {}) |  }}  " ];\n'.format(cont,aux_head.player.name, aux_head.player.score))

            string += "        queue_node{} -> queue_node{} ;\n".format(cont, cont + 1)
            aux_head = aux_head.next
            cont += 1

        if self.head is None:
            file.write('        queue_node[  shape = record, label = " {{  Empty  }}  " ];\n')

        file.write(string)
        file.write('        label = "Cola de Jugadores {}" '.format(self.times))
        file.write("    }\n")
        file.write("}")
        file.close()

        os.system("dot -Tpng queue-{a}.dot -o queue-{a}.png".format(a=self.times))
        os.system("queue-{}.png".format(self.times))




