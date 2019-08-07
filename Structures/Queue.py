from Nodes.QueueNode import QueueNode
from Classes.Player import Player


class Queue:
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


