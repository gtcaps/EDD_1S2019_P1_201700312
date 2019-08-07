from Nodes.DoubleLinkedNode import DoubleLinkedNode

class DoubleLinkedList:
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