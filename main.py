from Structures.Queue import Queue
from Classes.Player import Player
from Structures.DoubleLinkedList import DoubleLinkedList
from Structures.Stack import Stack


#my_queue = Queue()
#my_queue.enqueue("Aybson",50)
#my_queue.enqueue("Pedro",20)
#my_queue.enqueue("Cr7",30)

#my_list =DoubleLinkedList()
#my_list.insert_in_front(10, 54)
#my_list.insert_in_front(20, 53)
#my_list.insert_in_front(30, 52)
#my_list.insert_in_front(40, 51)
#my_list.insert_in_back(00, 00)
#my_list.insert_in_back(10, 10)
#my_list.insert_in_back(20, 20)
#my_list.insert_in_back(30, 30)
#my_list.view_list()

my_stack = Stack()
my_stack.push(10, 20)
my_stack.push(15, 20)
my_stack.push(25, 20)
my_stack.push(35, 20)
my_stack.view_stack()
print("Stack Size: " + str( my_stack.size ))

print("\n")
my_stack.pop()
my_stack.view_stack()
print("Stack Size: " + str( my_stack.size ))

print("\n")
my_stack.pop()
my_stack.view_stack()
print("Stack Size: " + str( my_stack.size ))

print("\n")
my_stack.pop()
my_stack.view_stack()
print("Stack Size: " + str( my_stack.size ))

print("\n")
my_stack.pop()
my_stack.view_stack()
print("Stack Size: " + str( my_stack.size ))



